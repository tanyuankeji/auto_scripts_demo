// 自动生成的寄存器文件
// 生成时间: 2025-03-24 19:57:34
// 生成器版本: 2.0.0

module test_regfile (
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
localparam ADDR_CTRL_REG = 8'h0;   // 控制寄存器 (ReadWrite类型)localparam ADDR_STATUS_REG = 8'h0;   // 状态寄存器 (ReadOnly类型)localparam ADDR_INT_EN_REG = 8'h0;   // 中断使能寄存器 (ReadWrite类型)localparam ADDR_INT_STATUS_REG = 8'h0;   // 中断状态寄存器，写1清零 (Write1Clean类型)localparam ADDR_VERSION_REG = 8'h0;   // 版本寄存器 (ReadOnly类型)localparam ADDR_CONFIG_REG = 8'h0;   // 配置寄存器，只能写入一次 (WriteOnce类型)
// 寄存器声明
reg [31:0] ctrl_reg_reg;            // 控制寄存器
reg [31:0] status_reg_reg;          // 状态寄存器
reg [31:0] int_en_reg_reg;          // 中断使能寄存器
reg [31:0] int_status_reg_reg;      // 中断状态寄存器，写1清零
reg [31:0] version_reg_reg;         // 版本寄存器
reg [31:0] config_reg_reg;          // 配置寄存器，只能写入一次
reg        config_reg_written;          // config_reg 写标志

// 复位和写逻辑
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg <= 32'h00000000;
        status_reg_reg <= 32'h00000000;
        int_en_reg_reg <= 32'h00000000;
        int_status_reg_reg <= 32'h00000000;
        version_reg_reg <= 32'h00010000;
        config_reg_reg <= 32'h00000000;
        config_reg_written <= 1'b0;
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
        // INT_EN_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_EN_REG) begin
            if (wr_be_0[0]) int_en_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_en_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_en_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_en_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // INT_STATUS_REG 是Write1Clean类型寄存器，写1清零对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_STATUS_REG) begin
            if (wr_be_0[0]) int_status_reg_reg[7:0] <= int_status_reg_reg[7:0] & ~wr_data_0[7:0];
            if (wr_be_0[1]) int_status_reg_reg[15:8] <= int_status_reg_reg[15:8] & ~wr_data_0[15:8];
            if (wr_be_0[2]) int_status_reg_reg[23:16] <= int_status_reg_reg[23:16] & ~wr_data_0[23:16];
            if (wr_be_0[3]) int_status_reg_reg[31:24] <= int_status_reg_reg[31:24] & ~wr_data_0[31:24];
        end
        // VERSION_REG 是只读寄存器，忽略写操作
        // CONFIG_REG 是WriteOnce类型寄存器，只写一次
        if (wr_en_0 && wr_addr_0 == ADDR_CONFIG_REG && !config_reg_written) begin
            if (wr_be_0[0]) config_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) config_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) config_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) config_reg_reg[31:24] <= wr_data_0[31:24];
            config_reg_written <= 1'b1; // 设置写标志
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
    // INT_EN_REG 是ReadWrite类型寄存器
    if (rd_addr_0 == ADDR_INT_EN_REG) begin
        rd_data_0 = int_en_reg_reg;
    end
    // INT_STATUS_REG 是Write1Clean类型寄存器
    if (rd_addr_0 == ADDR_INT_STATUS_REG) begin
        rd_data_0 = int_status_reg_reg;
    end
    // VERSION_REG 是ReadOnly类型寄存器
    if (rd_addr_0 == ADDR_VERSION_REG) begin
        rd_data_0 = version_reg_reg;
    end
    // CONFIG_REG 是WriteOnce类型寄存器
    if (rd_addr_0 == ADDR_CONFIG_REG) begin
        rd_data_0 = config_reg_reg;
    end
end

endmodule 