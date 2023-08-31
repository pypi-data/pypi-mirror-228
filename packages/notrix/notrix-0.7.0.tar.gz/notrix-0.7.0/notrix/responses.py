from datetime import datetime


class PaymentPageResponse:
    def __init__(self, uuid: str, price: float, webhook_url: str, link: str):
        self.uuid = uuid
        self.price = price
        self.webhook_url = webhook_url
        self._link = link

    def link(self, user_id: str) -> str:
        return f"{self._link}?userid={user_id}"


class ListenerResponse:
    def __init__(
        self,
        uuid: str,
        dst_address: str,
        expected_amount: float,
        expected_comment: str,
        status: str,
        currency_name: str,
        started_at: datetime,
        active: bool,
    ):
        self.uuid = uuid
        self.address = dst_address
        self.expected_amount = expected_amount
        self.expected_comment = expected_comment
        self.status = status
        self.currency = currency_name
        self.started_at = started_at
        self.active = active
