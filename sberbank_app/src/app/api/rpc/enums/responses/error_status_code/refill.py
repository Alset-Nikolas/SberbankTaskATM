from enum import Enum


class RefillErrorResponseStatusCode(int, Enum):
    currency_not_exist = 401
    bill_not_exist = 402
    bill_quantity_negative = 403
