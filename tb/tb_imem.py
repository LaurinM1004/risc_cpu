# tb/tb_imem.py
from pathlib import Path
import cocotb
from cocotb.triggers import Timer

def load_hex(path: str) -> list:
    values = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(int(line, 16))
    return values

@cocotb.test()
async def test_imem(dut):
    expected: list = load_hex(Path(__file__).parent / "imem.hex")

    for index, exp_instr in enumerate(expected):
        byte_addr = index * 4
        dut.addr.value = byte_addr
        await Timer(1, unit="ns")
        assert int(dut.instr.value) == exp_instr, f"Instr at index {index} is false"

    byte_addr = 4 * 256
    dut.addr.value = byte_addr
    await Timer(1, unit="ns")
    assert int(dut.instr.value) == expected[0], f"Instr at index 0 is false after wraparound, got {int(dut.instr.value):#x}"