# tb/runner.py
import os
from pathlib import Path
from cocotb_tools.runner import get_runner

hex_path = Path(__file__).parent / "imem.hex"

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


def test_imem_runner():
    root = Path(__file__).resolve().parents[1]

    runner = get_runner("verilator")
    runner.build(
        sources=[
            root / "src" / "pkg" / "riscv_pkg.sv",
            root / "src" / "mem" / "imem.sv",
        ],
        parameters={"MEM_INIT_FILE": f'"{hex_path}"'},
        hdl_toplevel="imem",
    )
    runner.test(hdl_toplevel="imem", test_module="tb_imem")


def test_regfile_runner():
    root = Path(__file__).resolve().parents[1]

    runner = get_runner("verilator")
    runner.build(
        sources=[
            root / "src" / "pkg" / "riscv_pkg.sv",
            root / "src" / "core" / "decode" / "regfile.sv",
        ],
        hdl_toplevel="regfile",
    )
    runner.test(hdl_toplevel="regfile", test_module="tb_regfile")


def test_decode_stage_runner():
    root = Path(__file__).resolve().parents[1]

    runner = get_runner("verilator")
    runner.build(
        sources=[
            root / "src" / "pkg" / "riscv_pkg.sv",
            root / "src" / "core" / "decode" / "regfile.sv",
            root / "src" / "core" / "decode" / "decode_stage.sv",
        ],
        hdl_toplevel="decode_stage",
    )
    runner.test(hdl_toplevel="decode_stage", test_module="tb_decode_stage")

