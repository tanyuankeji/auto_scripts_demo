module improved_hierarchical_regfile (
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
    localparam ADDR_LOCK_TEST_REG = 8'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] int_flag_reg_reg;
    reg [31:0] writeonly_reg_reg;
    reg [31:0] write1set_reg_reg;
    reg [31:0] lock_test_reg_reg;


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
            lock_test_reg_reg <= 32'h12345678;
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
                    ADDR_LOCK_TEST_REG: begin
                        // LOCK_TEST_REG 是ReadWrite类型寄存器
                        lock_test_reg_reg <= pwdata;
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
                ADDR_LOCK_TEST_REG: begin
                    // LOCK_TEST_REG 是可读寄存器
                    prdata = lock_test_reg_reg;
                end
                default: begin
                    // 未知地址，返回0
                    prdata = 32'd0;
                end
            endcase
        end
    end

endmodule 