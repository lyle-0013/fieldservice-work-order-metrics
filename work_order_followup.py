"""Report one field-service work order and decide if follow-up is due."""
from dataclasses import dataclass

from infrai_metrics import infrai


@dataclass(frozen=True)
class WorkOrder:
    work_order_id: str
    dispatch_status: str
    photo_count: int
    technician: str


def follow_up_due(order: WorkOrder) -> bool:
    """A dispatched order with at least one photo needs technician follow-up."""
    return order.dispatch_status == "dispatched" and order.photo_count > 0


def report_order(order: WorkOrder) -> str:
    tags = {"work_order_id": order.work_order_id, "technician": order.technician}
    infrai.metrics.report(type="counter", name="field_service.photos.received", value=order.photo_count, tags=tags)
    due = follow_up_due(order)
    infrai.metrics.report(type="gauge", name="field_service.follow_up_due", value=float(due), tags=tags)
    return "follow-up" if due else "closed"


if __name__ == "__main__":
    sample = WorkOrder("WO-1042", "dispatched", 3, "tech-17")
    print(report_order(sample))
