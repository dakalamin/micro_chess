import sys
import typing

import click


class ProblemTracker:
    def __init__(self, default_error: typing.Type[BaseException]=Exception) -> None:
        self._default_error = default_error
        self.reset()
    
    def reset(self) -> None:
        self._errors_found = 0
        
    def print_error(self, message: str) -> None:
        self._errors_found += 1
        click.secho(message, fg='red')
    
    @classmethod
    def print_warning(cls, message: str) -> None:
        click.secho(message, fg='yellow')
        
    @classmethod
    def raise_without_traceback(cls, error: BaseException) -> typing.NoReturn:
        sys.tracebacklimit = 0
        raise error
        
    def raise_error_if_found(self, message: str) -> None:
        if self._errors_found == 0:
            return
        
        formatted_message = message.format(errors_found=self._errors_found)
        error = self._default_error(formatted_message)
        
        self.raise_without_traceback(error)