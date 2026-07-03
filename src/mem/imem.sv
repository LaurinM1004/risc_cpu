import riscv_pkg::*;

module imem #(
    parameter string MEM_INIT_FILE = "tb/imem.hex"
) (
    input word_t addr,
    output word_t instr
);
    word_t i_mem [0:INSTR_MEM_DEPTH-1];
    localparam int ADDR_WIDTH = $clog2(INSTR_MEM_DEPTH);

    initial begin
        $readmemh(MEM_INIT_FILE, i_mem);
    end

// cut off last two bits s.t. division by 4
    assign instr = i_mem[addr[ADDR_WIDTH+1:2]];
endmodule
