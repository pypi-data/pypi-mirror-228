"""Pesapal API client and api methods."""
from datetime import datetime, timedelta
from typing import Dict

import httpx

from pesapal_v3._exceptions import PesapalAuthError
from pesapal_v3._types import AccessToken, Environment


class Pesapal:
    """Pesapal client."""

    _token_timeout = 5

    def __init__(
        self,
        *,
        consumer_key: str,
        consumer_secret: str,
        environment: Environment = "sandbox",
    ) -> None:
        if environment == "sandbox":
            self._base_url = "https://cybqa.pesapal.com/pesapalv3/api"
        else:
            self._base_url = "https://pay.pesapal.com/v3/api"

        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self._token = self._authenticate(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )
        self._instantiation_time = datetime.now()

    def _refresh_token(self) -> bool:
        now = datetime.now()
        refresh = (
            now - self._instantiation_time > timedelta(minutes=self._token_timeout)
            or now.minute != self._instantiation_time.minute
        )
        return refresh

    def _authenticate(self, *, consumer_key: str, consumer_secret: str) -> AccessToken:
        with httpx.Client(base_url=self._base_url) as client:
            data = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
            client_resp = client.post(
                "/Auth/RequestToken", headers=self._headers, json=data
            )
            response = client_resp.json()
            error = response.get("error", None)
            if error:
                raise PesapalAuthError(
                    error=error, status=response.get("status", "500")
                )
            self._headers.update({"Bearer-Token": response.get("token", "")})
            token: AccessToken = AccessToken(**response)
        return token

    def update_headers(self, *, headers: Dict[str, str]) -> None:
        """Updates the header values."""
        self._headers.update(headers)

    def register_ipn_url(
        self, *, ipn_url: str, ipn_notification_type: str = "GET"
    ) -> None:
        """Register the Instant Payment Notification callback URL.

        Arguments:
            ipn_url(str): the URL to register as a callback URL.
            ipn_notification_type(str): the http request method Pesapal will
                use when triggering the IPN alert. Can be GET or POST.
                Default is GET.
        """
        if not self._token:
            raise ValueError("The access token has not been set.")
