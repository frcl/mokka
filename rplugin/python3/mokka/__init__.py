import re

import neovim
from .interpreter import Interpreter


@neovim.plugin
class Mokka(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('RunLine')
    def run_line(self, args):
        lineno, _ = self.nvim.current.window.cursor
        buf = self.nvim.current.buffer

        # match current indention level and
        # append spaces if last line end with ':'
        spaces = re.match(r'^(\s*)', buf[lineno-2]).group(1)
        spaces += '    ' if buf[lineno-2].strip().endswith(':') else ''

        interpreter = Interpreter(filename=buf.name)

        # run with `pass` appended using precalulated spaces
        source = '\n'.join(buf[0:lineno-1]+[spaces+'pass'])

        if interpreter.exec(source):
            pass # TODO: show traceback
        else:
            value = interpreter.eval(buf[lineno-1])
            rep = str(value).replace('\n', '')
            if len(rep) > 32:
                rep = rep[:29]+'...'
            buf[lineno-1] = buf[lineno-1] + ' # ' + rep
