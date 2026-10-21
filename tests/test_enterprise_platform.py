import unittest
from src.enterprise_platform.governance import GovernedGateway, Principal, DEMO_PRINCIPALS

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.gw = GovernedGateway()

    def test_unverified_denied(self):
        r = self.gw.execute(DEMO_PRINCIPALS["Unverified caller"], "finance_report_lookup", "tenant-a")
        self.assertEqual(r["reason"], "identity_not_verified")

    def test_cross_tenant_denied(self):
        r = self.gw.execute(DEMO_PRINCIPALS["Finance reader · tenant A"], "finance_report_lookup", "tenant-b")
        self.assertEqual(r["reason"], "cross_tenant_access")

    def test_role_isolation(self):
        r = self.gw.execute(DEMO_PRINCIPALS["HR reader · tenant A"], "finance_report_lookup", "tenant-a")
        self.assertEqual(r["reason"], "role_not_permitted")

    def test_hr_read(self):
        r = self.gw.execute(DEMO_PRINCIPALS["HR reader · tenant A"], "hr_policy_lookup", "tenant-a")
        self.assertEqual([x["id"] for x in r["records"]], ["hr-01"])

    def test_tenant_b_read(self):
        r = self.gw.execute(DEMO_PRINCIPALS["Finance reader · tenant B"], "finance_report_lookup", "tenant-b")
        self.assertEqual([x["id"] for x in r["records"]], ["fin-02"])

    def test_unregistered_tool(self):
        r = self.gw.execute(DEMO_PRINCIPALS["Finance reader · tenant A"], "unknown_tool", "tenant-a")
        self.assertEqual(r["reason"], "tool_not_registered")

    def test_write_requires_approval(self):
        r = self.gw.execute(DEMO_PRINCIPALS["Finance admin · tenant A"], "vendor_payment_update", "tenant-a", "req-1")
        self.assertEqual(r["status"], "approval_required")

    def test_approved_write_still_not_connected(self):
        self.gw.approve("req-1", DEMO_PRINCIPALS["Approver · tenant A"])
        r = self.gw.execute(DEMO_PRINCIPALS["Finance admin · tenant A"], "vendor_payment_update", "tenant-a", "req-1")
        self.assertEqual(r["reason"], "write_execution_not_connected")

    def test_approval_is_tenant_scoped(self):
        self.gw.approve("req-1", DEMO_PRINCIPALS["Approver · tenant A"])
        admin = Principal("admin-b", "tenant-b", ("finance_admin",), True)
        self.assertEqual(self.gw.execute(admin, "vendor_payment_update", "tenant-b", "req-1")["status"], "approval_required")

    def test_unverified_approver(self):
        self.assertFalse(self.gw.approve("req-1", Principal("fake", "tenant-a", ("approver",), False)))

    def test_audit(self):
        self.gw.execute(DEMO_PRINCIPALS["HR reader · tenant A"], "hr_policy_lookup", "tenant-a", "trace-1")
        self.assertEqual(self.gw.audit[-1]["request_id"], "trace-1")

if __name__ == "__main__":
    unittest.main()
