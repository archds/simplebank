from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, confloat, constr, root_validator


class Currency(Enum):
    USD = 0


class Account(BaseModel):
    currency: Currency = Currency.USD
    amount: confloat(ge=0) = 0


class Client(BaseModel):
    name: constr(strip_whitespace=True)
    account: Account = Account()


class BankOperationType(Enum):
    deposit = 0
    withdraw = 1


class BankOperation(BaseModel):
    type: BankOperationType
    client: Client
    amount: confloat(ge=0)
    currency: Currency = Currency.USD
    description: constr(strip_whitespace=True)
    date: datetime = Field(default_factory=datetime.now)
    current_balance: Optional[confloat(ge=0)]

    @root_validator
    def calculate_current_balance(cls, values):
        if values['type'] == BankOperationType.deposit:
            values['current_balance'] = values['client'].account.amount + values['amount']

        if values['type'] == BankOperationType.withdraw:
            values['current_balance'] = values['client'].account.amount - values['amount']

        return values

    @property
    def deposit_amount(self) -> float:
        if self.type == BankOperationType.deposit:
            return self.amount

        return 0.0

    @property
    def withdraw_amount(self) -> float:
        if self.type == BankOperationType.withdraw:
            return self.amount

        return 0.0
