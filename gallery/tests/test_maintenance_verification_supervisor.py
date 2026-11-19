#!/usr/bin/env python3
"""Pure policy tests; no network, mutations or workflow reruns."""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location("supervisor", Path(__file__).resolve().parents[1]/"tools/supervise-maintenance-verification.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def run(attempt=1, conclusion="success", status="completed"):
    return dict(run_attempt=attempt, conclusion=conclusion, status=status)

def job(w,name,result="success",failed=None,skipped=()):
    steps=[dict(name=s,conclusion="skipped" if s in skipped else "failure" if s==failed else "success") for s in m.required_steps(w,name)]
    if failed and failed not in [s["name"] for s in steps]:
        steps.insert(0,dict(name=failed,conclusion="failure"))
    return dict(name=name,status="completed",conclusion=result,steps=steps)

def matrix(w):
    return [job(w,n) for n in sorted(m.EXPECTED[w])]

class Policy(unittest.TestCase):
    def test_success_requires_complete_matrix(self):
        for w in m.EXPECTED:
            self.assertEqual(m.classify(w,run(),matrix(w))[0],"pass")
            self.assertEqual(m.classify(w,run(),[])[0],"stop")
    def test_browser_retry_once(self):
        w=m.BROWSER
        jobs=matrix(w)
        jobs[0]=job(w,jobs[0]["name"],"failure",m.ROUTE_TEST)
        self.assertEqual(m.classify(w,run(conclusion="failure"),jobs)[0],"retry")
        self.assertEqual(m.classify(w,run(2,"failure"),jobs)[0],"stop")
        self.assertEqual(m.classify(w,run(2),matrix(w))[0],"pass")
    def test_integrity_failure_stops_even_running_matrix(self):
        w=m.BROWSER
        jobs=matrix(w)
        jobs[0]=job(w,jobs[0]["name"],"failure",m.CHECKS[w][0])
        self.assertEqual(m.classify(w,run(conclusion=None,status="in_progress"),jobs)[0],"stop")
        w=m.INTEGRITY
        for check in m.CHECKS[w]:
            self.assertEqual(m.classify(w,run(conclusion="failure"),[job(w,"integrity","failure",check)])[0],"stop")
    def test_setup_failure_can_retry_without_validation_failure(self):
        for w in m.EXPECTED:
            jobs=matrix(w)
            name=jobs[0]["name"]
            jobs[0]=job(w,name,"failure","Set up Python",m.required_steps(w,name))
            self.assertEqual(m.classify(w,run(conclusion="failure"),jobs)[0],"retry")
    def test_timeout_and_cancel(self):
        w=m.BROWSER
        jobs=matrix(w)
        jobs[0]=job(w,jobs[0]["name"],"timed_out",m.ROUTE_TEST)
        self.assertEqual(m.classify(w,run(conclusion="timed_out"),jobs)[0],"retry")
        jobs[0]["conclusion"]="cancelled"
        self.assertEqual(m.classify(w,run(conclusion="cancelled"),jobs)[0],"stop")
    def test_unknown_failures_stop(self):
        w=m.BROWSER
        jobs=matrix(w)
        jobs[0]=job(w,jobs[0]["name"],"failure","Unknown step")
        self.assertEqual(m.classify(w,run(conclusion="failure"),jobs)[0],"stop")
        self.assertEqual(m.classify(w,run(3),matrix(w))[0],"stop")
    def test_failed_required_step_cannot_pass(self):
        w=m.BROWSER
        jobs=matrix(w)
        jobs[0]=job(w,jobs[0]["name"],"success",m.ROUTE_TEST)
        self.assertEqual(m.classify(w,run(),jobs)[0],"stop")
    def test_duplicate_or_unknown_matrix(self):
        w=m.BROWSER
        jobs=matrix(w)
        self.assertEqual(m.classify(w,run(),jobs+[jobs[0]])[0],"stop")
        self.assertEqual(m.classify(w,run(),jobs+[job(w,"unknown")])[0],"stop")

if __name__=="__main__":
    unittest.main()
