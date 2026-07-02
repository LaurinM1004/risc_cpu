import riscv_pkg::*;

module pc_reg (
    input   logic clk,
    input   logic rst_n,

    input   word_t pc_in,
    output  word_t pc_out
);

always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        pc_out <= PC_RESET_VALUE;
    end else begin
        pc_out <= pc_in;
    end
end

endmodule
