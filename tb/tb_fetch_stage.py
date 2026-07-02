# tb/tb_fetch_stage.py
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

PC_RESET_VALUE = 0x0000_0000  # has to fit to localparam

async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.take_jump.value = 0
    dut.jump_target.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await Timer(1, unit="ns")


@cocotb.test()
async def test_fetch_stage(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)


    assert int(dut.pc_out.value) == PC_RESET_VALUE, f"PC should be {PC_RESET_VALUE:#x} after reset, but is {int(dut.pc_out.value):#x}"


    expected_pc = PC_RESET_VALUE
    await RisingEdge(dut.clk)
    for i in range(50):
        await RisingEdge(dut.clk)
        expected_pc = (expected_pc + 4) & 0xFFFF_FFFF
        assert int(dut.pc_out.value) == expected_pc, f"PC should be {expected_pc:#x} after {i+1} cycles, but is {int(dut.pc_out.value):#x}"


    dut.take_jump.value = 1
    for i in range(5):
        jump_target = random.randint(0, 0xFFFF_FFFF)
        dut.jump_target.value = jump_target
        expected_pc = jump_target
        await Timer(1, unit="ns")  # wait for combinational logic to settle
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        assert int(dut.pc_out.value) == expected_pc, f"PC should be {expected_pc:#x} but is {int(dut.pc_out.value):#x}"


    dut.take_jump.value = 0
    for i in range(5):
        jump_target = 0xABAB_ABAB
        dut.jump_target.value = jump_target
        expected_pc = (expected_pc + 4) & 0xFFFF_FFFF
        await Timer(1, unit="ns")  # wait for combinational logic to settle
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        assert int(dut.pc_out.value) == expected_pc, f"PC should be {expected_pc:#x} after {i+1} cycles, but is {int(dut.pc_out.value):#x}"
