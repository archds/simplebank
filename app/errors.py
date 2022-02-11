from prompt_toolkit.validation import ValidationError


class BankServiceException(BaseException):
    message = 'Something went wrong!'


class InsufficientFundsError(BankServiceException):
    message = 'Insufficient funds!'


class ClientDoesNotExistsError(BankServiceException):
    message = 'Client does not exists!'


class InvalidInputError(ValidationError):
    def __init__(self, document):
        super(InvalidInputError, self).__init__(
            cursor_position=len(document.text),
            message='Invalid input!'
        )


class InvalidClientNameError(ValidationError):
    def __init__(self, document):
        super(InvalidClientNameError, self).__init__(
            cursor_position=len(document.text),
            message='Invalid client name!'
        )
