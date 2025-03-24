// 自动生成的寄存器文件
// 生成时间: 2025-03-24 20:16:00
// 生成器版本: 2.0.0

module advanced_regfile (
    input wire                      clk,
    input wire                      rst_n,
    
    // 写端口 0
    input wire                      wr_en_0,
    input wire [7:0]  wr_addr_0,
    input wire [31:0]  wr_data_0,
    input wire [3:0]  wr_be_0,
    // 写端口 1
    input wire                      wr_en_1,
    input wire [7:0]  wr_addr_1,
    input wire [31:0]  wr_data_1,
    input wire [3:0]  wr_be_1,
    
    // 读端口 0
    input wire [7:0]  rd_addr_0,
    output reg [31:0]  rd_data_0,
    input wire [7:0]  rd_addr_1,
    output reg [31:0]  rd_data_1
);

// 寄存器地址常量定义
localparam ADDR_CTRL_REG = 8'h0;   // 主控寄存器 (ReadWrite类型)localparam ADDR_STATUS_REG = 8'h0;   // 状态寄存器 (ReadOnly类型)localparam ADDR_INT_FLAGS = 8'h0;   // 中断标志寄存器，读取后自动清零 (ReadClean类型)localparam ADDR_INT_ENABLE = 8'h0;   // 中断使能寄存器 (ReadWrite类型)localparam ADDR_INT_CLEAR = 8'h0;   // 中断清除寄存器，写1清零对应位 (Write1Clean类型)localparam ADDR_INT_SET = 8'h0;   // 中断设置寄存器，写1置位对应位 (Write1Set类型)localparam ADDR_TX_DATA = 8'h0;   // 发送数据寄存器，只能写入 (WriteOnly类型)localparam ADDR_RX_DATA = 8'h0;   // 接收数据寄存器，只能读取 (ReadOnly类型)localparam ADDR_CONFIG = 8'h0;   // 配置寄存器 (ReadWrite类型)localparam ADDR_LOCK_REG = 8'h0;   // 锁定寄存器，只能写入一次 (WriteOnce类型)localparam ADDR_STAT_COUNT = 8'h0;   // 统计计数器，读取后自动置位 (ReadWrite类型)localparam ADDR_W0C_REG = 8'h0;   // 写0清零寄存器，写0清零对应位 (ReadWrite类型)localparam ADDR_W0S_REG = 8'h0;   // 写0置位寄存器，写0置位对应位 (ReadWrite类型)localparam ADDR_TOG_REG = 8'h0;   // 翻转寄存器，写1翻转对应位 (ReadWrite类型)localparam ADDR_VER_REG = 8'h0;   // 版本信息寄存器 (ReadOnly类型)
// 寄存器声明
reg [31:0] ctrl_reg_reg;            // 主控寄存器
reg [31:0] status_reg_reg;          // 状态寄存器
reg [31:0] int_flags_reg;           // 中断标志寄存器，读取后自动清零
reg [31:0] int_enable_reg;          // 中断使能寄存器
reg [31:0] int_clear_reg;           // 中断清除寄存器，写1清零对应位
reg [31:0] int_set_reg;             // 中断设置寄存器，写1置位对应位
reg [31:0] tx_data_reg;             // 发送数据寄存器，只能写入
reg [31:0] rx_data_reg;             // 接收数据寄存器，只能读取
reg [31:0] config_reg;              // 配置寄存器
reg [31:0] lock_reg_reg;            // 锁定寄存器，只能写入一次
reg        lock_reg_written;            // lock_reg 写标志
reg [31:0] stat_count_reg;          // 统计计数器，读取后自动置位
reg [31:0] w0c_reg_reg;             // 写0清零寄存器，写0清零对应位
reg [31:0] w0s_reg_reg;             // 写0置位寄存器，写0置位对应位
reg [31:0] tog_reg_reg;             // 翻转寄存器，写1翻转对应位
reg [31:0] ver_reg_reg;             // 版本信息寄存器

