# pylint: disable=eval-used,exec-used,broad-except
import types
import ast
from typing import Optional, Union, Tuple


class Interpreter(object):
    """
    Class that emulates a seperate python interpreter, similar to the ones in
    the `code` module, but non interactive.
    """

    def __init__(self, filename: str) -> None:
        self.locals = {'__name__': '__console__', '__doc__': None}
        self.filename = filename

    def compile(self, source: Union[ast.AST, str], mode: str) -> types.CodeType:
        """
        Wrapper around builtin compile function.

        Arguments:
        - source: str
            source to compile
        - mode: {'exec', 'eval'}
            for what method zu compile

        Returns:
        - code object
        """
        return compile(source, self.filename, mode, dont_inherit=True)

    def eval(self, source: str) -> Tuple[Optional[object],
                                         Optional[Exception]]:
        """
        Evaluate an expression in the context of the virtual interpreter.

        Returns:
        - the object resulting from evaluation if the expression is valid
        - an exception if there is a SyntaxError, ValueError or OverflowError
        """

        try:
            code = self.compile(source, 'eval'), None
        except (OverflowError, SyntaxError, ValueError) as exc:
            return None, exc

        return self.eval_code(code)

    def eval_code(self, code: types.CodeType) -> Tuple[Optional[object],
                                                       Optional[Exception]]:
        """
        Evaluate a compiled expression in the context of the virtual
        interpreter.

        Returns:
        - the object resulting from evaluation if the expression is valid
        """
        try:
            return eval(code, self.locals), None
        except Exception as exc:
            return None, exc

    def exec(self, source: str) -> Optional[Exception]:
        """
        Execute the source inside the virtual interpreter.

        Returns:
        - None if the execution was sucessfull
        - an exception if there is a SyntaxError, ValueError or OverflowError
        """

        try:
            code = self.compile(source, 'exec')
        except (OverflowError, SyntaxError, ValueError) as exc:
            return exc

        return self.exec_code(code)

    def exec_code(self, code: types.CodeType) -> Optional[Exception]:
        """
        Execute the source inside the virtual interpreter.

        Returns:
        - None if the execution was sucessfull
        - an exception if there is a SyntaxError, ValueError or OverflowError
        """
        try:
            exec(code, self.locals)
        except Exception as exc:
            return exc
        else:
            return None
