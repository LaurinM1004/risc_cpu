# tb/tb_decode_stage.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

# Opcode-Werte aus deinem opcode_e Enum (zur Kontrolle in den Assertions)
OPCODE_OP     = 0b0110011  # R-Type (add, sub)
OPCODE_OP_IMM = 0b0010011  # I-Type (addi)

async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.rd_write_enable.value = 0
    dut.rd_addr.value = 0
    dut.rd_data.value = 0
    dut.instr.value = 0
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
async def test_decode_stage(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    # --- Scenario 1: addi x1, x0, 5  ==  0x00500093 ---
    dut.instr.value = 0x00500093
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == OPCODE_OP_IMM, f"Expected opcode {OPCODE_OP_IMM}, got {int(dut.opcode.value)}"
    assert int(dut.rd_addr.value) == 1, f"Expected rd_addr 1, got {int(dut.rd_addr.value)}"
    assert int(dut.funct3.value) == 0, f"Expected funct3 0, got {int(dut.funct3.value)}"
    assert int(dut.imm.value) == 5, f"Expected imm 5, got {int(dut.imm.value)}"

    # --- Scenario 2: add x3, x1, x2  ==  0x002081B3 ---
    dut.instr.value = 0x002081B3
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == OPCODE_OP, f"Expected opcode {OPCODE_OP}, got {int(dut.opcode.value)}"
    assert int(dut.rd_addr.value) == 3, f"Expected rd_addr 3, got {int(dut.rd_addr.value)}"
    assert int(dut.funct3.value) == 0, f"Expected funct3 0, got {int(dut.funct3.value)}"
    assert int(dut.funct7.value) == 0, f"Expected funct7 0, got {int(dut.funct7.value)}"

    # --- Scenario 3: sub x4, x3, x1  ==  0x40118233 ---
    dut.instr.value = 0x40118233
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == OPCODE_OP, f"Expected opcode {OPCODE_OP}, got {int(dut.opcode.value)}"
    assert int(dut.rd_addr.value) == 4, f"Expected rd_addr 4, got {int(dut.rd_addr.value)}"
    assert int(dut.funct3.value) == 0, f"Expected funct3 0, got {int(dut.funct3.value)}"
    assert int(dut.funct7.value) == 0b0100000, f"Expected funct7 0b0100000, got {int(dut.funct7.value)}"

    # --- Scenario 4: test negativ immediate (Sign-Extension) ---
    # addi x1, x0, -1
    dut.instr.value = 0xFFF00093  # addi x1, x0, -1
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == OPCODE_OP_IMM, f"Expected opcode {OPCODE_OP_IMM}, got {int(dut.opcode.value)}"
    assert int(dut.rd_addr.value) == 1, f"Expected rd_addr 1, got {int(dut.rd_addr.value)}"
    assert int(dut.imm.value) == 0xFFFFFFFF, f"Expected imm 0xFFFFFFFF (sign-extended -1), got {int(dut.imm.value)}"


    # --- Scenario 5: Regfile-Integration (Decode + eingebettetes regfile) ---
    await write_reg(dut, addr=1, data=0xCAFE)
    dut.instr.value = 0x00508113  # addi x2, x1, 5 -> rs1 = x1
    await Timer(1, unit="ns")
    assert int(dut.rs1_addr.value) == 1, f"Expected rs1_addr 1, got {int(dut.rs1_addr.value)}"
    assert int(dut.rs1_data.value) == 0xCAFE, f"Expected rs1_data 0xCAFE, got {int(dut.rs1_data.value)}"