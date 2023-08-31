"""Custom exceptions raised in the SDK."""

import builtins
from dataclasses import dataclass

from ._types import PesapalError


class PesapalAPIException(builtins.Exception):
    """Umbrella exception for the Pesapal SDK operations."""


class PesapalAPIError(PesapalAPIException):
    """Pesapal API error."""

    def __init__(self, error: PesapalError, status: str) -> None:
        message = f"{error!r}, status_code: {status}"
        super().__init__(message)


class PesapalAuthError(PesapalAPIError):
    """Pesapal authentication API error."""


class PesapalIPNURLRegError(PesapalAPIError):
    """Pesapal IPN URL registration error."""


class PesapalSubmitOrderRequestError(PesapalAPIError):
    """Pesapal submit an order request error."""


class PesapalListIPNsError(PesapalAPIError):
    """Pesapal list registered IPNs error."""


class PesapalGetTransactionStatusError(PesapalAPIError):
    """Pesapal get a transaction status error."""
