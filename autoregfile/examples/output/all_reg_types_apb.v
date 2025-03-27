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
);

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