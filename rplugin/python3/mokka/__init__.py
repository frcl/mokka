import neovim

import code
import re


@neovim.plugin
class Mokka(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('RunLine')
    def run_line(self, args):
        if self.nvim.current.line.strip().endswith('?'):
            lineno, _ = self.nvim.current.window.cursor
            buf = self.nvim.current.buffer

            # match current indention level and
            # append spaces if last line end with ':'
            spaces = re.match(r'^(\s*)', buf[lineno-2]).group(1)
            spaces += '    ' if buf[lineno-2].strip().endswith(':') else ''

            interpreter = code.InteractiveInterpreter()

            # complie with `pass` appended using precalulated spaces
            compiled = compile('\n'.join(buf[0:lineno-1]+[spaces+'pass']),
                               filename=buf.name,
                               mode='exec')

            interpreter.runcode(compiled)
            status = interpreter.runsource(buf[lineno-1], symbol='eval')
            self.nvim.current.line += str(status)
