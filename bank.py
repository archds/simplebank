import functools as fc
import sys
from datetime import datetime

from PyInquirer import prompt

import actions
from errors import BankServiceException
from validation import ClientExistsValidator, ClientNameValidator, ISOFormatValidation, WithdrawAmountValidator

tell = fc.partial(print, end='\n\n')

commands = {
    'Deposit': {
        'action': actions.deposit,
        'args': [
            {
                'type': 'input',
                'name': 'client',
                'message': 'Enter the client name:',
                'validate': ClientNameValidator
            },
            {
                'type': 'input',
                'name': 'amount',
                'message': 'Amount:',
                'validate': lambda val: float(val) > 0,
                'filter': lambda val: float(val)
            },
            {
                'type': 'input',
                'name': 'description',
                'message': 'Operation description:',
                'validate': lambda val: bool(val)
            }
        ]
    },
    'Withdraw': {
        'action': actions.withdraw,
        'args': [
            {
                'type': 'input',
                'name': 'client',
                'message': 'Enter the client name:',
                'validate': ClientExistsValidator
            },
            {
                'type': 'input',
                'name': 'amount',
                'message': 'Amount:',
                'filter': lambda val: float(val),
                'validate': WithdrawAmountValidator
            },
            {
                'type': 'input',
                'name': 'description',
                'message': 'Operation description:',
                'validate': lambda val: bool(val)
            }
        ]
    },
    'Show bank statement': {
        'action': actions.show_bank_statement,
        'args': [
            {
                'type': 'input',
                'name': 'client',
                'message': 'Enter the client name:',
                'validate': ClientExistsValidator
            },
            {
                'type': 'input',
                'name': 'since',
                'message': 'Since:',
                'validate': ISOFormatValidation,
                'filter': lambda val: datetime.fromisoformat(val)
            },
            {
                'type': 'input',
                'name': 'till',
                'message': 'Till:',
                'validate': ISOFormatValidation,
                'filter': lambda val: datetime.fromisoformat(val)
            },
        ]
    },
    'Exit': {
        'action': sys.exit,
        'args': []
    }
}


def _command_handler():
    initial_variants = [
        {
            'type': 'list',
            'name': 'command',
            'message': 'Choose action',
            'choices': [command for command in commands]
        }
    ]

    command = prompt(initial_variants)['command']
    commands[command]['action'](**prompt(commands[command]['args']))


if __name__ == '__main__':
    tell('Service started!', end='\n\n')

    while True:
        try:
            _command_handler()
        except (EOFError, KeyboardInterrupt, KeyError):
            sys.exit()
        except TypeError as err:
            pass
        except BankServiceException as err:
            tell(err.message)
        # except Exception as err:
        #     tell('Something went wrong!')
