"""Custom exceptions raised in the SDK."""

import builtins
from dataclasses import dataclass

from ._types import PesapalError


class PesapalAPIException(builtins.Exception):
    """Umbrella exception for the Pesapal SDK operations."""


class PesapalAuthError(PesapalAPIException):
    """Pesapal API authentication error."""

    def __init__(self, error: PesapalError, status: str) -> None:
        message = f"{error!r}, status_code: {status}"
        super().__init__(message)
