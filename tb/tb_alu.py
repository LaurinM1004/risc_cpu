# tb/test_alu.py
import random
import cocotb
from cocotb.triggers import Timer

# Spiegel von alu_op_e — Reihenfolge MUSS zum Package passen
ALU = {"SLL":0,"SLT":1,"SLTU":2,"XOR":3,"OR":4,
       "AND":5,"SRL":6,"SRA":7,"SUB":8,"ADD":9}
MASK = (1 << 32) - 1
def to_signed(x):
    return x - (1 << 32) if (x & 0x80000000) else x

def reference_model(op, a, b):
    if op == "SLL":
        res = (a << (b & 0x1F)) & MASK
    elif op == "SLT":
        res = int(to_signed(a) < to_signed(b))
    elif op == "SLTU":
        res = int(a < b)
    elif op == "XOR":
        res = a ^ b
    elif op == "OR":
        res = a | b
    elif op == "AND":
        res = a & b
    elif op == "SRL":
        res = (a >> (b & 0x1F)) & MASK
    elif op == "SRA":
        res = (to_signed(a) >> (b & 0x1F)) & MASK
    elif op == "SUB":
        res = (a - b) & MASK
    elif op == "ADD":
        res = (a + b) & MASK
    else:
        raise ValueError(f"Unknown ALU operation: {op}")
    return res, int(res == 0)

@cocotb.test()
async def test_alu_random(dut):
    for _ in range(1000):
        name, opval = random.choice(list(ALU.items()))
        a, b = random.randint(0, MASK), random.randint(0, MASK)
        dut.data_in_1.value = a
        dut.data_in_2.value = b
        dut.alu_op.value = opval
        await Timer(1, "ns")
        exp_res, exp_zero = reference_model(name, a, b)
        assert int(dut.alu_out.value) == exp_res, f"{name}: {a},{b}"
        assert int(dut.zero.value) == exp_zero