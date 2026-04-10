from freedon_lang import pipeline
from freedon_lang.runner import run_source


def test_line_frontend_directive_parses_and_runs() -> None:
    pipeline.set_exec_mode("interp")
    pipeline.set_ir_target(0)
    pipeline.set_frontend("lisp")  # should be overridden by directive

    src = """#!frontend line
print "ok"
"""
    # print returns None, last form => None
    assert run_source(src) is None


def test_line_frontend_allows_parenthesized_subcalls() -> None:
    pipeline.set_exec_mode("interp")
    pipeline.set_ir_target(0)
    src = """#!frontend line
poke 1 7 "ram"
print (peek 1 "ram")
"""
    assert run_source(src) is None

