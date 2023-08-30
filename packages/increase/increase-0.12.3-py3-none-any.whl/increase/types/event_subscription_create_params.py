# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["EventSubscriptionCreateParams"]


class EventSubscriptionCreateParams(TypedDict, total=False):
    url: Required[str]
    """The URL you'd like us to send webhooks to."""

    selected_event_category: Literal[
        "account.created",
        "account.updated",
        "account_number.created",
        "account_number.updated",
        "account_statement.created",
        "account_transfer.created",
        "account_transfer.updated",
        "ach_prenotification.created",
        "ach_prenotification.updated",
        "ach_transfer.created",
        "ach_transfer.updated",
        "card.created",
        "card.updated",
        "card_payment.created",
        "card_payment.updated",
        "card_dispute.created",
        "card_dispute.updated",
        "check_deposit.created",
        "check_deposit.updated",
        "check_transfer.created",
        "check_transfer.updated",
        "declined_transaction.created",
        "digital_wallet_token.created",
        "digital_wallet_token.updated",
        "document.created",
        "entity.created",
        "entity.updated",
        "external_account.created",
        "file.created",
        "group.updated",
        "group.heartbeat",
        "inbound_ach_transfer.created",
        "inbound_ach_transfer.updated",
        "inbound_ach_transfer_return.created",
        "inbound_ach_transfer_return.updated",
        "inbound_wire_drawdown_request.created",
        "oauth_connection.created",
        "oauth_connection.deactivated",
        "pending_transaction.created",
        "pending_transaction.updated",
        "real_time_decision.card_authorization_requested",
        "real_time_decision.digital_wallet_token_requested",
        "real_time_decision.digital_wallet_authentication_requested",
        "real_time_payments_transfer.created",
        "real_time_payments_transfer.updated",
        "real_time_payments_request_for_payment.created",
        "real_time_payments_request_for_payment.updated",
        "transaction.created",
        "wire_drawdown_request.created",
        "wire_drawdown_request.updated",
        "wire_transfer.created",
        "wire_transfer.updated",
    ]
    """
    If specified, this subscription will only receive webhooks for Events with the
    specified `category`.

    - `account.created` - Occurs whenever an Account is created.
    - `account.updated` - Occurs whenever an Account is updated.
    - `account_number.created` - Occurs whenever an Account Number is created.
    - `account_number.updated` - Occurs whenever an Account Number is updated.
    - `account_statement.created` - Occurs whenever an Account Statement is created.
    - `account_transfer.created` - Occurs whenever an Account Transfer is created.
    - `account_transfer.updated` - Occurs whenever an Account Transfer is updated.
    - `ach_prenotification.created` - Occurs whenever an ACH Prenotification is
      created.
    - `ach_prenotification.updated` - Occurs whenever an ACH Prenotification is
      updated.
    - `ach_transfer.created` - Occurs whenever an ACH Transfer is created.
    - `ach_transfer.updated` - Occurs whenever an ACH Transfer is updated.
    - `card.created` - Occurs whenever a Card is created.
    - `card.updated` - Occurs whenever a Card is updated.
    - `card_payment.created` - Occurs whenever a Card Payment is created.
    - `card_payment.updated` - Occurs whenever a Card Payment is updated.
    - `card_dispute.created` - Occurs whenever a Card Dispute is created.
    - `card_dispute.updated` - Occurs whenever a Card Dispute is updated.
    - `check_deposit.created` - Occurs whenever a Check Deposit is created.
    - `check_deposit.updated` - Occurs whenever a Check Deposit is updated.
    - `check_transfer.created` - Occurs whenever a Check Transfer is created.
    - `check_transfer.updated` - Occurs whenever a Check Transfer is updated.
    - `declined_transaction.created` - Occurs whenever a Declined Transaction is
      created.
    - `digital_wallet_token.created` - Occurs whenever a Digital Wallet Token is
      created.
    - `digital_wallet_token.updated` - Occurs whenever a Digital Wallet Token is
      updated.
    - `document.created` - Occurs whenever a Document is created.
    - `entity.created` - Occurs whenever an Entity is created.
    - `entity.updated` - Occurs whenever an Entity is updated.
    - `external_account.created` - Occurs whenever an External Account is created.
    - `file.created` - Occurs whenever a File is created.
    - `group.updated` - Occurs whenever a Group is updated.
    - `group.heartbeat` - Increase may send webhooks with this category to see if a
      webhook endpoint is working properly.
    - `inbound_ach_transfer.created` - Occurs whenever an Inbound ACH Transfer is
      created.
    - `inbound_ach_transfer.updated` - Occurs whenever an Inbound ACH Transfer is
      updated.
    - `inbound_ach_transfer_return.created` - Occurs whenever an Inbound ACH
      Transfer Return is created.
    - `inbound_ach_transfer_return.updated` - Occurs whenever an Inbound ACH
      Transfer Return is updated.
    - `inbound_wire_drawdown_request.created` - Occurs whenever an Inbound Wire
      Drawdown Request is created.
    - `oauth_connection.created` - Occurs whenever an OAuth Connection is created.
    - `oauth_connection.deactivated` - Occurs whenever an OAuth Connection is
      deactivated.
    - `pending_transaction.created` - Occurs whenever a Pending Transaction is
      created.
    - `pending_transaction.updated` - Occurs whenever a Pending Transaction is
      updated.
    - `real_time_decision.card_authorization_requested` - Occurs whenever a
      Real-Time Decision is created in response to a card authorization.
    - `real_time_decision.digital_wallet_token_requested` - Occurs whenever a
      Real-Time Decision is created in response to a digital wallet provisioning
      attempt.
    - `real_time_decision.digital_wallet_authentication_requested` - Occurs whenever
      a Real-Time Decision is created in response to a digital wallet requiring
      two-factor authentication.
    - `real_time_payments_transfer.created` - Occurs whenever a Real-Time Payments
      Transfer is created.
    - `real_time_payments_transfer.updated` - Occurs whenever a Real-Time Payments
      Transfer is updated.
    - `real_time_payments_request_for_payment.created` - Occurs whenever a Real-Time
      Payments Request for Payment is created.
    - `real_time_payments_request_for_payment.updated` - Occurs whenever a Real-Time
      Payments Request for Payment is updated.
    - `transaction.created` - Occurs whenever a Transaction is created.
    - `wire_drawdown_request.created` - Occurs whenever a Wire Drawdown Request is
      created.
    - `wire_drawdown_request.updated` - Occurs whenever a Wire Drawdown Request is
      updated.
    - `wire_transfer.created` - Occurs whenever a Wire Transfer is created.
    - `wire_transfer.updated` - Occurs whenever a Wire Transfer is updated.
    """

    shared_secret: str
    """The key that will be used to sign webhooks.

    If no value is passed, a random string will be used as default.
    """
