from typing import Optional, Union


class Interpreter(object):
    """
    Class that emulates a seperate python interpreter, similar to the ones in
    the `code` module, but non interactive.
    """

    def __init__(self, filename: str):
        self.locals = {'__name__': '__console__', '__doc__': None}
        self.filename = filename

    def compile(self, source: str, mode: str):
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

    def eval(self, source: str) -> object:
        """
        Evaluate an expression in the context of the virtual interpreter.

        Returns:
        - the object resulting from evaluation if the expression is valid
        - an exception if there is a SyntaxError, ValueError or OverflowError
        """

        try:
            code = self.compile(source, 'eval')
        except (OverflowError, SyntaxError, ValueError) as exc:
            return exc

        return eval(code, self.locals)

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

        exec(code, self.locals)
        return None
