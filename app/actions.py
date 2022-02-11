from datetime import datetime

from terminaltables import AsciiTable

import state
from models import BankOperation, BankOperationType, Client, Currency

__all__ = [
    'deposit',
    'withdraw',
    'show_bank_statement'
]


def deposit(client: str, amount: float, description: str) -> None:
    if client not in state.clients:
        state.clients[client] = Client(name=client)

    state.operations.append(
        BankOperation(
            type=BankOperationType.deposit,
            client=state.clients[client],
            amount=amount,
            description=description
        )
    )

    state.clients[client].account.amount += amount


def withdraw(client: str, amount: float, description: str) -> None:
    if client not in state.clients:
        raise ValueError(f'Client {client} do not have an account!')

    state.operations.append(
        BankOperation(
            type=BankOperationType.withdraw,
            client=state.clients[client],
            amount=amount,
            description=description
        )
    )

    state.clients[client].account.amount -= amount


def get_previous_balance(operation: BankOperation) -> float:
    client_ops = [
        op for op in state.operations
        if op.client.name == operation.client.name
    ]

    op_index = client_ops.index(operation)

    if op_index == 0:
        return 0
    else:
        return state.operations[op_index - 1].current_balance


def format_currency(value: float, currency: Currency, default: str = None) -> str:
    currency_map = {
        Currency.USD: '$'
    }

    if value:
        return f'{currency_map[currency]}{round(value, 2)}'

    return default or ''


def show_bank_statement(client: str, since: datetime, till: datetime) -> None:
    selected_ops = [
        op for op in state.operations
        if op.client.name == client and since <= op.date <= till
    ]

    if len(selected_ops) == 0:
        print('No transactions during this time')
        return

    table = []
    table_header = ['Date', 'Description', 'Withdrawals', 'Deposits', 'Balance']
    table_content = [
        [
            operation.date.strftime("%Y-%m-%d %H:%M:%S"),
            operation.description,
            format_currency(operation.withdraw_amount, operation.client.account.currency),
            format_currency(operation.deposit_amount, operation.client.account.currency),
            format_currency(operation.current_balance, operation.client.account.currency)
        ]
        for operation in selected_ops
    ]
    table.append(table_header)
    table.append(
        [
            '',
            'Previous balance',
            '',
            '',
            format_currency(get_previous_balance(selected_ops[0]), selected_ops[0].client.account.currency, '$0.0')
        ]
    )
    table.append(['' for _ in range(5)])
    table.extend(table_content)
    table.append(
        [
            '',
            'Totals',
            sum(op.amount for op in selected_ops if op.type == BankOperationType.withdraw),
            sum(op.amount for op in selected_ops if op.type == BankOperationType.deposit),
            format_currency(selected_ops[-1].current_balance, selected_ops[-1].client.account.currency)
        ]
    )

    table = AsciiTable(table)
    table.inner_footing_row_border = True

    print(table.table)
