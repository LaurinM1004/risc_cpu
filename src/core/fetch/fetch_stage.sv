import riscv_pkg::*;

module fetch_stage (
    input logic clk,
    input logic rst_n,

    input word_t jump_target,
    input logic  take_jump,

    output word_t pc_out

);
    word_t pc_in;

    assign pc_in = take_jump ? jump_target : pc_out + 4;

    pc_reg i_pc_reg (
        .clk(clk),
        .rst_n(rst_n),
        .pc_in(pc_in),
        .pc_out(pc_out)
    );

endmodule
