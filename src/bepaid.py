import base64
import json
from typing import Optional

import aiohttp

from .requester import HttpClient


class BepaidClient:
    API_BASE_URL = 'https://checkout.bepaid.by/ctp/api'

    def __init__(self, token: str, shop_id: int, site_url: str):
        self.token = token
        self.shop_id = shop_id
        self.site_url = site_url

    @property
    def auth_header(self) -> str:
        credentials = f"{self.shop_id}:{self.token}"
        return base64.b64encode(credentials.encode()).decode()

    @property
    def headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Version': '2',
            'Authorization': f'Basic {self.auth_header}'
        }

    def build_param(self, data: dict) -> dict:
        return {
            "wallet_token": self.token,
            "wallet_shop_id": self.shop_id,
            "bot": data.get("bot", "BepaidClient"),
            "pay_id": data.get("pay_id", 0),
            "description": data.get("description", ""),
            "user_id": data.get("user_id", 0),
            "web_site": self.site_url,
            "user": data.get("user", "")
        }

    def build_payload(self, data: dict, param: dict) -> dict:
        return {
            'checkout': {
                'transaction_type': data.get("transaction_type", "payment"),
                'test': data.get("test", False),
                'order': {
                    'amount': data.get("amount", 1),
                    'currency': data.get("currency", "BYN"),
                    'description': data.get("order_description", "Оплата абонемента"),
                    'tracking_id': data.get("tracking_id", 0)
                },
                'customer': {
                    'first_name': str(param['user']),
                },
                'settings': {
                    'notification_url': f"{param['web_site']}/BepaidBy",
                    'success_url': f"{param['web_site']}/success?bot={param['bot']}",
                    'decline_url': f"{param['web_site']}/fail",
                    'fail_url': f"{param['web_site']}/fail",
                    'cancel_url': f"{param['web_site']}/fail",
                    'language': data.get("language", "ru")
                }
            }
        }

    async def parse_response(self, response: aiohttp.ClientResponse, expected_status: int = 200, debug: bool = False) -> dict:
        try:
            payload = await response.json()
        except Exception:
            payload = {"error": "Invalid JSON response"}

        if debug:
            print(json.dumps(payload, indent=2, ensure_ascii=False))

        return {
            "ok": response.status == expected_status,
            "response": payload
        }

    async def create_payment(self, data: Optional[dict] = None, debug: bool = False) -> dict:
        if data is None:
            data = {}

        param = self.build_param(data)
        payload = self.build_payload(data, param)

        async with HttpClient() as client:
            response = await client.async_post(
                url=f'{self.API_BASE_URL}/checkouts',
                json=payload,
                headers=self.headers
            )
            return await self.parse_response(response, expected_status=201, debug=debug)

    async def get_payment_status(self, checkout_token: str, debug: bool = False) -> dict:
        async with HttpClient() as client:
            response = await client.async_get(
                url=f'{self.API_BASE_URL}/checkouts/{checkout_token}/status',
                headers=self.headers
            )
            return await self.parse_response(response, expected_status=200, debug=debug)
