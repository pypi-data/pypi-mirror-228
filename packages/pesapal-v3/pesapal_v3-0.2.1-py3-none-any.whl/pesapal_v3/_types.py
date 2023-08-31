"""Custom types for Pesapal SDK."""
from typing import Literal, NamedTuple, Optional, TypeAlias

Environment: TypeAlias = Literal["sandbox", "production"]
RedirectMode: TypeAlias = Literal["TOP_WINDOW", "PARENT_WINDOW"]
SubscriptionFrequency: TypeAlias = Literal["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]


class PesapalError(NamedTuple):
    """A pesapal API access error"""

    error_type: str
    code: str
    message: str
    # call_back_url: Optional[str]

    def __repr__(self) -> str:
        return (
            f"error_type: {self.error_type}, code: {self.code}, message: {self.message}"
        )


class AccessToken(NamedTuple):
    """The response of the returned token."""

    token: str
    expiryDate: str
    error: PesapalError
    status: str
    message: str


class IPNRegistration(NamedTuple):
    """The response from a successful IPN URL registration."""

    id: int
    url: str
    ipn_id: str
    status: str
    ipn_status: int
    created_date: str
    error: PesapalError
    notification_type: int
    ipn_status_decription: str
    ipn_notification_type_description: str


class BillingAddress(NamedTuple):
    """Payload for a customer address."""

    email_address: Optional[str]
    phone_number: Optional[str]
    country_code: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    line_1: Optional[str]
    line_2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    zip_code: Optional[str]


class SubscriptionDetails(NamedTuple):
    """Additional details for a subscription."""

    start_date: str
    end_date: str
    frequency: SubscriptionFrequency


class OrderRequest(NamedTuple):
    """Payload to crate a payment request."""

    id: str
    currency: str
    amount: float
    description: str
    callback_url: str
    cancellation_url: Optional[str]
    notification_id: str
    branch: Optional[str]
    billing_address: BillingAddress
    redirect_mode: Optional[RedirectMode]
    account_number: Optional[str]
    subscription_details: SubscriptionDetails


class OrderRequestResponse(NamedTuple):
    """Response of a successfully generated order request."""

    order_tracking_id: str
    merchant_reference: str
    redirect_url: str
    error: Optional[PesapalError]
    status: str


class TransactionStatus(NamedTuple):
    """An order transaction status."""

    payment_method: str
    amount: float
    created_date: str
    confirmation_code: str
    payment_status_description: str
    description: str
    message: str
    payment_account: str
    call_back_url: str
    status_code: str
    payment_status_code: str
    currency: str
    order_tracking_id: str
    merchant_reference: str
    error: Optional[PesapalError]
    status: str
