package riscv_pkg;



    localparam int INSTR_MEM_DEPTH = 256;
    localparam int XLEN = 32;
    localparam int REG_COUNT = 32;
    localparam int REG_IDX_WIDTH = $clog2(REG_COUNT);
    typedef logic [XLEN-1:0] word_t;
    localparam word_t PC_RESET_VALUE = 32'h0000_0000;
    typedef logic [REG_IDX_WIDTH-1:0] reg_addr_t;


    //TAKEN FROM https://docs.riscv.org/reference/isa/v20260120/unpriv/rv-32-64g.html
    typedef enum logic [6:0] {
        OP_LOAD   = 7'b0000011,
        OP_STORE  = 7'b0100011,
        OP_MADD   = 7'b1000011,
        OP_BRANCH = 7'b1100011,

        OP_LOAD_FP  = 7'b0000111,
        OP_STORE_FP = 7'b0100111,
        OP_MSUB   = 7'b1000111,
        OP_JALR   = 7'b1100111,

        OP_CUSTOM_0 = 7'b0001011,
        OP_CUSTOM_1 = 7'b0101011,
        OP_NMSUB  = 7'b1001011,

        OP_MISC_MEM = 7'b0001111,
        OP_AMO      = 7'b0101111,
        OP_NMADD    = 7'b1001111,
        OP_JAL    = 7'b1101111,

        OP_OP_IMM  = 7'b0010011,
        OP_OP      = 7'b0110011,
        OP_OP_FP   = 7'b1010011,
        OP_SYSTEM  = 7'b1110011,

        OP_AUIPC  = 7'b0010111,
        OP_LUI    = 7'b0110111,
        OP_V  = 7'b1010111,
        OP_VEC = 7'b1110111,

        OP_IMM_32= 7'b0011011,
        OP_OP_32 = 7'b0111011,
        OP_CUSTOM_2 = 7'b1011011,
        OP_CUSTOM_3 = 7'b1111011
    } opcode_e;

    //funct3 & funct7
    localparam logic [2:0] FUNCT3_LOAD_BYTE = 3'b000;
    localparam logic [2:0] FUNCT3_LOAD_HALF = 3'b001;
    localparam logic [2:0] FUNCT3_LOAD_WORD = 3'b010;
    localparam logic [2:0] FUNCT3_LOAD_BYTE_U = 3'b100;
    localparam logic [2:0] FUNCT3_LOAD_HALF_U = 3'b101;

    localparam logic [2:0] FUNCT3_STORE_BYTE = 3'b000;
    localparam logic [2:0] FUNCT3_STORE_HALF = 3'b001;
    localparam logic [2:0] FUNCT3_STORE_WORD = 3'b010;

    localparam logic [2:0] FUNCT3_BRANCH_EQ = 3'b000;
    localparam logic [2:0] FUNCT3_BRANCH_NE = 3'b001;
    localparam logic [2:0] FUNCT3_BRANCH_LT = 3'b100;
    localparam logic [2:0] FUNCT3_BRANCH_GE = 3'b101;
    localparam logic [2:0] FUNCT3_BRANCH_LT_U = 3'b110;
    localparam logic [2:0] FUNCT3_BRANCH_GE_U = 3'b111;

    localparam logic [2:0] FUNCT3_OP_IMM_ADD_SUB = 3'b000;
    localparam logic [2:0] FUNCT3_OP_IMM_SLL = 3'b001;
    localparam logic [2:0] FUNCT3_OP_IMM_SLT = 3'b010;
    localparam logic [2:0] FUNCT3_OP_IMM_SLTU = 3'b011;
    localparam logic [2:0] FUNCT3_OP_IMM_XOR = 3'b100;
    localparam logic [2:0] FUNCT3_OP_IMM_SRL_SRA = 3'b101;
    localparam logic [2:0] FUNCT3_OP_IMM_OR = 3'b110;
    localparam logic [2:0] FUNCT3_OP_IMM_AND = 3'b111;
    localparam logic [6:0] FUNCT7_OP_IMM_SRL = 7'b0000000;
    localparam logic [6:0] FUNCT7_OP_IMM_SRA = 7'b0100000;

    localparam logic [2:0] FUNCT3_OP_ADD_SUB = 3'b000;
    localparam logic [2:0] FUNCT3_OP_SLL = 3'b001;
    localparam logic [2:0] FUNCT3_OP_SLT = 3'b010;
    localparam logic [2:0] FUNCT3_OP_SLTU = 3'b011;
    localparam logic [2:0] FUNCT3_OP_XOR = 3'b100;
    localparam logic [2:0] FUNCT3_OP_SRL_SRA = 3'b101;
    localparam logic [2:0] FUNCT3_OP_OR = 3'b110;
    localparam logic [2:0] FUNCT3_OP_AND = 3'b111;
    localparam logic [6:0] FUNCT7_OP_SRL = 7'b0000000;
    localparam logic [6:0] FUNCT7_OP_SRA = 7'b0100000;
    localparam logic [6:0] FUNCT7_OP_SUB = 7'b0100000;
    localparam logic [6:0] FUNCT7_OP_ADD = 7'b0000000;

    //TODO: ADD MORE ALU OPS

    typedef enum logic [4:0] {
    ALU_SLL, ALU_SLT, ALU_SLTU, ALU_XOR, ALU_OR,
    ALU_AND, ALU_SRL, ALU_SRA, ALU_SUB, ALU_ADD
    } alu_op_e;
endpackage
