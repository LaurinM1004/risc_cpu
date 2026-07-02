# tb/runner.py
import os
from pathlib import Path
from cocotb_tools.runner import get_runner



def test_alu():
    root = Path(__file__).resolve().parents[1]
    runner = get_runner("verilator")
    runner.build(
        sources=[root / "src/pkg/riscv_pkg.sv",      # Package zuerst!
                 root / "src/core/execute/alu.sv"],
        hdl_toplevel="alu",
    )
    runner.test(hdl_toplevel="alu", test_module="tb_alu")


def test_fetch_stage_runner():
    root = Path(__file__).resolve().parents[1]

    runner = get_runner("verilator")
    runner.build(
        sources=[
            root / "src" / "pkg" / "riscv_pkg.sv",
            root / "src" / "core" / "fetch" / "pc_reg.sv",
            root / "src" / "core" / "fetch" / "fetch_stage.sv",
        ],
        hdl_toplevel="fetch_stage",
    )
    runner.test(hdl_toplevel="fetch_stage", test_module="tb_fetch_stage")
