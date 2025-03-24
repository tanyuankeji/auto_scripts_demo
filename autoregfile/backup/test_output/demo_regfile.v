// Auto-generated Register File
// Generated at 2023-03-22 10:30:45
// Generator Version: 1.0.0

module demo_regfile (
    input wire                      clk,
    input wire                      rst_n,
    
    // 写端口
    input wire                      wr_en_0,
    input wire [7:0]                wr_addr_0,
    input wire [31:0]               wr_data_0,
    input wire [3:0]                wr_be_0,
    
    // 读端口
    input wire [7:0]                rd_addr_0,
    output reg [31:0]               rd_data_0,
    input wire [7:0]                rd_addr_1,
    output reg [31:0]               rd_data_1
);

// 寄存器地址常量定义
localparam ADDR_CTRL_REG        = 8'h00;   // 控制寄存器 (ReadWrite类型)
localparam ADDR_STATUS_REG      = 8'h04;   // 状态寄存器 (ReadOnly类型)
localparam ADDR_INT_FLAGS       = 8'h08;   // 中断标志寄存器 (ReadClean类型)
localparam ADDR_INT_ENABLE      = 8'h0C;   // 中断使能寄存器 (ReadWrite类型)
localparam ADDR_TX_DATA         = 8'h10;   // 发送数据寄存器 (WriteOnly类型)
localparam ADDR_RX_DATA         = 8'h14;   // 接收数据寄存器 (ReadOnly类型)
localparam ADDR_CONFIG          = 8'h18;   // 配置寄存器 (ReadWrite类型)
localparam ADDR_INT_CLEAR       = 8'h1C;   // 中断清除寄存器 (Write1Clean类型)
localparam ADDR_INT_SET         = 8'h20;   // 中断设置寄存器 (Write1Set类型)
localparam ADDR_LOCK_REG        = 8'h24;   // 锁定寄存器 (WriteOnce类型)

// 寄存器声明
reg [31:0] ctrl_reg;           // 控制寄存器
reg [31:0] status_reg;         // 状态寄存器
reg [31:0] int_flags;          // 中断标志寄存器
reg [31:0] int_enable;         // 中断使能寄存器
reg [31:0] tx_data;            // 发送数据寄存器
reg [31:0] rx_data;            // 接收数据寄存器
reg [31:0] config_reg;         // 配置寄存器
reg [31:0] int_clear;          // 中断清除寄存器
reg [31:0] int_set;            // 中断设置寄存器
reg [31:0] lock_reg;           // 锁定寄存器
reg        lock_reg_written;   // 锁定寄存器写标志

