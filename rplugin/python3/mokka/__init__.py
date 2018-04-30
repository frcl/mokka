import re

import neovim
from .wrapper import Wrapper


@neovim.plugin
class Mokka(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('EvalUntilCurrent')
    def eval_until_current(self, args):
        lineno, _ = self.nvim.current.window.cursor
        buf = self.nvim.current.buffer

        wrapper = Wrapper(buf)

        try:
            rep = wrapper.eval_line(lineno)
        except ValueError:
            return

        # this needs serious fixing
        self.nvim.command(
            'redir =>a |exe "sil sign place buffer=".bufnr(\'\')|redir end'
        )
        self.nvim.command("let signlist=split(a, '\\n')")
        winwidth = self.nvim.current.window.width
        textwidth = winwidth - self.nvim.eval(
            '((&number||&relativenumber) ? &numberwidth : 0)'
            ' + &foldcolumn + (len(signlist) > 2 ? 2 : 0)'
        )
        maxlen = textwidth - len(buf[lineno-1]) - 3
        # maxlen = self.nvim.current.window.width - len(buf[lineno-1])
        short = rep[:maxlen-3] + '...' if len(rep) > maxlen else rep
        # TODO: get window width for dynamic lenght

        buf[lineno-1] = buf[lineno-1] + ' # ' + short
