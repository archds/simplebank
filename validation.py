from datetime import datetime
from typing import Optional

from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator

import state
from errors import ClientDoesNotExistsError, InsufficientFundsError, InvalidClientNameError, InvalidInputError
from models import Client


class ClientNameValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise InvalidClientNameError(document)


class ClientExistsValidator(ClientNameValidator):
    def validate(self, document):
        super(ClientExistsValidator, self).validate(document)

        if document.text not in state.clients:
            raise ClientDoesNotExistsError(document)

        WithdrawAmountValidator.current_client = state.clients[document.text]


class WithdrawAmountValidator(Validator):
    current_client: Optional[Client] = None

    def validate(self, document: Document):
        try:
            if float(document.text) <= 0:
                raise InvalidInputError(document)
        except Exception:
            raise InvalidInputError(document)

        if self.current_client.account.amount < float(document.text):
            self.current_client = None
            raise InsufficientFundsError


class ISOFormatValidation(Validator):
    def validate(self, document):
        try:
            datetime.fromisoformat(document.text)
        except ValueError:
            raise InvalidInputError(document)
