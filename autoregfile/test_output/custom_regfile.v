// 自动生成的寄存器文件
// 生成时间: 2023-03-22 12:30:45
// 生成器版本: 2.0.0

module custom_regfile (
    input wire                      clk,
    input wire                      rst_n,
    
    // 写端口 0
    input wire                      wr_en_0,
    input wire [7:0]                wr_addr_0,
    input wire [31:0]               wr_data_0,
    input wire [3:0]                wr_be_0,
    
    // 读端口 0
    input wire [7:0]                rd_addr_0,
    output reg [31:0]               rd_data_0,
    input wire [7:0]                rd_addr_1,
    output reg [31:0]               rd_data_1
);

// 寄存器地址常量定义
localparam ADDR_CTRL_REG    = 8'h00;   // 控制寄存器 (ReadWrite类型)
localparam ADDR_STATUS_REG  = 8'h04;   // 状态寄存器 (ReadOnly类型)
localparam ADDR_INT_FLAGS   = 8'h08;   // 中断标志寄存器，读取后自动清零 (ReadClean类型)
localparam ADDR_INT_ENABLE  = 8'h0C;   // 中断使能寄存器 (ReadWrite类型)
localparam ADDR_TX_DATA     = 8'h10;   // 发送数据寄存器，只能写入 (WriteOnly类型)
localparam ADDR_RX_DATA     = 8'h14;   // 接收数据寄存器，只能读取 (ReadOnly类型)
localparam ADDR_CONFIG      = 8'h18;   // 配置寄存器 (ReadWrite类型)
localparam ADDR_INT_CLEAR   = 8'h1C;   // 中断清除寄存器，写1清零中断标志 (Write1Clean类型)
localparam ADDR_INT_SET     = 8'h20;   // 中断设置寄存器，写1设置中断标志 (Write1Set类型)
localparam ADDR_LOCK_REG    = 8'h24;   // 锁定寄存器，只能写入一次 (WriteOnce类型)

// 寄存器声明
reg [31:0] ctrl_reg;                 // 控制寄存器
reg [31:0] status_reg;               // 状态寄存器
reg [31:0] int_flags;                // 中断标志寄存器，读取后自动清零
reg [31:0] int_enable;               // 中断使能寄存器
reg [31:0] tx_data;                  // 发送数据寄存器，只能写入
reg [31:0] rx_data;                  // 接收数据寄存器，只能读取
reg [31:0] config;                   // 配置寄存器
reg [31:0] int_clear;                // 中断清除寄存器，写1清零中断标志
reg [31:0] int_set;                  // 中断设置寄存器，写1设置中断标志
reg [31:0] lock_reg;                 // 锁定寄存器，只能写入一次
reg        lock_reg_written;         // lock_reg 写标志

