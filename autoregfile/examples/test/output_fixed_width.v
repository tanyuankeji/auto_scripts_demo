// =============================================================================
// 自动生成的寄存器文件: improved_hierarchical_regfile
// 生成时间: 2025-03-29 18:35:02
// =============================================================================

// DEBUG: 字段位置信息
// CTRL_REG 寄存器字段调试信息
// 原始字段数量: 3
// 字段名: enable, 位范围: high=0, low=0, width=1
// 字段名: mode, 位范围: high=2, low=1, width=2
// 字段名: start, 位范围: high=3, low=3, width=1
// STATUS_REG 寄存器字段调试信息
// 原始字段数量: 2
// 字段名: busy, 位范围: high=0, low=0, width=1
// 字段名: error, 位范围: high=1, low=1, width=1
// INT_FLAG_REG 寄存器字段调试信息
// 原始字段数量: 1
// 字段名: data_ready, 位范围: high=0, low=0, width=1
// WRITEONLY_REG 寄存器字段调试信息
// WRITE1SET_REG 寄存器字段调试信息
// LOCK_TEST_REG 寄存器字段调试信息
// 原始字段数量: 2
// 字段名: locked_field, 位范围: high=7, low=0, width=8
// 字段名: magic_field, 位范围: high=15, low=8, width=8

// DEBUG: 寄存器宽度计算
    // CTRL_REG 字段 enable high=0
    // CTRL_REG 字段 mode high=2
      // 更新最大位置为 2
    // CTRL_REG 字段 start high=3
      // 更新最大位置为 3
// CTRL_REG 最高位 = 0, 计算宽度 = 1
    // STATUS_REG 字段 busy high=0
    // STATUS_REG 字段 error high=1
      // 更新最大位置为 1
// STATUS_REG 最高位 = 0, 计算宽度 = 1
    // INT_FLAG_REG 字段 data_ready high=0
// INT_FLAG_REG 最高位 = 0, 计算宽度 = 1
    // LOCK_TEST_REG 字段 locked_field high=7
      // 更新最大位置为 7
    // LOCK_TEST_REG 字段 magic_field high=15
      // 更新最大位置为 15
// LOCK_TEST_REG 最高位 = 0, 计算宽度 = 1

