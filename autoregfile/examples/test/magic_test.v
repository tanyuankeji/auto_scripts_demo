// =============================================================================
// 自动生成的寄存器文件: extended_field_regfile
// 
// 生成时间: 
// 工具版本: 
// =============================================================================
`timescale 1ns / 1ps

module extended_field_regfile (
    // 时钟和复位
    input wire                         clk,
    input wire                         rst_n,
    
    // 总线接口
    // APB总线接口
    input wire [7:0]  paddr,
    input wire                         psel,
    input wire                         penable,
    input wire                         pwrite,
    input wire [31:0]  pwdata,
    output reg [31:0]  prdata,
    output reg                         pready,
    output reg                         pslverr

    // 硬件接口
    // STATUS_REG - 硬件写接口
    input wire [31:0] status_reg_hwin,
    input wire status_reg_hwen,

    // STATUS_REG.BUSY - 硬件写接口
    input wire status_reg_busy_hwin,
    input wire status_reg_busy_hwen,

    // 测试端口（可选）
    input wire                         test_mode
);

// 地址定义
localparam ADDR_CTRL_REG = 8'h00;
localparam ADDR_STATUS_REG = 8'h04;
localparam ADDR_LOCK_REG = 8'h08;
localparam ADDR_MAGIC_REG = 8'h0C;


// 内部信号定义
reg [7:0] wr_addr_0;
reg [31:0] wr_data_0;
reg                      wr_en_0;
reg [3:0] wr_be_0;

reg [7:0] rd_addr_0;
reg                      rd_en_0;
reg [31:0] rd_data_0;
reg [7:0] rd_addr_1;
reg                      rd_en_1;
reg [31:0] rd_data_1;

// 寄存器声明
reg [31:0] ctrl_reg_reg;            // 控制寄存器
reg [31:0] status_reg_reg;          // 状态寄存器
reg [31:0] lock_reg_reg;            // 锁定寄存器
reg [31:0] magic_reg_reg;           // 魔术数字寄存器

// 锁定逻辑

// 魔术数字依赖逻辑

// 字段级魔术数字依赖
wire ctrl_reg_start_magic_valid;
assign ctrl_reg_start_magic_valid = magic_reg_reg == 0xDEADBEEF;

// 硬件访问输出连接


// CTRL_REG 寄存器复位和更新逻辑
// 寄存器描述: 控制寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg <= 32'h00000000;
    end
    else begin
        // CTRL_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) ctrl_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) ctrl_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) ctrl_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// STATUS_REG 寄存器复位和更新逻辑
// 寄存器描述: 状态寄存器
// 类型: ReadOnly
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        status_reg_reg <= 32'h00000000;
    end
    else begin
        // STATUS_REG 是只读寄存器，软件写操作被忽略
        // 硬件写逻辑
        if (status_reg_hwen) begin
            status_reg_reg <= status_reg_hwin;
        end

        // 读操作触发的特殊逻辑
    end
end

// LOCK_REG 寄存器复位和更新逻辑
// 寄存器描述: 锁定寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        lock_reg_reg <= 32'h00000000;
    end
    else begin
        // LOCK_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG) begin
            if (wr_be_0[0]) lock_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) lock_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) lock_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) lock_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// MAGIC_REG 寄存器复位和更新逻辑
// 寄存器描述: 魔术数字寄存器
// 类型: ReadWrite
// 默认值: 0xDEADBEEF
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        magic_reg_reg <= 32'hDEADBEEF;
    end
    else begin
        // MAGIC_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_MAGIC_REG) begin
            if (wr_be_0[0]) magic_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) magic_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) magic_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) magic_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end



// CTRL_REG.ENABLE 字段逻辑
// 位位置: [0:0]
// 描述: 使能位
// 功能: 控制系统工作使能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// CTRL_REG.START 字段逻辑
// 位位置: [1:1]
// 描述: 启动位
// 功能: 启动一次操作，需要验证魔术数字
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[1] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG && ctrl_reg_start_magic_valid) begin
            if (wr_be_0[0]) ctrl_reg_reg[1] <= wr_data_0[1];
        end
        
        
        
    end
end


// STATUS_REG.BUSY 字段逻辑
// 位位置: [0:0]
// 描述: 忙状态标志
// 功能: 表示系统当前正在工作中
// 类型: ReadOnly
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        status_reg_reg[0] <= 0;
    end
    else begin
        
        
        // 硬件写逻辑
        if (status_reg_busy_hwen) begin
            status_reg_reg[0] <= status_reg_busy_hwin;
        end
        
        
    end
end


// LOCK_REG.LOCK_BIT 字段逻辑
// 位位置: [0:0]
// 描述: 锁定位
// 功能: 锁定配置，防止意外修改
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        lock_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_LOCK_REG) begin
            if (wr_be_0[0]) lock_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// MAGIC_REG.MAGIC_VALUE 字段逻辑
// 位位置: [31:0]
// 描述: 魔术数字值
// 功能: 用于授权访问的魔术数字
// 类型: ReadWrite
// 默认值: 0xDEADBEEF
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        magic_reg_reg[31:0] <= 32'hDEADBEEF;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_MAGIC_REG) begin
            if (wr_be_0[0]) magic_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) magic_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) magic_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) magic_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// 总线接口逻辑
module extended_field_regfile (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // APB总线接口
    input  wire [7:0]   paddr,
    input  wire                     psel,
    input  wire                     penable,
    input  wire                     pwrite,
    input  wire [31:0]   pwdata,
    output reg  [31:0]   prdata,
    output wire                     pready,
    output wire                     pslverr
);

    // 地址常量定义
    localparam ADDR_CTRL_REG = 8'h0;
    localparam ADDR_STATUS_REG = 8'h0;
    localparam ADDR_LOCK_REG = 8'h0;
    localparam ADDR_MAGIC_REG = 8'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] lock_reg_reg;
    reg [31:0] magic_reg_reg;

    // 锁定逻辑

    // APB总线控制信号
    wire apb_write = psel && penable && pwrite;
    wire apb_read  = psel && !pwrite;
    
    // APB总线就绪信号 - 本设计总是准备好
    assign pready  = 1'b1;
    
    // APB总线错误信号 - 本设计不产生错误
    assign pslverr = 1'b0;
    
    // 寄存器写逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // 复位所有寄存器
            ctrl_reg_reg <= 32'h00000000;
            status_reg_reg <= 32'h00000000;
            lock_reg_reg <= 32'h00000000;
            magic_reg_reg <= 32'hDEADBEEF;
        end
        else begin
            // 默认清零脉冲信号
            
            // 写逻辑
            if (apb_write) begin
                case (paddr)
                    ADDR_CTRL_REG: begin
                        // CTRL_REG 是ReadWrite类型寄存器
                        ctrl_reg_reg <= pwdata;
                    end
                    ADDR_STATUS_REG: begin
                        // STATUS_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_LOCK_REG: begin
                        // LOCK_REG 是ReadWrite类型寄存器
                        lock_reg_reg <= pwdata;
                    end
                    ADDR_MAGIC_REG: begin
                        // MAGIC_REG 是ReadWrite类型寄存器
                        magic_reg_reg <= pwdata;
                    end
                    default: begin
                        // 未知地址，不做任何操作
                    end
                endcase
            end
            
            // 读操作触发的特殊逻辑
        end
    end
    
    // 寄存器读逻辑
    always @(*) begin
        prdata = 32'd0; // 默认值
        
        if (apb_read) begin
            case (paddr)
                ADDR_CTRL_REG: begin
                    // CTRL_REG 是可读寄存器
                    prdata = ctrl_reg_reg;
                end
                ADDR_STATUS_REG: begin
                    // STATUS_REG 是可读寄存器
                    prdata = status_reg_reg;
                end
                ADDR_LOCK_REG: begin
                    // LOCK_REG 是可读寄存器
                    prdata = lock_reg_reg;
                end
                ADDR_MAGIC_REG: begin
                    // MAGIC_REG 是可读寄存器
                    prdata = magic_reg_reg;
                end
                default: begin
                    // 未知地址，返回0
                    prdata = 32'd0;
                end
            endcase
        end
    end

endmodule 
// 读取逻辑
always @(*) begin
    rd_data_0 = 32'd0; // 默认值
    
    case (rd_addr_0)
        ADDR_CTRL_REG: begin
            rd_data_0 = ctrl_reg_reg;
        end
        ADDR_STATUS_REG: begin
            rd_data_0 = status_reg_reg;
        end
        ADDR_LOCK_REG: begin
            rd_data_0 = lock_reg_reg;
        end
        ADDR_MAGIC_REG: begin
            rd_data_0 = magic_reg_reg;
        end
        default: rd_data_0 = 32'd0;
    endcase
    rd_data_1 = 32'd0; // 默认值
    
    case (rd_addr_1)
        ADDR_CTRL_REG: begin
            rd_data_1 = ctrl_reg_reg;
        end
        ADDR_STATUS_REG: begin
            rd_data_1 = status_reg_reg;
        end
        ADDR_LOCK_REG: begin
            rd_data_1 = lock_reg_reg;
        end
        ADDR_MAGIC_REG: begin
            rd_data_1 = magic_reg_reg;
        end
        default: rd_data_1 = 32'd0;
    endcase
end

endmodule 