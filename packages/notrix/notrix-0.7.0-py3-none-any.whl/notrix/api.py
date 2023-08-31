from typing import BinaryIO

import requests
from .responses import PaymentPageResponse, ListenerResponse


class Client:
    BASE_URL = "https://api.notrix.io"

    def __init__(self, secret_api_key: str):
        self.secret_api_key = secret_api_key

    def _auth_headers(self) -> dict:
        return {f"Authorization": f"Token {self.secret_api_key}"}

    def _make_request(self, method: str, path: str, **kwargs):
        request_path = f"{self.BASE_URL}/{path}"
        headers = kwargs.pop("headers", {}).update(self._auth_headers())
        return requests.request(method, request_path, headers=headers, **kwargs)

    def create_payment_page(
        self,
        title: str,
        description: str,
        image: BinaryIO,
        price: float,
        webhook_url: str = None,
    ):
        if webhook_url is None:
            webhook_url = ""

        response = self._make_request(
            "post",
            "api/payment-page/",
            data={
                "title": title,
                "description": description,
                "price": price,
                "webhook_url": webhook_url,
            },
            files={"image": image},
        )

        response.raise_for_status()

        return PaymentPageResponse(**response.json())

    def create_listener(
        self,
        address: str,
        currency_name: str,
        expected_amount: float,
        expected_comment: str,
    ) -> ListenerResponse:
        data = {
            "dst_address": address,
            "currency_name": currency_name,
            "expected_amount": expected_amount,
            "expected_comment": expected_comment,
        }

        response = self._make_request(
            "post",
            "api/listeners/",
            data=data,
        )

        response.raise_for_status()

        return ListenerResponse(**response.json())

    def recheck_listener(self, listener_uuid: str):
        response = self._make_request(
            "post",
            f"api/listeners/{listener_uuid}/recheck/",
        )

        response.raise_for_status()

    def get_listener(self, listener_uuid: str) -> ListenerResponse:
        response = self._make_request(
            "post",
            f"api/listeners/{listener_uuid}/",
        )

        response.raise_for_status()

        return ListenerResponse(**response.json())
