" Mokka - Python Code Evaluation Plugin

python3 import vim

func! RunLine()
" start python script
    python3 << EOF
local_pyvars = {}
global_pyvars = {'__name__': '__main__'}
cw = vim.current.window
cb = vim.current.buffer

line, _ = cw.cursor
try:
    exec('\n'.join(cb[0:line-1]), global_pyvars, local_pyvars)
except Exception as e:
    print('ERROR:', e)
else:
    try:
        print(eval(cb[line-1], global_pyvars, local_pyvars))
    except Exception as e:
        print('ERROR:', e)
EOF
" end python script
endfunc

func! RunLine2()
    python3 << EOF
import code
import re
clno, _ = vim.current.window.cursor
cb = vim.current.buffer
spaces_last = re.match(r'^(\s*)', cb[clno-2]).group(1)
interpreter = code.InteractiveInterpreter()
compiled = compile('\n'.join(cb[0:clno-1]+[spaces_last+'pass']),
                   filename=cb.name,
                   mode='exec')
#for line in cb[0:clno]:
#    interpreter.runsource(line)
interpreter.runcode(compiled)
interpreter.runsource(cb[clno-1])
EOF
endfunc


nnoremap <leader>rl :call RunLine2()<cr>
