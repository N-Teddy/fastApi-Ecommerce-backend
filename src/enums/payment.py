from enum import Enum

class PaymentMethod(str, Enum):
    CARD = "card"
    PAY_ON_DELIVERY = "pay_on_delivery"
    TRANSFER = "transfer"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"