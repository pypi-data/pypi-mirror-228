"""Custom types for Pesapal SDK."""
from typing import Literal, NamedTuple, TypeAlias


class PesapalError(NamedTuple):
    """A pesapal API access error"""

    error_type: str
    code: str
    message: str

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


Environment: TypeAlias = Literal["sandbox", "production"]
