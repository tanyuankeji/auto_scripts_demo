// =============================================================================
// 自动生成的寄存器文件: separated_regfile
// 
// 生成时间: 
// 工具版本: 
// =============================================================================
`timescale 1ns / 1ps

module separated_regfile (
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
    // INT_FLAG_REG - 硬件写接口
    input wire [31:0] int_flag_reg_hwin,
    input wire int_flag_reg_hwen,

    // STATUS_REG.BUSY - 硬件写接口
    input wire status_reg_busy_hwin,
    input wire status_reg_busy_hwen,
    // STATUS_REG.ERROR - 硬件写接口
    input wire status_reg_error_hwin,
    input wire status_reg_error_hwen,
    // INT_FLAG_REG.DATA_READY - 硬件写接口
    input wire int_flag_reg_data_ready_hwin,
    input wire int_flag_reg_data_ready_hwen,

    // 测试端口（可选）
    input wire                         test_mode
);

// 地址定义
localparam ADDR_CTRL_REG = 8'h00;
localparam ADDR_STATUS_REG = 8'h04;
localparam ADDR_INT_FLAG_REG = 8'h08;
localparam ADDR_WRITEONLY_REG = 8'h0C;
localparam ADDR_WRITE1SET_REG = 8'h10;


// 内部信号定义
reg [7:0] wr_addr_0;
reg [31:0] wr_data_0;
reg                      wr_en_0;
reg [3:0] wr_be_0;

reg [7:0] rd_addr_0;
reg                      rd_en_0;
reg [31:0] rd_data_0;

// 寄存器声明
reg [31:0] ctrl_reg_reg;            // 控制寄存器
reg [31:0] status_reg_reg;          // 状态寄存器
reg [31:0] int_flag_reg_reg;        // 中断标志寄存器
reg [31:0] writeonly_reg_reg;       // 只写寄存器
reg [31:0] write1set_reg_reg;       // 写1置位寄存器



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

// INT_FLAG_REG 寄存器复位和更新逻辑
// 寄存器描述: 中断标志寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        int_flag_reg_reg <= 32'h00000000;
    end
    else begin
        // INT_FLAG_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_INT_FLAG_REG) begin
            if (wr_be_0[0]) int_flag_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) int_flag_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) int_flag_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) int_flag_reg_reg[31:24] <= wr_data_0[31:24];
        end
        // 硬件写逻辑
        else if (int_flag_reg_hwen) begin
            int_flag_reg_reg <= int_flag_reg_hwin;
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITEONLY_REG 寄存器复位和更新逻辑
// 寄存器描述: 只写寄存器
// 类型: WriteOnly
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonly_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITEONLY_REG 是 WriteOnly 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONLY_REG) begin
            if (wr_be_0[0]) writeonly_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonly_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) writeonly_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) writeonly_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITE1SET_REG 寄存器复位和更新逻辑
// 寄存器描述: 写1置位寄存器
// 类型: Write1Set
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE1SET_REG 是 Write1Set 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1SET_REG) begin
            if (wr_be_0[0]) write1set_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write1set_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) write1set_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) write1set_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end



// CTRL_REG.ENABLE 字段逻辑
// 位位置: [0:0]
// 描述: 使能位
// 功能: 系统使能控制
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


// CTRL_REG.MODE 字段逻辑
// 位位置: [2:1]
// 描述: 模式选择
// 功能: 00=空闲, 01=低功耗, 10=正常, 11=高性能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[2:1] <= 2'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg_reg[2:1] <= wr_data_0[2:1];
        end
        
        
        
    end
end


// CTRL_REG.START 字段逻辑
// 位位置: [3:3]
// 描述: 启动位
// 功能: 写1开始一次操作
// 类型: Write1Pulse
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ctrl_reg_reg[3] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_CTRL_REG) begin
            if (wr_be_0[0]) ctrl_reg_reg[3] <= wr_data_0[3];
        end
        
        
        
    end
end


// STATUS_REG.BUSY 字段逻辑
// 位位置: [0:0]
// 描述: 忙状态标志
// 功能: 指示系统当前是否正在运行
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


// STATUS_REG.ERROR 字段逻辑
// 位位置: [1:1]
// 描述: 错误标志
// 功能: 指示系统是否发生错误
// 类型: ReadOnly
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        status_reg_reg[1] <= 0;
    end
    else begin
        
        
        // 硬件写逻辑
        if (status_reg_error_hwen) begin
            status_reg_reg[1] <= status_reg_error_hwin;
        end
        
        
    end
end


// INT_FLAG_REG.DATA_READY 字段逻辑
// 位位置: [0:0]
// 描述: 数据就绪中断
// 功能: 数据准备就绪时置位，软件写1清零
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        int_flag_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_INT_FLAG_REG) begin
            if (wr_be_0[0]) int_flag_reg_reg[0] <= wr_data_0[0];
        end
        
        // 硬件写逻辑
        else if (int_flag_reg_data_ready_hwen) begin
            int_flag_reg_reg[0] <= int_flag_reg_data_ready_hwin;
        end
        
        
    end
end


// WRITE1SET_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: 写1置位的位字段
// 功能: 软件写1置位此位
// 类型: Write1Set
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1SET_REG) begin
            if (wr_be_0[0]) write1set_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// 总线接口逻辑
module separated_regfile (
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
    localparam ADDR_INT_FLAG_REG = 8'h0;
    localparam ADDR_WRITEONLY_REG = 8'h0;
    localparam ADDR_WRITE1SET_REG = 8'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] int_flag_reg_reg;
    reg [31:0] writeonly_reg_reg;
    reg [31:0] write1set_reg_reg;


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
            int_flag_reg_reg <= 32'h00000000;
            writeonly_reg_reg <= 32'h00000000;
            write1set_reg_reg <= 32'h00000000;
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
                    ADDR_INT_FLAG_REG: begin
                        // INT_FLAG_REG 是ReadWrite类型寄存器
                        int_flag_reg_reg <= pwdata;
                    end
                    ADDR_WRITEONLY_REG: begin
                        // WRITEONLY_REG 是WriteOnly类型寄存器
                        writeonly_reg_reg <= pwdata;
                    end
                    ADDR_WRITE1SET_REG: begin
                        // WRITE1SET_REG 是写1置位寄存器
                        write1set_reg_reg <= write1set_reg_reg | pwdata;
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
                ADDR_INT_FLAG_REG: begin
                    // INT_FLAG_REG 是可读寄存器
                    prdata = int_flag_reg_reg;
                end
                ADDR_WRITEONLY_REG: begin
                    // WRITEONLY_REG 是只写寄存器，读取返回0
                    prdata = 32'd0;
                end
                ADDR_WRITE1SET_REG: begin
                    // WRITE1SET_REG 是可读寄存器
                    prdata = write1set_reg_reg;
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
        ADDR_INT_FLAG_REG: begin
            rd_data_0 = int_flag_reg_reg;
        end
        ADDR_WRITEONLY_REG: begin
            rd_data_0 = 32'd0; // 只写寄存器，读取返回0
        end
        ADDR_WRITE1SET_REG: begin
            rd_data_0 = write1set_reg_reg;
        end
        default: rd_data_0 = 32'd0;
    endcase
end

endmodule 