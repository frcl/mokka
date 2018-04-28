import re

import neovim
from .wrapper import Wrapper


@neovim.plugin
class Mokka(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('EvalLine')
    def eval_line(self, args):
        lineno, _ = self.nvim.current.window.cursor
        buf = self.nvim.current.buffer
        interpreter = Interpreter(filename=buf.name)
        value = interpreter.eval(buf[lineno-1])
        rep = str(value).replace('\n', '')
        if len(rep) > 32:
            rep = rep[:29]+'...'
        buf[lineno-1] = buf[lineno-1] + ' # ' + rep

    @neovim.function('EvalUntilCurrent')
    def eval_until_current(self, args):
        lineno, _ = self.nvim.current.window.cursor
        buf = self.nvim.current.buffer

        wrapper = Wrapper(buf)

        try:
            rep = wrapper.eval_line(lineno)
        except ValueError:
            return

        maxlen = 64
        short = rep[:maxlen-3] + '...' if len(rep) > maxlen else rep
        # TODO: get window width for dynamic lenght

        buf[lineno-1] = buf[lineno-1] + ' # ' + short
