import riscv_pkg::*;

module regfile(
    input logic         clk,
    input logic         rst_n,

    input reg_addr_t        rs1_addr,
    input reg_addr_t        rs2_addr,

    output word_t       rs1_data,
    output word_t       rs2_data,

    input reg_addr_t        rd_addr,
    input word_t        rd_data,
    input logic         rd_write_enable
);

    word_t regs[REG_COUNT];

    assign rs1_data = rs1_addr== 0 ? '0 : regs[rs1_addr];
    assign rs2_data = rs2_addr== 0 ? '0 : regs[rs2_addr];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            regs <= '{default:0};
        end
        else if (rd_write_enable && !(rd_addr==0)) begin
            regs[rd_addr] <= rd_data;
        end
    end


endmodule