// 复位逻辑
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 复位所有寄存器
        ctrl_reg <= 32'h00000000;
        status_reg <= 32'h00000000;
        int_flags <= 32'h00000000;
        int_enable <= 32'h00000000;
        tx_data <= 32'h00000000;
        rx_data <= 32'h00000000;
        config_reg <= 32'h00000001; // 默认配置
        int_clear <= 32'h00000000;
        int_set <= 32'h00000000;
        lock_reg <= 32'h00000000;
        lock_reg_written <= 1'b0;
    end
    else begin
        // 写逻辑
        // CTRL_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) ctrl_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) ctrl_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) ctrl_reg[31:24] <= wr_data_0[31:24];
        end
        
        // STATUS_REG 是 ReadOnly 类型寄存器，不可写
        // 这里模拟状态更新
        status_reg[0] <= ctrl_reg[0]; // 仅示例：状态位跟随控制位
        
        // INT_FLAGS 是 ReadClean 类型寄存器，读取后自动清零
        // 写操作模拟中断标志设置
        if (wr_en_0 && wr_addr_0 == ADDR_INT_FLAGS) begin
            if (wr_be_0[0]) int_flags[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= wr_data_0[31:24];
        end
        
        // INT_ENABLE 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_ENABLE) begin
            if (wr_be_0[0]) int_enable[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_enable[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_enable[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_enable[31:24] <= wr_data_0[31:24];
        end
        
        // TX_DATA 是 WriteOnly 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_TX_DATA) begin
            if (wr_be_0[0]) tx_data[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) tx_data[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) tx_data[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) tx_data[31:24] <= wr_data_0[31:24];
        end
        
        // RX_DATA 是 ReadOnly 类型寄存器，不可写
        // 这里可以添加外部数据输入逻辑
        
        // CONFIG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CONFIG) begin
            if (wr_be_0[0]) config_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) config_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) config_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) config_reg[31:24] <= wr_data_0[31:24];
        end
        
        // INT_CLEAR 是 Write1Clean 类型寄存器，写1清零对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_CLEAR) begin
            if (wr_be_0[0]) int_flags[7:0] <= int_flags[7:0] & ~wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= int_flags[15:8] & ~wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= int_flags[23:16] & ~wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= int_flags[31:24] & ~wr_data_0[31:24];
        end
        
        // INT_SET 是 Write1Set 类型寄存器，写1设置对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_SET) begin
            if (wr_be_0[0]) int_flags[7:0] <= int_flags[7:0] | wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= int_flags[15:8] | wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= int_flags[23:16] | wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= int_flags[31:24] | wr_data_0[31:24];
        end
        
        // LOCK_REG 是 WriteOnce 类型寄存器，只能写一次
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG && !lock_reg_written) begin
            if (wr_be_0[0]) lock_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) lock_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) lock_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) lock_reg[31:24] <= wr_data_0[31:24];
            lock_reg_written <= 1'b1; // 设置写标志，防止再次写入
        end
        
        // 读操作触发的特殊逻辑
        if (rd_addr_0 == ADDR_INT_FLAGS || rd_addr_1 == ADDR_INT_FLAGS) begin
            // 如果读端口读取了INT_FLAGS，则清零（ReadClean类型）
            if (rd_addr_0 == ADDR_INT_FLAGS) 
                int_flags <= 32'h00000000;
            else if (rd_addr_1 == ADDR_INT_FLAGS)
                int_flags <= 32'h00000000;
        end
    end
end

// 读端口0 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_0 = 32'h00000000;
    
    case (rd_addr_0)
        ADDR_CTRL_REG:    rd_data_0 = ctrl_reg;      // ReadWrite
        ADDR_STATUS_REG:  rd_data_0 = status_reg;    // ReadOnly
        ADDR_INT_FLAGS:   rd_data_0 = int_flags;     // ReadClean
        ADDR_INT_ENABLE:  rd_data_0 = int_enable;    // ReadWrite
        ADDR_TX_DATA:     rd_data_0 = 32'h00000000;  // WriteOnly 读取返回0
        ADDR_RX_DATA:     rd_data_0 = rx_data;       // ReadOnly
        ADDR_CONFIG:      rd_data_0 = config_reg;    // ReadWrite
        ADDR_INT_CLEAR:   rd_data_0 = 32'h00000000;  // Write1Clean 读取返回0
        ADDR_INT_SET:     rd_data_0 = 32'h00000000;  // Write1Set 读取返回0
        ADDR_LOCK_REG:    rd_data_0 = lock_reg;      // WriteOnce
        default:          rd_data_0 = 32'h00000000;  // 未知地址返回0
    endcase
end

// 读端口1 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_1 = 32'h00000000;
    
    case (rd_addr_1)
        ADDR_CTRL_REG:    rd_data_1 = ctrl_reg;      // ReadWrite
        ADDR_STATUS_REG:  rd_data_1 = status_reg;    // ReadOnly
        ADDR_INT_FLAGS:   rd_data_1 = int_flags;     // ReadClean
        ADDR_INT_ENABLE:  rd_data_1 = int_enable;    // ReadWrite
        ADDR_TX_DATA:     rd_data_1 = 32'h00000000;  // WriteOnly 读取返回0
        ADDR_RX_DATA:     rd_data_1 = rx_data;       // ReadOnly
        ADDR_CONFIG:      rd_data_1 = config_reg;    // ReadWrite
        ADDR_INT_CLEAR:   rd_data_1 = 32'h00000000;  // Write1Clean 读取返回0
        ADDR_INT_SET:     rd_data_1 = 32'h00000000;  // Write1Set 读取返回0
        ADDR_LOCK_REG:    rd_data_1 = lock_reg;      // WriteOnce
        default:          rd_data_1 = 32'h00000000;  // 未知地址返回0
    endcase
end

endmodule 