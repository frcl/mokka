import ast
from .interpreter import Interpreter


class Wrapper(object):
    """
    wrapper around Interpreter that parses the source and aranges for special
    syntax elements like assignments, for loops and with statements to be
    evaluated in a specific sence
    """
    ignored_tokens = ('import', 'def', 'for', 'with')

    def __init__(self, buf) -> None:
        self.filename = buf.name
        self.buf = buf # TODO: is this necessary?

        try:
            self.ast = ast.parse('\n'.join(buf))
            self.msg = None
        except SyntaxError as exc:
            self.ast = None
            self.msg = self._format_exc(exc)

    def _format_exc(self, exc: Exception) -> str:
        if isinstance(exc, SyntaxError):
            # text = exc.text.replace("\n", "")
            # return ('{0.__class__.__name__}: {1}, line {0.lineno}'
                    # .format(exc, text))
            return '{0.__class__.__name__}, line {0.lineno}'.format(exc)

        return '{0.__class__.__name__}: {0}'.format(exc)

    def _format_value(self, value: object) -> str:
        return repr(value).replace('\n', '')

    def eval_line(self, number: int) -> object:
        """
        Evaluate a line by number

        Arguments:
        - number: int
            number of line to evaluate

        Returns:
        - result of evaluating the line
        """

        if self.ast:
            interpreter = Interpreter(self.filename)

            cur_line = self.buf[number-1].strip()
            if (not cur_line) or any(cur_line.startswith(token)
                                     for token in self.ignored_tokens):
                raise ValueError()

            # constuction area:
            # =================
            pre_nodes = []

            def find_cur_node(node):
                if hasattr(node, 'lineno') and node.lineno == number:
                    return node

                if hasattr(node, 'body'):
                    for subn in node.body:
                        if subn.lineno > number:
                            break
                        pre_nodes.append(subn)
                        nextn = subn
                else:
                    return None

                pre_nodes.pop()
                return find_cur_node(nextn)

            node = find_cur_node(self.ast)

            compiled = interpreter.compile(ast.Module(pre_nodes), 'exec')
            interpreter.exec_code(compiled)

            if isinstance(node, ast.If):
                source = node.test
            else:
                source = node.value

            compiled = interpreter.compile(ast.Expression(source), 'eval')
            value = interpreter.eval_code(compiled)
            # =================

            return self._format_value(value)
        else:
            return self.msg

    def eval_range(self, start: int, end: int) -> object:
        """
        experimental
        """
        pass
