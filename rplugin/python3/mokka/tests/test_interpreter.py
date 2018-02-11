import sys
import pytest
from mokka.interpreter import Interpreter


@pytest.fixture
def interpreter():
    return Interpreter('test.py')


def test_simple_eval(interpreter):
    assert interpreter.eval('1+1') == 2


def test_local_access(interpreter):
    interpreter.exec('x=1')
    assert interpreter.eval('x+1') == 2


def test_function_import_access(interpreter):
    interpreter.exec('import sys\n'
                     'def test():\n'
                     '    print(locals())\n'
                     '    return sys.version')
    assert interpreter.eval('test()') == sys.version