// 复位和写逻辑
always @(posedge clk) begin
    if (rst_n == 1'b0) begin
        ctrl_reg_reg <= 32'h00000001;
        status_reg_reg <= 32'h00000000;
        int_flags_reg <= 32'h00000000;
        int_enable_reg <= 32'h00000000;
        int_clear_reg <= 32'h00000000;
        int_set_reg <= 32'h00000000;
        tx_data_reg <= 32'h00000000;
        rx_data_reg <= 32'h00000000;
        config_reg <= 32'h00000001;
        lock_reg_reg <= 32'h00000000;
        lock_reg_written <= 1'b0;
        stat_count_reg <= 32'h00000000;
        w0c_reg_reg <= 32'hFFFFFFFF;
        w0s_reg_reg <= 32'h00000000;
        tog_reg_reg <= 32'h00000000;
        ver_reg_reg <= 32'h00010001;
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
        // INT_FLAGS 是ReadClean类型寄存器
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
        // INT_CLEAR 是Write1Clean类型寄存器，写1清零对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_CLEAR) begin
            if (wr_be_0[0]) int_clear_reg[7:0] <= int_clear_reg[7:0] & ~wr_data_0[7:0];
            if (wr_be_0[1]) int_clear_reg[15:8] <= int_clear_reg[15:8] & ~wr_data_0[15:8];
            if (wr_be_0[2]) int_clear_reg[23:16] <= int_clear_reg[23:16] & ~wr_data_0[23:16];
            if (wr_be_0[3]) int_clear_reg[31:24] <= int_clear_reg[31:24] & ~wr_data_0[31:24];
        end
        // INT_SET 是Write1Set类型寄存器，写1置位对应位
        if (wr_en_0 && wr_addr_0 == ADDR_INT_SET) begin
            if (wr_be_0[0]) int_set_reg[7:0] <= int_set_reg[7:0] | wr_data_0[7:0];
            if (wr_be_0[1]) int_set_reg[15:8] <= int_set_reg[15:8] | wr_data_0[15:8];
            if (wr_be_0[2]) int_set_reg[23:16] <= int_set_reg[23:16] | wr_data_0[23:16];
            if (wr_be_0[3]) int_set_reg[31:24] <= int_set_reg[31:24] | wr_data_0[31:24];
        end
        // TX_DATA 是WriteOnly类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_TX_DATA) begin
            if (wr_be_0[0]) tx_data_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) tx_data_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) tx_data_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) tx_data_reg[31:24] <= wr_data_0[31:24];
        end
        // RX_DATA 是只读寄存器，忽略写操作
        // CONFIG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CONFIG) begin
            if (wr_be_0[0]) config_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) config_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) config_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) config_reg[31:24] <= wr_data_0[31:24];
        end
        // LOCK_REG 是WriteOnce类型寄存器，只写一次
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG && !lock_reg_written) begin
            if (wr_be_0[0]) lock_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) lock_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) lock_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) lock_reg_reg[31:24] <= wr_data_0[31:24];
            lock_reg_written <= 1'b1; // 设置写标志
        end
        // STAT_COUNT 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_STAT_COUNT) begin
            if (wr_be_0[0]) stat_count_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) stat_count_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) stat_count_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) stat_count_reg[31:24] <= wr_data_0[31:24];
        end
        // W0C_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_W0C_REG) begin
            if (wr_be_0[0]) w0c_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) w0c_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) w0c_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) w0c_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // W0S_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_W0S_REG) begin
            if (wr_be_0[0]) w0s_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) w0s_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) w0s_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) w0s_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // TOG_REG 是ReadWrite类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_TOG_REG) begin
            if (wr_be_0[0]) tog_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) tog_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) tog_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) tog_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // VER_REG 是只读寄存器，忽略写操作
        // CTRL_REG 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_CTRL_REG) begin
            if (wr_be_1[0]) ctrl_reg_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) ctrl_reg_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) ctrl_reg_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) ctrl_reg_reg[31:24] <= wr_data_1[31:24];
        end
        // STATUS_REG 是只读寄存器，忽略写操作
        // INT_FLAGS 是ReadClean类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_INT_FLAGS) begin
            if (wr_be_1[0]) int_flags_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) int_flags_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) int_flags_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) int_flags_reg[31:24] <= wr_data_1[31:24];
        end
        // INT_ENABLE 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_INT_ENABLE) begin
            if (wr_be_1[0]) int_enable_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) int_enable_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) int_enable_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) int_enable_reg[31:24] <= wr_data_1[31:24];
        end
        // INT_CLEAR 是Write1Clean类型寄存器，写1清零对应位
        if (wr_en_1 && wr_addr_1 == ADDR_INT_CLEAR) begin
            if (wr_be_1[0]) int_clear_reg[7:0] <= int_clear_reg[7:0] & ~wr_data_1[7:0];
            if (wr_be_1[1]) int_clear_reg[15:8] <= int_clear_reg[15:8] & ~wr_data_1[15:8];
            if (wr_be_1[2]) int_clear_reg[23:16] <= int_clear_reg[23:16] & ~wr_data_1[23:16];
            if (wr_be_1[3]) int_clear_reg[31:24] <= int_clear_reg[31:24] & ~wr_data_1[31:24];
        end
        // INT_SET 是Write1Set类型寄存器，写1置位对应位
        if (wr_en_1 && wr_addr_1 == ADDR_INT_SET) begin
            if (wr_be_1[0]) int_set_reg[7:0] <= int_set_reg[7:0] | wr_data_1[7:0];
            if (wr_be_1[1]) int_set_reg[15:8] <= int_set_reg[15:8] | wr_data_1[15:8];
            if (wr_be_1[2]) int_set_reg[23:16] <= int_set_reg[23:16] | wr_data_1[23:16];
            if (wr_be_1[3]) int_set_reg[31:24] <= int_set_reg[31:24] | wr_data_1[31:24];
        end
        // TX_DATA 是WriteOnly类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_TX_DATA) begin
            if (wr_be_1[0]) tx_data_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) tx_data_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) tx_data_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) tx_data_reg[31:24] <= wr_data_1[31:24];
        end
        // RX_DATA 是只读寄存器，忽略写操作
        // CONFIG 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_CONFIG) begin
            if (wr_be_1[0]) config_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) config_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) config_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) config_reg[31:24] <= wr_data_1[31:24];
        end
        // LOCK_REG 是WriteOnce类型寄存器，只写一次
        if (wr_en_1 && wr_addr_1 == ADDR_LOCK_REG && !lock_reg_written) begin
            if (wr_be_1[0]) lock_reg_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) lock_reg_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) lock_reg_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) lock_reg_reg[31:24] <= wr_data_1[31:24];
            lock_reg_written <= 1'b1; // 设置写标志
        end
        // STAT_COUNT 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_STAT_COUNT) begin
            if (wr_be_1[0]) stat_count_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) stat_count_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) stat_count_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) stat_count_reg[31:24] <= wr_data_1[31:24];
        end
        // W0C_REG 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_W0C_REG) begin
            if (wr_be_1[0]) w0c_reg_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) w0c_reg_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) w0c_reg_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) w0c_reg_reg[31:24] <= wr_data_1[31:24];
        end
        // W0S_REG 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_W0S_REG) begin
            if (wr_be_1[0]) w0s_reg_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) w0s_reg_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) w0s_reg_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) w0s_reg_reg[31:24] <= wr_data_1[31:24];
        end
        // TOG_REG 是ReadWrite类型寄存器
        if (wr_en_1 && wr_addr_1 == ADDR_TOG_REG) begin
            if (wr_be_1[0]) tog_reg_reg[7:0] <= wr_data_1[7:0];
            if (wr_be_1[1]) tog_reg_reg[15:8] <= wr_data_1[15:8];
            if (wr_be_1[2]) tog_reg_reg[23:16] <= wr_data_1[23:16];
            if (wr_be_1[3]) tog_reg_reg[31:24] <= wr_data_1[31:24];
        end
        // VER_REG 是只读寄存器，忽略写操作

        // 读操作触发的特殊逻辑
        // 如果读端口读取了INT_FLAGS，则清零（ReadClean类型）
        if (rd_addr_0 == ADDR_INT_FLAGS || rd_addr_1 == ADDR_INT_FLAGS) begin
            if (rd_addr_0 == ADDR_INT_FLAGS) 
                int_flags_reg <= 32'd0;
            if (rd_addr_1 == ADDR_INT_FLAGS) 
                int_flags_reg <= 32'd0;
        end
    end
