import riscv_pkg::*;

module decode_stage (
    input logic clk,
    input logic rst_n,

    input word_t instr,

    output opcode_e opcode,
    output logic[2:0] funct3,
    output logic[6:0] funct7,
    output word_t imm,

    output word_t rs1_data,
    output word_t rs2_data,

    output reg_addr_t rd_addr,
    input word_t rd_data,
    input logic rd_write_enable
);

    reg_addr_t rs1_addr,rs2_addr;

    assign opcode = opcode_e'(instr[6:0]);
    assign rd_addr     = instr[11:7];
    assign funct3 = instr[14:12];
    assign rs1_addr    = instr[19:15];
    assign rs2_addr    = instr[24:20];
    assign funct7 = instr[31:25];
    assign imm = { {20{instr[31]}}, instr[31:20] };
    regfile i_regfile (
        .clk(clk),
        .rst_n(rst_n),

        .rs1_addr(rs1_addr),
        .rs2_addr(rs2_addr),

        .rs1_data(rs1_data),
        .rs2_data(rs2_data),

        .rd_addr(rd_addr),
        .rd_data(rd_data),
        .rd_write_enable(rd_write_enable)
    );

endmodule
