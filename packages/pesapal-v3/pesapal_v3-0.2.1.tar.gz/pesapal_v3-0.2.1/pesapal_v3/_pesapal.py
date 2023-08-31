"""Pesapal API client and api methods."""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import httpx

from pesapal_v3._exceptions import (PesapalAuthError,
                                    PesapalGetTransactionStatusError,
                                    PesapalIPNURLRegError,
                                    PesapalListIPNsError,
                                    PesapalSubmitOrderRequestError)
from pesapal_v3._types import (AccessToken, Environment, IPNRegistration,
                               OrderRequest, OrderRequestResponse,
                               PesapalError, SubscriptionDetails,
                               TransactionStatus)


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
        if not consumer_key:
            raise ValueError("consumer_key cannot be empty")

        if not consumer_secret:
            raise ValueError("consumer_secret cannot be empty")

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret

        if environment == "sandbox":
            self._base_url = "https://cybqa.pesapal.com/pesapalv3/api"
        else:
            self._base_url = "https://pay.pesapal.com/v3/api"

        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self._token = self._authenticate(
            consumer_key=self._consumer_key, consumer_secret=self._consumer_secret
        )
        self._instantiation_time = datetime.now()

    def _refresh_token(self) -> None:
        now = datetime.now()
        refresh = (
            now - self._instantiation_time > timedelta(minutes=self._token_timeout)
            or now.minute != self._instantiation_time.minute
        )
        if refresh:
            self._token = self._authenticate(
                consumer_key=self._consumer_key, consumer_secret=self._consumer_secret
            )

    def _validate_order_request(
        self, order_request: OrderRequest, is_subscription: bool
    ) -> None:
        if not order_request:
            raise ValueError("order_request cannot be empty")
        if is_subscription:
            account = order_request.account_number
            subscription = order_request.subscription_details
            if not account:
                raise ValueError("account is required to create a subscription.")
            if account and bool(subscription):
                if not subscription.start_date:
                    raise ValueError("start_date cannot be empty")
                if not subscription.end_date:
                    raise ValueError("end_date cannot be empty")
                if not subscription.frequency:
                    raise ValueError("frequency cannot be empty")

    def _authenticate(self, *, consumer_key: str, consumer_secret: str) -> AccessToken:
        with httpx.Client(base_url=self._base_url) as client:
            data = {"consumer_key": consumer_key, "consumer_secret": consumer_secret}
            client_resp = client.post(
                "/Auth/RequestToken", headers=self._headers, json=data
            )
            response = client_resp.json()
            error = response.get("error", None)
            status = response.get("status", "500")
            if status != "200":
                raise PesapalAuthError(
                    error=error, status=response.get("status", "500")
                )
            token = response.get("token", "")
            self._headers.update({"Authorization": f"Bearer {token}"})
        return AccessToken(**response)

    def update_headers(self, *, headers: Dict[str, str]) -> None:
        """Updates the header values."""
        self._headers.update(headers)

    def register_ipn_url(
        self, *, ipn_url: str, ipn_notification_type: str = "GET"
    ) -> IPNRegistration:
        """Register the Instant Payment Notification callback URL.

        Arguments:
            ipn_url(str): the URL to register as a callback URL.
            ipn_notification_type(str): the http request method Pesapal will
                use when triggering the IPN alert. Can be GET or POST.
                Default is GET.
        """
        if not ipn_url:
            raise ValueError("ipn_url cannot be empty.")

        if not ipn_notification_type:
            raise ValueError("ipn_notification_type cannot be empty.")

        self._refresh_token()
        with httpx.Client(base_url=self._base_url) as client:
            data = {
                "url": ipn_url,
                "ipn_notification_type": ipn_notification_type,
            }
            client_resp = client.post(
                "/URLSetup/RegisterIPN", headers=self._headers, json=data
            )
            response = client_resp.json()

        message = response.get("message", None)
        if isinstance(message, str):
            message = json.loads(message)

        if isinstance(message, dict):
            error = message.get("error", None)
            status = message.get("status", "500")
            if message and status != "200":
                error_msg = PesapalError(**error)
                raise PesapalIPNURLRegError(error=error_msg, status=status)
        ipn: IPNRegistration = IPNRegistration(**response)
        return ipn

    def get_registered_ipns(self) -> List[IPNRegistration]:
        """Lists all the registered IPN URLS."""
        self._refresh_token()
        with httpx.Client(base_url=self._base_url) as client:
            client_resp = client.get(
                "/URLSetup/GetIpnList",
                headers=self._headers,
            )
            response: List[IPNRegistration] = client_resp.json()
        if isinstance(response, dict):
            error = response.get("error", None)
            status = response.get("status", "500")

            if status != "200":
                error_msg = PesapalError(**error)
                raise PesapalListIPNsError(error=error_msg, status=status)
        return response

    def submit_order_request(
        self, *, order_request: OrderRequest, is_subscription: bool = False
    ) -> OrderRequestResponse:
        """Process the request to create a payment."""
        self._validate_order_request(order_request, is_subscription)
        self._refresh_token()
        with httpx.Client(base_url=self._base_url) as client:
            client_resp = client.post(
                "/Transactions/SubmitOrderRequest",
                headers=self._headers,
                json=order_request,
            )
            response = client_resp.json()
        error = response.get("error", None)
        status = response.get("status", "500")
        if status != "200":
            error_msg = PesapalError(**error)
            raise PesapalSubmitOrderRequestError(error=error_msg, status=status)
        return OrderRequestResponse(**response)

    def get_transaction_status(self, *, order_tracking_id: str) -> TransactionStatus:
        """Get the transaction status of an order."""
        if not order_tracking_id:
            raise ValueError("order_tracking_id cannot be empty")

        self._refresh_token()
        with httpx.Client(base_url=self._base_url) as client:
            client_resp = client.get(
                f"/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}",
                headers=self._headers,
            )
            response = client_resp.json()
        error = response.get("error", None)
        status = response.get("status", "500")
        if status != "200":
            error_msg = PesapalError(**error)
            raise PesapalGetTransactionStatusError(error=error_msg, status=status)
        return TransactionStatus(**response)
