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

nnoremap <leader>rl :call RunLine()<cr>