`timescale 1ns / 1ps

module improved_hierarchical_regfile (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // 总线接口
    input  wire [7:0]     addr,
    input  wire                     chip_select,
    input  wire                     write_en,
    input  wire                     read_en,
    input  wire [31:0]     write_data,
    output reg  [31:0]     read_data,
    output wire                     data_valid,
    

    output wire [0:0]      ctrl_reg_enable_o,
    input  wire [0:0]      ctrl_reg_enable_i,
    input  wire                       ctrl_reg_enable_wen,
    output wire [1:0]      ctrl_reg_mode_o,
    input  wire [1:0]      ctrl_reg_mode_i,
    input  wire                       ctrl_reg_mode_wen,
    input  wire [0:0]      ctrl_reg_start_i,
    input  wire                       ctrl_reg_start_wen,
    output wire [0:0]      status_reg_busy_o,
    input  wire [0:0]      status_reg_busy_i,
    input  wire                       status_reg_busy_wen,
    output wire [0:0]      status_reg_error_o,
    input  wire [0:0]      status_reg_error_i,
    input  wire                       status_reg_error_wen,
    input  wire [0:0]      int_flag_reg_data_ready_i,
    input  wire                       int_flag_reg_data_ready_wen,
    input  wire [7:0]      writeonly_reg_i,
    input  wire                      writeonly_reg_wen,
    input  wire [7:0]      write1set_reg_i,
    input  wire                      write1set_reg_wen,
    output wire [7:0]      lock_test_reg_locked_field_o,
    input  wire [7:0]      lock_test_reg_locked_field_i,
    input  wire                       lock_test_reg_locked_field_wen,
    output wire [7:0]      lock_test_reg_magic_field_o,
    input  wire [7:0]      lock_test_reg_magic_field_i,
    input  wire                       lock_test_reg_magic_field_wen
);

// =============================================================================
// 字段位置定义
// =============================================================================

// CTRL_REG 字段位置定义
localparam CTRL_REG_ENABLE_POS   = 0;
localparam CTRL_REG_ENABLE_WIDTH = 1;
localparam CTRL_REG_MODE_POS   = 1;
localparam CTRL_REG_MODE_WIDTH = 2;
localparam CTRL_REG_START_POS   = 3;
localparam CTRL_REG_START_WIDTH = 1;
// STATUS_REG 字段位置定义
localparam STATUS_REG_BUSY_POS   = 0;
localparam STATUS_REG_BUSY_WIDTH = 1;
localparam STATUS_REG_ERROR_POS   = 1;
localparam STATUS_REG_ERROR_WIDTH = 1;
// INT_FLAG_REG 字段位置定义
localparam INT_FLAG_REG_DATA_READY_POS   = 0;
localparam INT_FLAG_REG_DATA_READY_WIDTH = 1;
// LOCK_TEST_REG 字段位置定义
localparam LOCK_TEST_REG_LOCKED_FIELD_POS   = 0;
localparam LOCK_TEST_REG_LOCKED_FIELD_WIDTH = 8;
localparam LOCK_TEST_REG_MAGIC_FIELD_POS   = 8;
localparam LOCK_TEST_REG_MAGIC_FIELD_WIDTH = 8;

// =============================================================================
// 寄存器位宽定义 - 架构优化：添加自动计算的寄存器位宽
// =============================================================================
localparam CTRL_REG_WIDTH = 4;
localparam STATUS_REG_WIDTH = 2;
localparam INT_FLAG_REG_WIDTH = 1;
localparam WRITEONLY_REG_WIDTH = 8;
localparam WRITE1SET_REG_WIDTH = 8;
localparam LOCK_TEST_REG_WIDTH = 16;

// =============================================================================
// 控制信号定义
// =============================================================================

// 控制信号
wire write_active = chip_select && write_en;
wire read_active = chip_select && read_en;
assign data_valid = read_active;

// 地址选择信号
wire sel_ctrl_reg = (addr == 8'h00);
wire sel_status_reg = (addr == 8'h04);
wire sel_int_flag_reg = (addr == 8'h08);
wire sel_writeonly_reg = (addr == 8'h0C);
wire sel_write1set_reg = (addr == 8'h1C);
wire sel_lock_test_reg = (addr == 8'h14);

// =============================================================================
// 寄存器定义
// =============================================================================

// CTRL_REG 寄存器 - 控制寄存器
reg [CTRL_REG_WIDTH-1:0] ctrl_reg;
// STATUS_REG 寄存器 - 状态寄存器
reg [STATUS_REG_WIDTH-1:0] status_reg;
// INT_FLAG_REG 寄存器 - 中断标志寄存器
reg [INT_FLAG_REG_WIDTH-1:0] int_flag_reg;
// WRITEONLY_REG 寄存器 - 只写寄存器
reg [WRITEONLY_REG_WIDTH-1:0] writeonly_reg;
// WRITE1SET_REG 寄存器 - 写1置位寄存器
reg [WRITE1SET_REG_WIDTH-1:0] write1set_reg;
// LOCK_TEST_REG 寄存器 - 
reg [LOCK_TEST_REG_WIDTH-1:0] lock_test_reg;

// CTRL_REG 字段寄存器
reg [0:0] ctrl_reg_enable_reg;  // 使能位
reg [1:0] ctrl_reg_mode_reg;  // 模式选择
reg [0:0] ctrl_reg_start_reg;  // 启动位
// STATUS_REG 字段寄存器
reg [0:0] status_reg_busy_reg;  // 忙状态标志
reg [0:0] status_reg_error_reg;  // 错误标志
// INT_FLAG_REG 字段寄存器
reg [0:0] int_flag_reg_data_ready_reg;  // 数据就绪中断
// LOCK_TEST_REG 字段寄存器
reg [7:0] lock_test_reg_locked_field_reg;  // 受锁控制的字段
reg [7:0] lock_test_reg_magic_field_reg;  // 魔数控制的字段

// =============================================================================
// 字段与寄存器连接
// =============================================================================

// CTRL_REG 寄存器组合
always @(*) begin
    ctrl_reg = {
        {(32-CTRL_REG_WIDTH){1'b0}},  // 高位填充
        ctrl_reg_start_reg,        ctrl_reg_mode_reg,        ctrl_reg_enable_reg    };
end

// CTRL_REG 字段接口连接
assign ctrl_reg_enable_o = ctrl_reg_enable_reg;
assign ctrl_reg_mode_o = ctrl_reg_mode_reg;
// STATUS_REG 寄存器组合
always @(*) begin
    status_reg = {
        {(32-STATUS_REG_WIDTH){1'b0}},  // 高位填充
        status_reg_error_reg,        status_reg_busy_reg    };
end

// STATUS_REG 字段接口连接
assign status_reg_busy_o = status_reg_busy_reg;
assign status_reg_error_o = status_reg_error_reg;
// INT_FLAG_REG 寄存器组合
always @(*) begin
    int_flag_reg = {
        {(32-INT_FLAG_REG_WIDTH){1'b0}},  // 高位填充
        int_flag_reg_data_ready_reg    };
end

// INT_FLAG_REG 字段接口连接
// LOCK_TEST_REG 寄存器组合
always @(*) begin
    lock_test_reg = {
        {(32-LOCK_TEST_REG_WIDTH){1'b0}},  // 高位填充
        lock_test_reg_magic_field_reg,        lock_test_reg_locked_field_reg    };
end

// LOCK_TEST_REG 字段接口连接
assign lock_test_reg_locked_field_o = lock_test_reg_locked_field_reg;
assign lock_test_reg_magic_field_o = lock_test_reg_magic_field_reg;

// =============================================================================
// 读取逻辑
// =============================================================================
always @(*) begin
    read_data = 32'd0;  // 默认值
    
    if (read_active) begin
        if (sel_ctrl_reg) begin
            read_data = {(32-CTRL_REG_WIDTH){1'b0}, ctrl_reg};
        end
        else if (sel_status_reg) begin
            read_data = {(32-STATUS_REG_WIDTH){1'b0}, status_reg};
        end
        else if (sel_int_flag_reg) begin
            read_data = {(32-INT_FLAG_REG_WIDTH){1'b0}, int_flag_reg};
        end
        else if (sel_writeonly_reg) begin
            read_data = 32'd0; // 只写寄存器，读取返回0
        end
        else if (sel_write1set_reg) begin
            read_data = {(32-WRITE1SET_REG_WIDTH){1'b0}, write1set_reg};
        end
        else if (sel_lock_test_reg) begin
            read_data = {(32-LOCK_TEST_REG_WIDTH){1'b0}, lock_test_reg};
        end
        else begin
            read_data = 32'd0;
        end
    end
end

// =============================================================================
// 寄存器更新逻辑
// =============================================================================
// CTRL_REG 子字段寄存器更新
// ENABLE 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        ctrl_reg_enable_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_ctrl_reg) begin            ctrl_reg_enable_reg <= write_data[0:0];        end
        else if (ctrl_reg_enable_wen) begin
            ctrl_reg_enable_reg <= ctrl_reg_enable_i;
        end        end    end
end
// MODE 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        ctrl_reg_mode_reg <= 2'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_ctrl_reg) begin            ctrl_reg_mode_reg <= write_data[2:1];        end
        else if (ctrl_reg_mode_wen) begin
            ctrl_reg_mode_reg <= ctrl_reg_mode_i;
        end        end    end
end
// START 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        ctrl_reg_start_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_ctrl_reg) begin            // 写脉冲，下一个周期自动清零
            ctrl_reg_start_reg <= write_data[3:3];        end
        else if (ctrl_reg_start_wen) begin
            ctrl_reg_start_reg <= ctrl_reg_start_i;
        end        else begin
            // 脉冲类型字段在没有写入时自动清零
            ctrl_reg_start_reg <= 1'h0;
        end    end
end


// STATUS_REG 子字段寄存器更新
// BUSY 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        status_reg_busy_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_status_reg) begin            // 只读字段，忽略软件写入        end
        else if (status_reg_busy_wen) begin
            status_reg_busy_reg <= status_reg_busy_i;
        end        end    end
end
// ERROR 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        status_reg_error_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_status_reg) begin            // 只读字段，忽略软件写入        end
        else if (status_reg_error_wen) begin
            status_reg_error_reg <= status_reg_error_i;
        end        end    end
end


// INT_FLAG_REG 子字段寄存器更新
// DATA_READY 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        int_flag_reg_data_ready_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_int_flag_reg) begin            int_flag_reg_data_ready_reg <= int_flag_reg_data_ready_reg & ~write_data[0:0];        end
        else if (int_flag_reg_data_ready_wen) begin
            int_flag_reg_data_ready_reg <= int_flag_reg_data_ready_i;
        end        end    end
end


// WRITEONLY_REG 寄存器 (无子字段)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonly_reg <= 8'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_writeonly_reg) begin            writeonly_reg <= write_data[7:0];        end
        else if (writeonly_reg_wen) begin
            writeonly_reg <= writeonly_reg_i;
        end        end    end
end

// WRITE1SET_REG 寄存器 (无子字段)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg <= 8'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_write1set_reg) begin            write1set_reg <= write1set_reg | write_data[7:0];        end
        else if (write1set_reg_wen) begin
            write1set_reg <= write1set_reg_i;
        end        end    end
end

// LOCK_TEST_REG 子字段寄存器更新
// LOCKED_FIELD 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        lock_test_reg_locked_field_reg <= 8'h55;
    end
    else begin
        // 软件优先
        if (write_active && sel_lock_test_reg) begin            lock_test_reg_locked_field_reg <= write_data[7:0];        end
        else if (lock_test_reg_locked_field_wen) begin
            lock_test_reg_locked_field_reg <= lock_test_reg_locked_field_i;
        end        end    end
end
// MAGIC_FIELD 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        lock_test_reg_magic_field_reg <= 8'hAA;
    end
    else begin
        // 软件优先
        if (write_active && sel_lock_test_reg) begin            lock_test_reg_magic_field_reg <= write_data[15:8];        end
        else if (lock_test_reg_magic_field_wen) begin
            lock_test_reg_magic_field_reg <= lock_test_reg_magic_field_i;
        end        end    end
end


endmodule 