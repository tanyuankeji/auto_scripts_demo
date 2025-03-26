// 自动生成的寄存器文件
// 生成时间: 2025-03-26 21:19:19
// 生成器版本: 2.0.0

module lock_test_address (
    input wire                      clk,
    input wire                      rst_n,
    
    // 写端口 0
    input wire                      wr_en_0,
    input wire [7:0]  wr_addr_0,
    input wire [31:0]  wr_data_0,
    input wire [3:0]  wr_be_0,
    
    // 读端口 0
    input wire [7:0]  rd_addr_0,
    output reg [31:0]  rd_data_0
);

// 寄存器地址常量定义
localparam ADDR_LOCK_REG = 8'h0;   // 锁定控制寄存器 (LockField类型)localparam ADDR_DATA_REG = 8'h0;   // 数据寄存器 (ReadWrite类型)
// 寄存器声明
reg [31:0] lock_reg_reg;            // 锁定控制寄存器
reg [31:0] data_reg_reg;            // 数据寄存器
wire       data_reg_locked;            // data_reg 锁定标志

// 锁定逻辑
assign data_reg_locked = lock_reg_reg[0];

// 复位和写逻辑
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        lock_reg_reg <= 32'h00000000;
        data_reg_reg <= 32'h00000000;
    end
    else begin
        // LOCK_REG 是LockField类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG) begin
            if (wr_be_0[0]) lock_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) lock_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) lock_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) lock_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // DATA_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_DATA_REG && !data_reg_locked) begin
            if (wr_be_0[0]) data_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) data_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) data_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) data_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// 读端口0 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_0 = 32'd0;
    
    // LOCK_REG 是LockField类型寄存器
    if (rd_addr_0 == ADDR_LOCK_REG) begin
        rd_data_0 = lock_reg_reg;
    end
    // DATA_REG 是ReadWrite类型寄存器
    if (rd_addr_0 == ADDR_DATA_REG) begin
        rd_data_0 = data_reg_reg;
    end
end

endmodule 