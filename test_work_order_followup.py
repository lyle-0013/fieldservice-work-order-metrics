import unittest

from work_order_followup import WorkOrder, follow_up_due


class FollowUpDueTests(unittest.TestCase):
    def test_dispatched_order_with_photo_needs_follow_up(self) -> None:
        order = WorkOrder("WO-1042", "dispatched", 3, "tech-17")
        self.assertTrue(follow_up_due(order))


    def test_undispatched_order_with_photo_does_not_need_follow_up(self) -> None:
        order = WorkOrder("WO-1043", "queued", 3, "tech-17")
        self.assertFalse(follow_up_due(order))
