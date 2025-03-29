// =============================================================================
// 自动生成的寄存器文件: improved_hierarchical_regfile
// 生成时间: 2025-03-29 12:15:47
// =============================================================================

`timescale 1ns / 1ps

module improved_hierarchical_regfile (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // 总线接口
    input  wire [7:0]   addr,
    input  wire                     chip_select,
    input  wire                     write_en,
    input  wire                     read_en,
    input  wire [31:0]   write_data,
    output reg  [31:0]   read_data,
    output wire                     data_valid    

    output wire [0:0] ctrl_reg_enable_o,
    input  wire [0:0] ctrl_reg_enable_i,
    input  wire                       ctrl_reg_enable_wen,
    output wire [1:0] ctrl_reg_mode_o,
    input  wire [1:0] ctrl_reg_mode_i,
    input  wire                       ctrl_reg_mode_wen,
    input  wire [0:0] ctrl_reg_start_i,
    input  wire                       ctrl_reg_start_wen,
    output wire [0:0] status_reg_busy_o,
    input  wire [0:0] status_reg_busy_i,
    input  wire                       status_reg_busy_wen,
    output wire [0:0] status_reg_error_o,
    input  wire [0:0] status_reg_error_i,
    input  wire                       status_reg_error_wen,
    input  wire [0:0] int_flag_reg_data_ready_i,
    input  wire                       int_flag_reg_data_ready_wen,
    input  wire [7:0] writeonly_reg_i,
    input  wire                      writeonly_reg_wen,
    input  wire [7:0] write1set_reg_i,
    input  wire                      write1set_reg_wen,
    output wire [7:0] lock_test_reg_locked_field_o,
    input  wire [7:0] lock_test_reg_locked_field_i,
    input  wire                       lock_test_reg_locked_field_wen,
    output wire [7:0] lock_test_reg_magic_field_o,
    input  wire [7:0] lock_test_reg_magic_field_i,
    input  wire                       lock_test_reg_magic_field_wen
);

// =============================================================================
// 字段位置定义
// =============================================================================

// CTRL_REG 字段位置定义
localparam CTRL_REG_ENABLE_POS = 0;
localparam CTRL_REG_ENABLE_WIDTH = 1;
localparam CTRL_REG_MODE_POS = 1;
localparam CTRL_REG_MODE_WIDTH = 2;
localparam CTRL_REG_START_POS = 3;
localparam CTRL_REG_START_WIDTH = 1;
// STATUS_REG 字段位置定义
localparam STATUS_REG_BUSY_POS = 0;
localparam STATUS_REG_BUSY_WIDTH = 1;
localparam STATUS_REG_ERROR_POS = 1;
localparam STATUS_REG_ERROR_WIDTH = 1;
// INT_FLAG_REG 字段位置定义
localparam INT_FLAG_REG_DATA_READY_POS = 0;
localparam INT_FLAG_REG_DATA_READY_WIDTH = 1;
// LOCK_TEST_REG 字段位置定义
localparam LOCK_TEST_REG_LOCKED_FIELD_POS = 0;
localparam LOCK_TEST_REG_LOCKED_FIELD_WIDTH = 8;
localparam LOCK_TEST_REG_MAGIC_FIELD_POS = 8;
localparam LOCK_TEST_REG_MAGIC_FIELD_WIDTH = 8;

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
reg [0:0] ctrl_reg_reg;
// STATUS_REG 寄存器 - 状态寄存器
reg [0:0] status_reg_reg;
// INT_FLAG_REG 寄存器 - 中断标志寄存器
reg [0:0] int_flag_reg_reg;
// WRITEONLY_REG 寄存器 - 只写寄存器
reg [7:0] writeonly_reg_reg;
// WRITE1SET_REG 寄存器 - 写1置位寄存器
reg [7:0] write1set_reg_reg;
// LOCK_TEST_REG 寄存器 - 锁测试寄存器
reg [0:0] lock_test_reg_reg;

// CTRL_REG 字段寄存器
reg [0:0] ctrl_reg_enable_reg; // 使能位
reg [1:0] ctrl_reg_mode_reg; // 模式选择
reg [0:0] ctrl_reg_start_reg; // 启动位
// STATUS_REG 字段寄存器
reg [0:0] status_reg_busy_reg; // 忙状态标志
reg [0:0] status_reg_error_reg; // 错误标志
// INT_FLAG_REG 字段寄存器
reg [0:0] int_flag_reg_data_ready_reg; // 数据就绪中断
// LOCK_TEST_REG 字段寄存器
reg [7:0] lock_test_reg_locked_field_reg; // 受锁控制的字段
reg [7:0] lock_test_reg_magic_field_reg; // 魔数控制的字段

// =============================================================================
// 字段与寄存器连接
// =============================================================================

// CTRL_REG 寄存器组合
always @(*) begin
    ctrl_reg_reg = {         ctrl_reg_start_reg
,         ctrl_reg_mode_reg
,         ctrl_reg_enable_reg
 };
end

// CTRL_REG 字段接口连接
assign ctrl_reg_enable_o = ctrl_reg_enable_reg;
assign ctrl_reg_mode_o = ctrl_reg_mode_reg;
// STATUS_REG 寄存器组合
always @(*) begin
    status_reg_reg = {         status_reg_error_reg
,         status_reg_busy_reg
 };
end

// STATUS_REG 字段接口连接
assign status_reg_busy_o = status_reg_busy_reg;
assign status_reg_error_o = status_reg_error_reg;
// INT_FLAG_REG 寄存器组合
always @(*) begin
    int_flag_reg_reg = {         int_flag_reg_data_ready_reg
 };
end

// INT_FLAG_REG 字段接口连接
// LOCK_TEST_REG 寄存器组合
always @(*) begin
    lock_test_reg_reg = {         lock_test_reg_magic_field_reg
,         lock_test_reg_locked_field_reg
 };
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
        case (1'b1)  // 优先级编码器
            sel_ctrl_reg: read_data = ctrl_reg_reg;
            sel_status_reg: read_data = status_reg_reg;
            sel_int_flag_reg: read_data = int_flag_reg_reg;
            sel_write1set_reg: read_data = { 32'd0 | write1set_reg_reg };
            sel_lock_test_reg: read_data = lock_test_reg_reg;
            default: read_data = 32'd0;
        endcase
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
        if (write_active && sel_ctrl_reg) begin
            ctrl_reg_enable_reg <= write_data[0:0];
        end
        else if (ctrl_reg_enable_wen) begin
            ctrl_reg_enable_reg <= ctrl_reg_enable_i;
        end
    end
end
// MODE 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        ctrl_reg_mode_reg <= 2'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_ctrl_reg) begin
            ctrl_reg_mode_reg <= write_data[2:1];
        end
        else if (ctrl_reg_mode_wen) begin
            ctrl_reg_mode_reg <= ctrl_reg_mode_i;
        end
    end
end
// START 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        ctrl_reg_start_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_ctrl_reg) begin
            // 写1脉冲，下一个周期自动清零
            ctrl_reg_start_reg <= write_data[3:3];
        end
        else if (ctrl_reg_start_wen) begin
            ctrl_reg_start_reg <= ctrl_reg_start_i;
        end
        else begin
            // 脉冲类型字段在没有写入时自动清零
            ctrl_reg_start_reg <= 1'h0;
        end
    end
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
        if (write_active && sel_status_reg) begin
            // 只读字段，忽略软件写入
        end
        else if (status_reg_busy_wen) begin
            status_reg_busy_reg <= status_reg_busy_i;
        end
    end
end
// ERROR 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        status_reg_error_reg <= 1'h0;
    end
    else begin
        // 软件优先
        if (write_active && sel_status_reg) begin
            // 只读字段，忽略软件写入
        end
        else if (status_reg_error_wen) begin
            status_reg_error_reg <= status_reg_error_i;
        end
    end
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
        if (write_active && sel_int_flag_reg) begin
            int_flag_reg_data_ready_reg <= int_flag_reg_data_ready_reg & ~write_data[0:0];
        end
        else if (int_flag_reg_data_ready_wen) begin
            int_flag_reg_data_ready_reg <= int_flag_reg_data_ready_i;
        end
    end
end

// WRITEONLY_REG 寄存器 (无子字段)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonly_reg_reg <= 8'h00;
    end
    else begin
        // 软件优先
        if (write_active && sel_writeonly_reg) begin
            writeonly_reg_reg <= write_data[7:0];
        end
        else if (writeonly_reg_wen) begin
            writeonly_reg_reg <= writeonly_reg_i;
        end
    end
end

// WRITE1SET_REG 寄存器 (无子字段)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg_reg <= 8'h00;
    end
    else begin
        // 软件优先
        if (write_active && sel_write1set_reg) begin
            write1set_reg_reg <= write1set_reg_reg | write_data[7:0];
        end
        else if (write1set_reg_wen) begin
            write1set_reg_reg <= write1set_reg_i;
        end
    end
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
        if (write_active && sel_lock_test_reg) begin
            lock_test_reg_locked_field_reg <= write_data[7:0];
        end
        else if (lock_test_reg_locked_field_wen) begin
            lock_test_reg_locked_field_reg <= lock_test_reg_locked_field_i;
        end
    end
end
// MAGIC_FIELD 字段
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 使用字段特定的复位值或从寄存器复位值中提取
        lock_test_reg_magic_field_reg <= 8'hAA;
    end
    else begin
        // 软件优先
        if (write_active && sel_lock_test_reg) begin
            lock_test_reg_magic_field_reg <= write_data[15:8];
        end
        else if (lock_test_reg_magic_field_wen) begin
            lock_test_reg_magic_field_reg <= lock_test_reg_magic_field_i;
        end
    end
end

endmodule 