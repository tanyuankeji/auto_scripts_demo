// 自动生成的寄存器文件
// 生成时间: 2025-03-26 20:51:03
// 生成器版本: 2.0.0

module excel_regfile (
    input wire                      clk,
    input wire                      rst_n,
    
    // 写端口 0
    input wire                      wr_en_0,
    input wire [7:0]  wr_addr_0,
    input wire [31:0]  wr_data_0,
    input wire [3:0]  wr_be_0,
    
    // 读端口 0
    input wire [7:0]  rd_addr_0,
    output reg [31:0]  rd_data_0,
    input wire [7:0]  rd_addr_1,
    output reg [31:0]  rd_data_1
);

// 寄存器地址常量定义
localparam ADDR_CTRL_REG = 8'h0;   // 控制寄存器 (ReadWrite类型)localparam ADDR_STATUS_REG = 8'h0;   // 状态寄存器 (ReadOnly类型)localparam ADDR_INT_FLAGS = 8'h0;   // 中断标志寄存器 (ReadWrite类型)localparam ADDR_INT_ENABLE = 8'h0;   // 中断使能寄存器 (ReadWrite类型)
// 寄存器声明
reg [31:0] ctrl_reg_reg;            // 控制寄存器
reg [31:0] status_reg_reg;          // 状态寄存器
reg [31:0] int_flags_reg;           // 中断标志寄存器
reg [31:0] int_enable_reg;          // 中断使能寄存器


// 复位和写逻辑
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg <= 32'h00000000;
        status_reg_reg <= 32'h00000000;
        int_flags_reg <= 32'h00000000;
        int_enable_reg <= 32'h00000000;
    end
    else begin
        // CTRL_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) ctrl_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) ctrl_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) ctrl_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // STATUS_REG 是只读寄存器，忽略写操作
        // INT_FLAGS 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_FLAGS) begin
            if (wr_be_0[0]) int_flags_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_flags_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_flags_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_flags_reg[31:24] <= wr_data_0[31:24];
        end
        // INT_ENABLE 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_ENABLE) begin
            if (wr_be_0[0]) int_enable_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_enable_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_enable_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_enable_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// 读端口0 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_0 = 32'd0;
    
    // CTRL_REG 是ReadWrite类型寄存器
    if (rd_addr_0 == ADDR_CTRL_REG) begin
        rd_data_0 = ctrl_reg_reg;
    end
    // STATUS_REG 是ReadOnly类型寄存器
    if (rd_addr_0 == ADDR_STATUS_REG) begin
        rd_data_0 = status_reg_reg;
    end
    // INT_FLAGS 是ReadWrite类型寄存器
    if (rd_addr_0 == ADDR_INT_FLAGS) begin
        rd_data_0 = int_flags_reg;
    end
    // INT_ENABLE 是ReadWrite类型寄存器
    if (rd_addr_0 == ADDR_INT_ENABLE) begin
        rd_data_0 = int_enable_reg;
    end
end

// 读端口1 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_1 = 32'd0;
    
    // CTRL_REG 是ReadWrite类型寄存器
    if (rd_addr_1 == ADDR_CTRL_REG) begin
        rd_data_1 = ctrl_reg_reg;
    end
    // STATUS_REG 是ReadOnly类型寄存器
    if (rd_addr_1 == ADDR_STATUS_REG) begin
        rd_data_1 = status_reg_reg;
    end
    // INT_FLAGS 是ReadWrite类型寄存器
    if (rd_addr_1 == ADDR_INT_FLAGS) begin
        rd_data_1 = int_flags_reg;
    end
    // INT_ENABLE 是ReadWrite类型寄存器
    if (rd_addr_1 == ADDR_INT_ENABLE) begin
        rd_data_1 = int_enable_reg;
    end
end

endmodule 