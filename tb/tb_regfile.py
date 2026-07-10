# tb/tb_regfile.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.rd_write_enable.value = 0
    dut.rd_addr.value = 0
    dut.rd_data.value = 0
    dut.rs1_addr.value = 0
    dut.rs2_addr.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await Timer(1, unit="ns")

async def write_reg(dut, addr, data):
    dut.rd_addr.value = addr
    dut.rd_data.value = data
    dut.rd_write_enable.value = 1
    await Timer(1, unit="ns")
    await RisingEdge(dut.clk)
    dut.rd_write_enable.value = 0
    await Timer(1, unit="ns")

@cocotb.test()
async def test_regfile(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)


    dut.rs1_addr.value = 1
    dut.rs2_addr.value = 2
    await Timer(1, unit="ns")
    assert int(dut.rs1_data.value) == 0, f"Expected rs1_data to be 0 after reset, got {int(dut.rs1_data.value)}"
    assert int(dut.rs2_data.value) == 0, f"Expected rs2_data to be 0 after reset, got {int(dut.rs2_data.value)}"


    await write_reg(dut, addr=5, data=420)
    dut.rs1_addr.value = 5
    await Timer(1, unit="ns")
    assert int(dut.rs1_data.value) == 420, f"Expected rs1_data to be 420, got {int(dut.rs1_data.value)}"


    await write_reg(dut, addr=0, data=0xDEADBEEF)  # Versuch, x0 zu überschreiben
    dut.rs1_addr.value = 0
    await Timer(1, unit="ns")
    assert int(dut.rs1_data.value) == 0, f"x0 has to be always 0, got {int(dut.rs1_data.value)}"


    await write_reg(dut, addr=10, data=0x1111)
    await write_reg(dut, addr=20, data=0x2222)
    dut.rs1_addr.value = 10
    dut.rs2_addr.value = 20
    await Timer(1, unit="ns")
    assert ((dut.rs1_data.value == 0x1111) and (dut.rs2_data.value == 0x2222)), f"read the wrong values, got {int(dut.rs1_data.value)} and {int(dut.rs2_data.value)}"