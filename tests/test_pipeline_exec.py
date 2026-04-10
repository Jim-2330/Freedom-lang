from freedon_lang import pipeline
from freedon_lang.runner import run_source


def _reset_pipeline() -> None:
    pipeline.set_frontend("lisp")
    pipeline.set_exec_mode("interp")
    pipeline.set_ir_target(0)


def test_compile_ir2_runs_basic_arith() -> None:
    _reset_pipeline()
    pipeline.set_exec_mode("compile")
    pipeline.set_ir_target(2)
    out = run_source("(+ 1 2)")
    assert out == 3


def test_mixed_mode_falls_back_to_interp_on_compile_error() -> None:
    _reset_pipeline()
    pipeline.set_exec_mode("mixed")
    pipeline.set_ir_target(2)
    # fn 编译支持，但这里构造一个会触发 VM 栈检查差异的场景：空 do
    out = run_source("(do)")
    assert out is None

