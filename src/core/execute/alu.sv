import riscv_pkg::*;


module alu (
    input      word_t data_in_1,
    input      word_t data_in_2,

    output     word_t alu_out,

    input      alu_op_e alu_op,

    output     logic zero
);
always_comb begin
    unique case (alu_op)
        ALU_SLL : alu_out = data_in_1 << data_in_2[4:0];
        ALU_SLT : alu_out = ($signed(data_in_1) < $signed(data_in_2)) ? 32'd1 : 32'd0;
        ALU_SLTU: alu_out = (data_in_1 < data_in_2) ? 32'd1 : 32'd0;
        ALU_XOR : alu_out = data_in_1 ^ data_in_2;
        ALU_OR  : alu_out = data_in_1 | data_in_2;
        ALU_AND : alu_out = data_in_1 & data_in_2;
        ALU_SRL : alu_out = data_in_1 >> data_in_2[4:0];
        ALU_SRA : alu_out = $signed(data_in_1) >>> data_in_2[4:0];
        ALU_SUB : alu_out = data_in_1 - data_in_2;
        ALU_ADD : alu_out = data_in_1 + data_in_2;

        default : alu_out = '0;
    endcase

    zero = (alu_out == 0);
end


endmodule