end

// 读端口0 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_0 = 32'd0;
    
    case (rd_addr_0)
        ADDR_CTRL_REG: rd_data_0 = ctrl_reg_reg;  // ReadWrite 类型
        ADDR_STATUS_REG: rd_data_0 = status_reg_reg;  // ReadOnly 类型
        ADDR_INT_FLAGS: rd_data_0 = int_flags_reg;  // ReadClean 类型
        ADDR_INT_ENABLE: rd_data_0 = int_enable_reg;  // ReadWrite 类型
        ADDR_INT_CLEAR: rd_data_0 = int_clear_reg;  // Write1Clean 类型
        ADDR_INT_SET: rd_data_0 = int_set_reg;  // Write1Set 类型
        ADDR_TX_DATA: rd_data_0 = 32'd0;  // WriteOnly 类型
        ADDR_RX_DATA: rd_data_0 = rx_data_reg;  // ReadOnly 类型
        ADDR_CONFIG: rd_data_0 = config_reg;  // ReadWrite 类型
        ADDR_LOCK_REG: rd_data_0 = lock_reg_reg;  // WriteOnce 类型
        ADDR_STAT_COUNT: rd_data_0 = stat_count_reg;  // ReadWrite 类型
        ADDR_W0C_REG: rd_data_0 = w0c_reg_reg;  // ReadWrite 类型
        ADDR_W0S_REG: rd_data_0 = w0s_reg_reg;  // ReadWrite 类型
        ADDR_TOG_REG: rd_data_0 = tog_reg_reg;  // ReadWrite 类型
        ADDR_VER_REG: rd_data_0 = ver_reg_reg;  // ReadOnly 类型
        default: rd_data_0 = 32'd0;  // 未知地址返回0
    endcase