// 复位逻辑
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg <= 32'd0;
        status_reg <= 32'd0;
        int_flags <= 32'd0;
        int_enable <= 32'd0;
        tx_data <= 32'd0;
        rx_data <= 32'd0;
        config <= 32'd1;
        int_clear <= 32'd0;
        int_set <= 32'd0;
        lock_reg <= 32'd0;
        lock_reg_written <= 1'b0;
    end
    else begin
        // CTRL_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) ctrl_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) ctrl_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) ctrl_reg[31:24] <= wr_data_0[31:24];
        end

        // STATUS_REG 是只读寄存器，忽略写操作
        // 这里模拟状态更新
        status_reg[0] <= ctrl_reg[0]; // 状态位0跟随控制位0
        
        // INT_FLAGS 是ReadClean类型寄存器，读取后自动清零
        if (wr_en_0 && wr_addr_0 == ADDR_INT_FLAGS) begin
            if (wr_be_0[0]) int_flags[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= wr_data_0[31:24];
        end
        
        // INT_ENABLE 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_ENABLE) begin
            if (wr_be_0[0]) int_enable[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_enable[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_enable[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_enable[31:24] <= wr_data_0[31:24];
        end
        
        // TX_DATA 是WriteOnly类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_TX_DATA) begin
            if (wr_be_0[0]) tx_data[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) tx_data[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) tx_data[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) tx_data[31:24] <= wr_data_0[31:24];
        end
        
        // RX_DATA 是ReadOnly类型寄存器，忽略写操作
        // 这里可以添加外部数据输入逻辑
        
        // CONFIG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CONFIG) begin
            if (wr_be_0[0]) config[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) config[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) config[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) config[31:24] <= wr_data_0[31:24];
        end
        
        // INT_CLEAR 是Write1Clean类型寄存器，写1清零对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_CLEAR) begin
            if (wr_be_0[0]) int_flags[7:0] <= int_flags[7:0] & ~wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= int_flags[15:8] & ~wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= int_flags[23:16] & ~wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= int_flags[31:24] & ~wr_data_0[31:24];
        end
        
        // INT_SET 是Write1Set类型寄存器，写1置位对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_SET) begin
            if (wr_be_0[0]) int_flags[7:0] <= int_flags[7:0] | wr_data_0[7:0];
            if (wr_be_0[1]) int_flags[15:8] <= int_flags[15:8] | wr_data_0[15:8];
            if (wr_be_0[2]) int_flags[23:16] <= int_flags[23:16] | wr_data_0[23:16];
            if (wr_be_0[3]) int_flags[31:24] <= int_flags[31:24] | wr_data_0[31:24];
        end
        
        // LOCK_REG 是WriteOnce类型寄存器，只写一次
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG && !lock_reg_written) begin
            if (wr_be_0[0]) lock_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) lock_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) lock_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) lock_reg[31:24] <= wr_data_0[31:24];
            lock_reg_written <= 1'b1; // 设置写标志
        end

        // 读操作触发的特殊逻辑
        // 如果读端口读取了INT_FLAGS，则清零（ReadClean类型）
        if (rd_addr_0 == ADDR_INT_FLAGS || rd_addr_1 == ADDR_INT_FLAGS) begin
            if (rd_addr_0 == ADDR_INT_FLAGS) 
                int_flags <= 32'd0;
            else if (rd_addr_1 == ADDR_INT_FLAGS)
                int_flags <= 32'd0;
        end
    end
end

// 读端口0 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_0 = 32'd0;
    
    case (rd_addr_0)
        ADDR_CTRL_REG:    rd_data_0 = ctrl_reg;      // ReadWrite 类型
        ADDR_STATUS_REG:  rd_data_0 = status_reg;    // ReadOnly 类型
        ADDR_INT_FLAGS:   rd_data_0 = int_flags;     // ReadClean 类型
        ADDR_INT_ENABLE:  rd_data_0 = int_enable;    // ReadWrite 类型
        ADDR_TX_DATA:     rd_data_0 = 32'd0;         // WriteOnly 类型，读取返回0
        ADDR_RX_DATA:     rd_data_0 = rx_data;       // ReadOnly 类型
        ADDR_CONFIG:      rd_data_0 = config;        // ReadWrite 类型
        ADDR_INT_CLEAR:   rd_data_0 = 32'd0;         // Write1Clean 类型，读取返回0
        ADDR_INT_SET:     rd_data_0 = 32'd0;         // Write1Set 类型，读取返回0
        ADDR_LOCK_REG:    rd_data_0 = lock_reg;      // WriteOnce 类型
        default:          rd_data_0 = 32'd0;         // 未知地址返回0
    endcase
end

// 读端口1 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_1 = 32'd0;
    
    case (rd_addr_1)
        ADDR_CTRL_REG:    rd_data_1 = ctrl_reg;      // ReadWrite 类型
        ADDR_STATUS_REG:  rd_data_1 = status_reg;    // ReadOnly 类型
        ADDR_INT_FLAGS:   rd_data_1 = int_flags;     // ReadClean 类型
        ADDR_INT_ENABLE:  rd_data_1 = int_enable;    // ReadWrite 类型
        ADDR_TX_DATA:     rd_data_1 = 32'd0;         // WriteOnly 类型，读取返回0
        ADDR_RX_DATA:     rd_data_1 = rx_data;       // ReadOnly 类型
        ADDR_CONFIG:      rd_data_1 = config;        // ReadWrite 类型
        ADDR_INT_CLEAR:   rd_data_1 = 32'd0;         // Write1Clean 类型，读取返回0
        ADDR_INT_SET:     rd_data_1 = 32'd0;         // Write1Set 类型，读取返回0
        ADDR_LOCK_REG:    rd_data_1 = lock_reg;      // WriteOnce 类型
        default:          rd_data_1 = 32'd0;         // 未知地址返回0
    endcase
end

endmodule 