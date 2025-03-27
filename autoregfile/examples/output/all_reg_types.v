// =============================================================================
// 自动生成的寄存器文件: all_reg_types
// 
// 生成时间: 
// 工具版本: 
// =============================================================================
`timescale 1ns / 1ps

module all_reg_types (
    // 时钟和复位
    input wire                         clk,
    input wire                         rst_n,
    
    // 总线接口
    // APB总线接口
    input wire [9:0]  paddr,
    input wire                         psel,
    input wire                         penable,
    input wire                         pwrite,
    input wire [31:0]  pwdata,
    output reg [31:0]  prdata,
    output reg                         pready,
    output reg                         pslverr

    // 硬件接口


    // 测试端口（可选）
    input wire                         test_mode
);

// 地址定义
localparam ADDR_READWRITE_REG = 10'h00;
localparam ADDR_READONLY_REG = 10'h04;
localparam ADDR_WRITEONLY_REG = 10'h08;
localparam ADDR_WRITE1CLEAN_REG = 10'h0C;
localparam ADDR_WRITE1SET_REG = 10'h10;
localparam ADDR_WRITE0CLEAN_REG = 10'h14;
localparam ADDR_WRITE0SET_REG = 10'h18;
localparam ADDR_WRITEONCE_REG = 10'h1C;
localparam ADDR_WRITEONLYONCE_REG = 10'h20;
localparam ADDR_READCLEAN_REG = 10'h24;
localparam ADDR_READSET_REG = 10'h28;
localparam ADDR_WRITEREADCLEAN_REG = 10'h2C;
localparam ADDR_WRITEREADSET_REG = 10'h30;
localparam ADDR_WRITE1PULSE_REG = 10'h34;
localparam ADDR_WRITE0PULSE_REG = 10'h38;


// 内部信号定义
reg [9:0] wr_addr_0;
reg [31:0] wr_data_0;
reg                      wr_en_0;
reg [3:0] wr_be_0;

reg [9:0] rd_addr_0;
reg                      rd_en_0;
reg [31:0] rd_data_0;

// 寄存器声明
reg [31:0] readwrite_reg_reg;       // ReadWrite类型寄存器
reg [31:0] readonly_reg_reg;        // ReadOnly类型寄存器
reg [31:0] writeonly_reg_reg;       // WriteOnly类型寄存器
reg [31:0] write1clean_reg_reg;     // Write1Clean类型寄存器
reg [31:0] write1set_reg_reg;       // Write1Set类型寄存器
reg [31:0] write0clean_reg_reg;     // Write0Clean类型寄存器
reg [31:0] write0set_reg_reg;       // Write0Set类型寄存器
reg [31:0] writeonce_reg_reg;       // WriteOnce类型寄存器
reg        writeonce_reg_written;       // writeonce_reg 写标志
reg [31:0] writeonlyonce_reg_reg;   // WriteOnlyOnce类型寄存器
reg [31:0] readclean_reg_reg;       // ReadClean类型寄存器
reg [31:0] readset_reg_reg;         // ReadSet类型寄存器
reg [31:0] writereadclean_reg_reg;  // WriteReadClean类型寄存器
reg [31:0] writereadset_reg_reg;    // WriteReadSet类型寄存器
reg [31:0] write1pulse_reg_reg;     // Write1Pulse类型寄存器
// 脉冲寄存器声明（内部寄存器变量已在输出端口声明）
reg [31:0] write0pulse_reg_reg;     // Write0Pulse类型寄存器
// 脉冲寄存器声明（内部寄存器变量已在输出端口声明）



// 硬件访问输出连接


// READWRITE_REG 寄存器复位和更新逻辑
// 寄存器描述: ReadWrite类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readwrite_reg_reg <= 32'h00000000;
    end
    else begin
        // READWRITE_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_READWRITE_REG) begin
            if (wr_be_0[0]) readwrite_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readwrite_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) readwrite_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) readwrite_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// READONLY_REG 寄存器复位和更新逻辑
// 寄存器描述: ReadOnly类型寄存器
// 类型: ReadOnly
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readonly_reg_reg <= 32'h00000000;
    end
    else begin
        // READONLY_REG 是只读寄存器，软件写操作被忽略

        // 读操作触发的特殊逻辑
    end
end

// WRITEONLY_REG 寄存器复位和更新逻辑
// 寄存器描述: WriteOnly类型寄存器
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

// WRITE1CLEAN_REG 寄存器复位和更新逻辑
// 寄存器描述: Write1Clean类型寄存器
// 类型: Write1Clean
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1clean_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE1CLEAN_REG 是 Write1Clean 类型寄存器，写1清零对应位
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) write1clean_reg_reg[7:0] <= write1clean_reg_reg[7:0] & ~wr_data_0[7:0];
            if (wr_be_0[1]) write1clean_reg_reg[15:8] <= write1clean_reg_reg[15:8] & ~wr_data_0[15:8];
            if (wr_be_0[2]) write1clean_reg_reg[23:16] <= write1clean_reg_reg[23:16] & ~wr_data_0[23:16];
            if (wr_be_0[3]) write1clean_reg_reg[31:24] <= write1clean_reg_reg[31:24] & ~wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITE1SET_REG 寄存器复位和更新逻辑
// 寄存器描述: Write1Set类型寄存器
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

// WRITE0CLEAN_REG 寄存器复位和更新逻辑
// 寄存器描述: Write0Clean类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0clean_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE0CLEAN_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0CLEAN_REG) begin
            if (wr_be_0[0]) write0clean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0clean_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) write0clean_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) write0clean_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITE0SET_REG 寄存器复位和更新逻辑
// 寄存器描述: Write0Set类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0set_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE0SET_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0SET_REG) begin
            if (wr_be_0[0]) write0set_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0set_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) write0set_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) write0set_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITEONCE_REG 寄存器复位和更新逻辑
// 寄存器描述: WriteOnce类型寄存器
// 类型: WriteOnce
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonce_reg_reg <= 32'h00000000;
        writeonce_reg_written <= 1'b0;
    end
    else begin
        // WRITEONCE_REG 是 WriteOnce 类型寄存器，只写一次
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONCE_REG && !writeonce_reg_written) begin
            if (wr_be_0[0]) writeonce_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonce_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) writeonce_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) writeonce_reg_reg[31:24] <= wr_data_0[31:24];
            writeonce_reg_written <= 1'b1; // 设置写标志
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITEONLYONCE_REG 寄存器复位和更新逻辑
// 寄存器描述: WriteOnlyOnce类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonlyonce_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITEONLYONCE_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONLYONCE_REG) begin
            if (wr_be_0[0]) writeonlyonce_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonlyonce_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) writeonlyonce_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) writeonlyonce_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// READCLEAN_REG 寄存器复位和更新逻辑
// 寄存器描述: ReadClean类型寄存器
// 类型: ReadClean
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readclean_reg_reg <= 32'h00000000;
    end
    else begin
        // READCLEAN_REG 是 ReadClean 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_READCLEAN_REG) begin
            if (wr_be_0[0]) readclean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readclean_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) readclean_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) readclean_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
        // 如果读端口读取了READCLEAN_REG，则清零（ReadClean类型）
        if (rd_addr_0 == ADDR_READCLEAN_REG) begin
            if (rd_addr_0 == ADDR_READCLEAN_REG) 
                readclean_reg_reg <= 32'd0;
        end
    end
end

// READSET_REG 寄存器复位和更新逻辑
// 寄存器描述: ReadSet类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readset_reg_reg <= 32'h00000000;
    end
    else begin
        // READSET_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_READSET_REG) begin
            if (wr_be_0[0]) readset_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readset_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) readset_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) readset_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITEREADCLEAN_REG 寄存器复位和更新逻辑
// 寄存器描述: WriteReadClean类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writereadclean_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITEREADCLEAN_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEREADCLEAN_REG) begin
            if (wr_be_0[0]) writereadclean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writereadclean_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) writereadclean_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) writereadclean_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITEREADSET_REG 寄存器复位和更新逻辑
// 寄存器描述: WriteReadSet类型寄存器
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writereadset_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITEREADSET_REG 是 ReadWrite 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEREADSET_REG) begin
            if (wr_be_0[0]) writereadset_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writereadset_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) writereadset_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) writereadset_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITE1PULSE_REG 寄存器复位和更新逻辑
// 寄存器描述: Write1Pulse类型寄存器
// 类型: Write1Pulse
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1pulse_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE1PULSE_REG 是 Write1Pulse 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1PULSE_REG) begin
            if (wr_be_0[0]) write1pulse_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write1pulse_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) write1pulse_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) write1pulse_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end

// WRITE0PULSE_REG 寄存器复位和更新逻辑
// 寄存器描述: Write0Pulse类型寄存器
// 类型: Write0Pulse
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0pulse_reg_reg <= 32'h00000000;
    end
    else begin
        // WRITE0PULSE_REG 是 Write0Pulse 类型寄存器
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0PULSE_REG) begin
            if (wr_be_0[0]) write0pulse_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0pulse_reg_reg[15:8] <= wr_data_0[15:8];
            if (wr_be_0[2]) write0pulse_reg_reg[23:16] <= wr_data_0[23:16];
            if (wr_be_0[3]) write0pulse_reg_reg[31:24] <= wr_data_0[31:24];
        end

        // 读操作触发的特殊逻辑
    end
end



// READWRITE_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: ReadWrite类型字段
// 功能: 测试ReadWrite功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readwrite_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_READWRITE_REG) begin
            if (wr_be_0[0]) readwrite_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readwrite_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) readwrite_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) readwrite_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// READONLY_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: ReadOnly类型字段
// 功能: 测试ReadOnly功能
// 类型: ReadOnly
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readonly_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        
        
        
    end
end


// WRITEONLY_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: WriteOnly类型字段
// 功能: 测试WriteOnly功能
// 类型: WriteOnly
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonly_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONLY_REG) begin
            if (wr_be_0[0]) writeonly_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonly_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) writeonly_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) writeonly_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE1CLEAN_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write1Clean类型字段
// 功能: 测试Write1Clean功能
// 类型: Write1Clean
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1clean_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) write1clean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write1clean_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write1clean_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write1clean_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        // 写1清零逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) 
                write1clean_reg_reg[7:0] <= 
                    write1clean_reg_reg[7:0] & 
                    ~(wr_data_0[7:0]);
            if (wr_be_0[1]) 
                write1clean_reg_reg[15:8] <= 
                    write1clean_reg_reg[15:8] & 
                    ~(wr_data_0[7:0]);
            if (wr_be_0[2]) 
                write1clean_reg_reg[23:16] <= 
                    write1clean_reg_reg[23:16] & 
                    ~(wr_data_0[7:0]);
            if (wr_be_0[3]) 
                write1clean_reg_reg[31:24] <= 
                    write1clean_reg_reg[31:24] & 
                    ~(wr_data_0[7:0]);
        end
        
    end
end


// WRITE1CLEAN_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write1Clean位字段
// 功能: 测试Write1Clean位功能
// 类型: Write1Clean
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1clean_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) write1clean_reg_reg[0] <= wr_data_0[0];
        end
        
        
        // 写1清零逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0] && wr_data_0[0]) 
                write1clean_reg_reg[0] <= 1'b0;
        end
        
    end
end


// WRITE1CLEAN_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write1Clean多位字段
// 功能: 测试Write1Clean多位功能
// 类型: Write1Clean
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1clean_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) write1clean_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        // 写1清零逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1CLEAN_REG) begin
            if (wr_be_0[0]) 
                write1clean_reg_reg[4:1] <= 
                    write1clean_reg_reg[4:1] & 
                    ~(wr_data_0[4:1]);
        end
        
    end
end


// WRITE1SET_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write1Set类型字段
// 功能: 测试Write1Set功能
// 类型: Write1Set
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1SET_REG) begin
            if (wr_be_0[0]) write1set_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write1set_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write1set_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write1set_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE1SET_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write1Set位字段
// 功能: 测试Write1Set位功能
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


// WRITE1SET_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write1Set多位字段
// 功能: 测试Write1Set多位功能
// 类型: Write1Set
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1set_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1SET_REG) begin
            if (wr_be_0[0]) write1set_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        
    end
end


// WRITE0CLEAN_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write0Clean类型字段
// 功能: 测试Write0Clean功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0clean_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0CLEAN_REG) begin
            if (wr_be_0[0]) write0clean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0clean_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write0clean_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write0clean_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE0CLEAN_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write0Clean位字段
// 功能: 测试Write0Clean位功能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0clean_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0CLEAN_REG) begin
            if (wr_be_0[0]) write0clean_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// WRITE0CLEAN_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write0Clean多位字段
// 功能: 测试Write0Clean多位功能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0clean_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0CLEAN_REG) begin
            if (wr_be_0[0]) write0clean_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        
    end
end


// WRITE0SET_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write0Set类型字段
// 功能: 测试Write0Set功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0set_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0SET_REG) begin
            if (wr_be_0[0]) write0set_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0set_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write0set_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write0set_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE0SET_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write0Set位字段
// 功能: 测试Write0Set位功能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0set_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0SET_REG) begin
            if (wr_be_0[0]) write0set_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// WRITE0SET_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write0Set多位字段
// 功能: 测试Write0Set多位功能
// 类型: ReadWrite
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0set_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0SET_REG) begin
            if (wr_be_0[0]) write0set_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        
    end
end


// WRITEONCE_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: WriteOnce类型字段
// 功能: 测试WriteOnce功能
// 类型: WriteOnce
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonce_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONCE_REG) begin
            if (wr_be_0[0]) writeonce_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonce_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) writeonce_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) writeonce_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITEONLYONCE_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: WriteOnlyOnce类型字段
// 功能: 测试WriteOnlyOnce功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writeonlyonce_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEONLYONCE_REG) begin
            if (wr_be_0[0]) writeonlyonce_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writeonlyonce_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) writeonlyonce_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) writeonlyonce_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// READCLEAN_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: ReadClean类型字段
// 功能: 测试ReadClean功能
// 类型: ReadClean
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readclean_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_READCLEAN_REG) begin
            if (wr_be_0[0]) readclean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readclean_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) readclean_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) readclean_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
        // 读取后自动清零
        if (rd_addr_0 == ADDR_READCLEAN_REG) begin
            readclean_reg_reg[31:0] <= 32'd0;
        end
    end
end


// READSET_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: ReadSet类型字段
// 功能: 测试ReadSet功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        readset_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_READSET_REG) begin
            if (wr_be_0[0]) readset_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) readset_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) readset_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) readset_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITEREADCLEAN_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: WriteReadClean类型字段
// 功能: 测试WriteReadClean功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writereadclean_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEREADCLEAN_REG) begin
            if (wr_be_0[0]) writereadclean_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writereadclean_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) writereadclean_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) writereadclean_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITEREADSET_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: WriteReadSet类型字段
// 功能: 测试WriteReadSet功能
// 类型: ReadWrite
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        writereadset_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITEREADSET_REG) begin
            if (wr_be_0[0]) writereadset_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) writereadset_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) writereadset_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) writereadset_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE1PULSE_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write1Pulse类型字段
// 功能: 测试Write1Pulse功能
// 类型: Write1Pulse
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1pulse_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1PULSE_REG) begin
            if (wr_be_0[0]) write1pulse_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write1pulse_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write1pulse_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write1pulse_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE1PULSE_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write1Pulse位字段
// 功能: 测试Write1Pulse位功能
// 类型: Write1Pulse
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1pulse_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1PULSE_REG) begin
            if (wr_be_0[0]) write1pulse_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// WRITE1PULSE_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write1Pulse多位字段
// 功能: 测试Write1Pulse多位功能
// 类型: Write1Pulse
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write1pulse_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE1PULSE_REG) begin
            if (wr_be_0[0]) write1pulse_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        
    end
end


// WRITE0PULSE_REG.VALUE 字段逻辑
// 位位置: [31:0]
// 描述: Write0Pulse类型字段
// 功能: 测试Write0Pulse功能
// 类型: Write0Pulse
// 默认值: 0x00000000
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0pulse_reg_reg[31:0] <= 32'h00000000;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0PULSE_REG) begin
            if (wr_be_0[0]) write0pulse_reg_reg[7:0] <= wr_data_0[7:0];
            if (wr_be_0[1]) write0pulse_reg_reg[15:8] <= wr_data_0[7:0];
            if (wr_be_0[2]) write0pulse_reg_reg[23:16] <= wr_data_0[7:0];
            if (wr_be_0[3]) write0pulse_reg_reg[31:24] <= wr_data_0[7:0];
        end
        
        
        
    end
end


// WRITE0PULSE_REG.BIT0 字段逻辑
// 位位置: [0:0]
// 描述: Write0Pulse位字段
// 功能: 测试Write0Pulse位功能
// 类型: Write0Pulse
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0pulse_reg_reg[0] <= 0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0PULSE_REG) begin
            if (wr_be_0[0]) write0pulse_reg_reg[0] <= wr_data_0[0];
        end
        
        
        
    end
end


// WRITE0PULSE_REG.BITS 字段逻辑
// 位位置: [4:1]
// 描述: Write0Pulse多位字段
// 功能: 测试Write0Pulse多位功能
// 类型: Write0Pulse
// 默认值: 0
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write0pulse_reg_reg[4:1] <= 4'd0;
    end
    else begin
        
        // 软件写逻辑
        if (wr_en_0 && wr_addr_0 == ADDR_WRITE0PULSE_REG) begin
            if (wr_be_0[0]) write0pulse_reg_reg[4:1] <= wr_data_0[4:1];
        end
        
        
        
    end
end


// 总线接口逻辑
module all_reg_types (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // APB总线接口
    input  wire [9:0]   paddr,
    input  wire                     psel,
    input  wire                     penable,
    input  wire                     pwrite,
    input  wire [31:0]   pwdata,
    output reg  [31:0]   prdata,
    output wire                     pready,
    output wire                     pslverr
    ,
    // 脉冲输出信号
    output reg  [31:0]   write1pulse_reg_pulse,    output reg  [31:0]   write0pulse_reg_pulse);

    // 地址常量定义
    localparam ADDR_READWRITE_REG = 10'h0;
    localparam ADDR_READONLY_REG = 10'h0;
    localparam ADDR_WRITEONLY_REG = 10'h0;
    localparam ADDR_WRITE1CLEAN_REG = 10'h0;
    localparam ADDR_WRITE1SET_REG = 10'h0;
    localparam ADDR_WRITE0CLEAN_REG = 10'h0;
    localparam ADDR_WRITE0SET_REG = 10'h0;
    localparam ADDR_WRITEONCE_REG = 10'h0;
    localparam ADDR_WRITEONLYONCE_REG = 10'h0;
    localparam ADDR_READCLEAN_REG = 10'h0;
    localparam ADDR_READSET_REG = 10'h0;
    localparam ADDR_WRITEREADCLEAN_REG = 10'h0;
    localparam ADDR_WRITEREADSET_REG = 10'h0;
    localparam ADDR_WRITE1PULSE_REG = 10'h0;
    localparam ADDR_WRITE0PULSE_REG = 10'h0;

    // 寄存器定义
    reg [31:0] readwrite_reg_reg;
    reg [31:0] readonly_reg_reg;
    reg [31:0] writeonly_reg_reg;
    reg [31:0] write1clean_reg_reg;
    reg [31:0] write1set_reg_reg;
    reg [31:0] write0clean_reg_reg;
    reg [31:0] write0set_reg_reg;
    reg [31:0] writeonce_reg_reg;
    reg        writeonce_reg_written;
    reg [31:0] writeonlyonce_reg_reg;
    reg [31:0] readclean_reg_reg;
    reg [31:0] readset_reg_reg;
    reg [31:0] writereadclean_reg_reg;
    reg [31:0] writereadset_reg_reg;
    reg [31:0] write1pulse_reg_reg;
    reg [31:0] write0pulse_reg_reg;


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
            readwrite_reg_reg <= 32'h00000000;
            readonly_reg_reg <= 32'h00000000;
            writeonly_reg_reg <= 32'h00000000;
            write1clean_reg_reg <= 32'h00000000;
            write1set_reg_reg <= 32'h00000000;
            write0clean_reg_reg <= 32'h00000000;
            write0set_reg_reg <= 32'h00000000;
            writeonce_reg_reg <= 32'h00000000;
            writeonce_reg_written <= 1'b0;
            writeonlyonce_reg_reg <= 32'h00000000;
            readclean_reg_reg <= 32'h00000000;
            readset_reg_reg <= 32'h00000000;
            writereadclean_reg_reg <= 32'h00000000;
            writereadset_reg_reg <= 32'h00000000;
            write1pulse_reg_reg <= 32'h00000000;
            write1pulse_reg_pulse <= 32'd0;
            write0pulse_reg_reg <= 32'h00000000;
            write0pulse_reg_pulse <= 32'd0;
        end
        else begin
            // 默认清零脉冲信号
            write1pulse_reg_pulse <= 32'd0;
            write0pulse_reg_pulse <= 32'd0;
            
            // 写逻辑
            if (apb_write) begin
                case (paddr)
                    ADDR_READWRITE_REG: begin
                        // READWRITE_REG 是ReadWrite类型寄存器
                        readwrite_reg_reg <= pwdata;
                    end
                    ADDR_READONLY_REG: begin
                        // READONLY_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_WRITEONLY_REG: begin
                        // WRITEONLY_REG 是WriteOnly类型寄存器
                        writeonly_reg_reg <= pwdata;
                    end
                    ADDR_WRITE1CLEAN_REG: begin
                        // WRITE1CLEAN_REG 是写1清零寄存器
                        write1clean_reg_reg <= write1clean_reg_reg & ~pwdata;
                    end
                    ADDR_WRITE1SET_REG: begin
                        // WRITE1SET_REG 是写1置位寄存器
                        write1set_reg_reg <= write1set_reg_reg | pwdata;
                    end
                    ADDR_WRITE0CLEAN_REG: begin
                        // WRITE0CLEAN_REG 是ReadWrite类型寄存器
                        write0clean_reg_reg <= pwdata;
                    end
                    ADDR_WRITE0SET_REG: begin
                        // WRITE0SET_REG 是ReadWrite类型寄存器
                        write0set_reg_reg <= pwdata;
                    end
                    ADDR_WRITEONCE_REG: begin
                        // WRITEONCE_REG 是只写一次寄存器
                        if (!writeonce_reg_written) begin
                            writeonce_reg_reg <= pwdata;
                            writeonce_reg_written <= 1'b1;
                        end
                    end
                    ADDR_WRITEONLYONCE_REG: begin
                        // WRITEONLYONCE_REG 是ReadWrite类型寄存器
                        writeonlyonce_reg_reg <= pwdata;
                    end
                    ADDR_READCLEAN_REG: begin
                        // READCLEAN_REG 是ReadClean类型寄存器
                        readclean_reg_reg <= pwdata;
                    end
                    ADDR_READSET_REG: begin
                        // READSET_REG 是ReadWrite类型寄存器
                        readset_reg_reg <= pwdata;
                    end
                    ADDR_WRITEREADCLEAN_REG: begin
                        // WRITEREADCLEAN_REG 是ReadWrite类型寄存器
                        writereadclean_reg_reg <= pwdata;
                    end
                    ADDR_WRITEREADSET_REG: begin
                        // WRITEREADSET_REG 是ReadWrite类型寄存器
                        writereadset_reg_reg <= pwdata;
                    end
                    ADDR_WRITE1PULSE_REG: begin
                        // WRITE1PULSE_REG 是写1产生脉冲寄存器
                        write1pulse_reg_pulse <= pwdata;
                        write1pulse_reg_reg <= 32'd0;
                    end
                    ADDR_WRITE0PULSE_REG: begin
                        // WRITE0PULSE_REG 是写0产生脉冲寄存器
                        write0pulse_reg_pulse <= ~pwdata;
                        write0pulse_reg_reg <= 32'd0;
                    end
                    default: begin
                        // 未知地址，不做任何操作
                    end
                endcase
            end
            
            // 读操作触发的特殊逻辑
            // 如果读取了READCLEAN_REG，则清零（ReadClean类型）
            if (apb_read && paddr == ADDR_READCLEAN_REG) begin
                readclean_reg_reg <= 32'd0;
            end
        end
    end
    
    // 寄存器读逻辑
    always @(*) begin
        prdata = 32'd0; // 默认值
        
        if (apb_read) begin
            case (paddr)
                ADDR_READWRITE_REG: begin
                    // READWRITE_REG 是可读寄存器
                    prdata = readwrite_reg_reg;
                end
                ADDR_READONLY_REG: begin
                    // READONLY_REG 是可读寄存器
                    prdata = readonly_reg_reg;
                end
                ADDR_WRITEONLY_REG: begin
                    // WRITEONLY_REG 是只写寄存器，读取返回0
                    prdata = 32'd0;
                end
                ADDR_WRITE1CLEAN_REG: begin
                    // WRITE1CLEAN_REG 是可读寄存器
                    prdata = write1clean_reg_reg;
                end
                ADDR_WRITE1SET_REG: begin
                    // WRITE1SET_REG 是可读寄存器
                    prdata = write1set_reg_reg;
                end
                ADDR_WRITE0CLEAN_REG: begin
                    // WRITE0CLEAN_REG 是可读寄存器
                    prdata = write0clean_reg_reg;
                end
                ADDR_WRITE0SET_REG: begin
                    // WRITE0SET_REG 是可读寄存器
                    prdata = write0set_reg_reg;
                end
                ADDR_WRITEONCE_REG: begin
                    // WRITEONCE_REG 是可读寄存器
                    prdata = writeonce_reg_reg;
                end
                ADDR_WRITEONLYONCE_REG: begin
                    // WRITEONLYONCE_REG 是可读寄存器
                    prdata = writeonlyonce_reg_reg;
                end
                ADDR_READCLEAN_REG: begin
                    // READCLEAN_REG 是可读寄存器
                    prdata = readclean_reg_reg;
                end
                ADDR_READSET_REG: begin
                    // READSET_REG 是可读寄存器
                    prdata = readset_reg_reg;
                end
                ADDR_WRITEREADCLEAN_REG: begin
                    // WRITEREADCLEAN_REG 是可读寄存器
                    prdata = writereadclean_reg_reg;
                end
                ADDR_WRITEREADSET_REG: begin
                    // WRITEREADSET_REG 是可读寄存器
                    prdata = writereadset_reg_reg;
                end
                ADDR_WRITE1PULSE_REG: begin
                    // WRITE1PULSE_REG 是可读寄存器
                    prdata = write1pulse_reg_reg;
                end
                ADDR_WRITE0PULSE_REG: begin
                    // WRITE0PULSE_REG 是可读寄存器
                    prdata = write0pulse_reg_reg;
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
        ADDR_READWRITE_REG: begin
            rd_data_0 = readwrite_reg_reg;
        end
        ADDR_READONLY_REG: begin
            rd_data_0 = readonly_reg_reg;
        end
        ADDR_WRITEONLY_REG: begin
            rd_data_0 = 32'd0; // 只写寄存器，读取返回0
        end
        ADDR_WRITE1CLEAN_REG: begin
            rd_data_0 = write1clean_reg_reg;
        end
        ADDR_WRITE1SET_REG: begin
            rd_data_0 = write1set_reg_reg;
        end
        ADDR_WRITE0CLEAN_REG: begin
            rd_data_0 = write0clean_reg_reg;
        end
        ADDR_WRITE0SET_REG: begin
            rd_data_0 = write0set_reg_reg;
        end
        ADDR_WRITEONCE_REG: begin
            rd_data_0 = writeonce_reg_reg;
        end
        ADDR_WRITEONLYONCE_REG: begin
            rd_data_0 = writeonlyonce_reg_reg;
        end
        ADDR_READCLEAN_REG: begin
            rd_data_0 = readclean_reg_reg;
        end
        ADDR_READSET_REG: begin
            rd_data_0 = readset_reg_reg;
        end
        ADDR_WRITEREADCLEAN_REG: begin
            rd_data_0 = writereadclean_reg_reg;
        end
        ADDR_WRITEREADSET_REG: begin
            rd_data_0 = writereadset_reg_reg;
        end
        ADDR_WRITE1PULSE_REG: begin
            rd_data_0 = write1pulse_reg_reg;
        end
        ADDR_WRITE0PULSE_REG: begin
            rd_data_0 = write0pulse_reg_reg;
        end
        default: rd_data_0 = 32'd0;
    endcase
end

endmodule 