end

// 读端口1 组合逻辑
always @(*) begin
    // 默认值为全0
    rd_data_1 = 32'd0;
    
    case (rd_addr_1)
        ADDR_CTRL_REG: rd_data_1 = ctrl_reg_reg;  // ReadWrite 类型
        ADDR_STATUS_REG: rd_data_1 = status_reg_reg;  // ReadOnly 类型
        ADDR_INT_FLAGS: rd_data_1 = int_flags_reg;  // ReadClean 类型
        ADDR_INT_ENABLE: rd_data_1 = int_enable_reg;  // ReadWrite 类型
        ADDR_INT_CLEAR: rd_data_1 = int_clear_reg;  // Write1Clean 类型
        ADDR_INT_SET: rd_data_1 = int_set_reg;  // Write1Set 类型
        ADDR_TX_DATA: rd_data_1 = 32'd0;  // WriteOnly 类型
        ADDR_RX_DATA: rd_data_1 = rx_data_reg;  // ReadOnly 类型
        ADDR_CONFIG: rd_data_1 = config_reg;  // ReadWrite 类型
        ADDR_LOCK_REG: rd_data_1 = lock_reg_reg;  // WriteOnce 类型
        ADDR_STAT_COUNT: rd_data_1 = stat_count_reg;  // ReadWrite 类型
        ADDR_W0C_REG: rd_data_1 = w0c_reg_reg;  // ReadWrite 类型
        ADDR_W0S_REG: rd_data_1 = w0s_reg_reg;  // ReadWrite 类型
        ADDR_TOG_REG: rd_data_1 = tog_reg_reg;  // ReadWrite 类型
        ADDR_VER_REG: rd_data_1 = ver_reg_reg;  // ReadOnly 类型
        default: rd_data_1 = 32'd0;  // 未知地址返回0
    endcase
end

endmodule 