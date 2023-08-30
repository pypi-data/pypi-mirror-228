# File generated from our OpenAPI spec by Stainless.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["InboundACHTransfer", "Acceptance", "Decline", "TransferReturn"]


class Acceptance(BaseModel):
    accepted_at: datetime
    """The time at which the transfer was accepted."""

    transaction_id: str
    """The id of the transaction for the accepted transfer."""


class Decline(BaseModel):
    declined_at: datetime
    """The time at which the transfer was declined."""

    declined_transaction_id: str
    """The id of the transaction for the declined transfer."""

    reason: Literal[
        "ach_route_canceled",
        "ach_route_disabled",
        "breaches_limit",
        "credit_entry_refused_by_receiver",
        "duplicate_return",
        "entity_not_active",
        "group_locked",
        "insufficient_funds",
        "misrouted_return",
        "return_of_erroneous_or_reversing_debit",
        "no_ach_route",
        "originator_request",
        "transaction_not_allowed",
        "user_initiated",
    ]
    """The reason for the transfer decline

    - `ach_route_canceled` - The account number is canceled.
    - `ach_route_disabled` - The account number is disabled.
    - `breaches_limit` - The transaction would cause a limit to be exceeded.
    - `credit_entry_refused_by_receiver` - A credit was refused.
    - `duplicate_return` - Other.
    - `entity_not_active` - The account's entity is not active.
    - `group_locked` - Your account is inactive.
    - `insufficient_funds` - Your account contains insufficient funds.
    - `misrouted_return` - Other.
    - `return_of_erroneous_or_reversing_debit` - Other.
    - `no_ach_route` - The account number that was debited does not exist.
    - `originator_request` - Other.
    - `transaction_not_allowed` - The transaction is not allowed per Increase's
      terms.
    - `user_initiated` - The user initiated the decline.
    """


class TransferReturn(BaseModel):
    reason: Literal[
        "authorization_revoked_by_customer",
        "payment_stopped",
        "customer_advised_unauthorized_improper_ineligible_or_incomplete",
        "representative_payee_deceased_or_unable_to_continue_in_that_capacity",
        "beneficiary_or_account_holder_deceased",
        "credit_entry_refused_by_receiver",
        "duplicate_entry",
        "corporate_customer_advised_not_authorized",
    ]
    """The reason for the transfer return

    - `authorization_revoked_by_customer` - The customer no longer authorizes this
      transaction. The Nacha return code is R07.
    - `payment_stopped` - The customer asked for the payment to be stopped. This
      reason is only allowed for debits. The Nacha return code is R08.
    - `customer_advised_unauthorized_improper_ineligible_or_incomplete` - The
      customer advises that the debit was unauthorized. The Nacha return code is
      R10.
    - `representative_payee_deceased_or_unable_to_continue_in_that_capacity` - The
      payee is deceased. The Nacha return code is R14.
    - `beneficiary_or_account_holder_deceased` - The account holder is deceased. The
      Nacha return code is R15.
    - `credit_entry_refused_by_receiver` - The customer refused a credit entry. This
      reason is only allowed for credits. The Nacha return code is R23.
    - `duplicate_entry` - The account holder identified this transaction as a
      duplicate. The Nacha return code is R24.
    - `corporate_customer_advised_not_authorized` - The corporate customer no longer
      authorizes this transaction. The Nacha return code is R29.
    """

    returned_at: datetime
    """The time at which the transfer was returned."""

    transaction_id: str
    """The id of the transaction for the returned transfer."""


class InboundACHTransfer(BaseModel):
    id: str
    """The inbound ach transfer's identifier."""

    acceptance: Optional[Acceptance]
    """If your transfer is accepted, this will contain details of the acceptance."""

    amount: int
    """The transfer amount in USD cents."""

    automatically_resolves_at: datetime
    """The time at which the transfer will be automatically resolved."""

    decline: Optional[Decline]
    """If your transfer is declined, this will contain details of the decline."""

    direction: Literal["credit", "debit"]
    """The direction of the transfer.

    - `credit` - Credit
    - `debit` - Debit
    """

    originator_company_descriptive_date: Optional[str]
    """The descriptive date of the transfer."""

    originator_company_discretionary_data: Optional[str]
    """The additional information included with the transfer."""

    originator_company_entry_description: str
    """The description of the transfer."""

    originator_company_id: str
    """The id of the company that initiated the transfer."""

    originator_company_name: str
    """The name of the company that initiated the transfer."""

    receiver_id_number: Optional[str]
    """The id of the receiver of the transfer."""

    receiver_name: Optional[str]
    """The name of the receiver of the transfer."""

    status: Literal["pending", "declined", "accepted", "returned"]
    """The status of the transfer.

    - `pending` - The Inbound ACH Transfer is awaiting action, will transition
      automatically if no action is taken.
    - `declined` - The Inbound ACH Transfer has been declined.
    - `accepted` - The Inbound ACH Transfer is accepted.
    - `returned` - The Inbound ACH Transfer has been returned.
    """

    trace_number: str
    """The trace number of the transfer."""

    transfer_return: Optional[TransferReturn]
    """If your transfer is returned, this will contain details of the return."""

    type: Literal["inbound_ach_transfer"]
    """A constant representing the object's type.

    For this resource it will always be `inbound_ach_transfer`.
    """
