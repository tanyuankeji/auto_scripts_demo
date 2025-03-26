module apb_example (
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
    localparam ADDR_INTR_ENABLE_REG = 8'h0;
    localparam ADDR_INTR_STATUS_REG = 8'h0;
    localparam ADDR_DATA_REG = 8'h0;
    localparam ADDR_CONFIG_REG = 8'h0;
    localparam ADDR_PULSE_REG = 8'h0;
    localparam ADDR_VERSION_REG = 8'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] intr_enable_reg_reg;
    reg [31:0] intr_status_reg_reg;
    reg [31:0] data_reg_reg;
    reg [31:0] config_reg_reg;
    reg [31:0] pulse_reg_reg;
    reg [31:0] version_reg_reg;


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
            intr_enable_reg_reg <= 32'h00000000;
            intr_status_reg_reg <= 32'h00000000;
            data_reg_reg <= 32'h00000000;
            config_reg_reg <= 32'h00000000;
            pulse_reg_reg <= 32'h00000000;
            pulse_reg_pulse <= 32'd0;
            version_reg_reg <= 32'h00010000;
        end
        else begin
            // 默认清零脉冲信号
            pulse_reg_pulse <= 32'd0;
            
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
                    ADDR_INTR_ENABLE_REG: begin
                        // INTR_ENABLE_REG 是ReadWrite类型寄存器
                        intr_enable_reg_reg <= pwdata;
                    end
                    ADDR_INTR_STATUS_REG: begin
                        // INTR_STATUS_REG 是写1清零寄存器
                        intr_status_reg_reg <= intr_status_reg_reg & ~pwdata;
                    end
                    ADDR_DATA_REG: begin
                        // DATA_REG 是ReadWrite类型寄存器
                        data_reg_reg <= pwdata;
                    end
                    ADDR_CONFIG_REG: begin
                        // CONFIG_REG 是ReadWrite类型寄存器
                        if (!config_reg_locked) begin
                            config_reg_reg <= pwdata;
                        end
                    end
                    ADDR_PULSE_REG: begin
                        // PULSE_REG 是写1产生脉冲寄存器
                        pulse_reg_pulse <= pwdata;
                        pulse_reg_reg <= 32'd0;
                    end
                    ADDR_VERSION_REG: begin
                        // VERSION_REG 是只读寄存器，忽略写操作
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
                ADDR_INTR_ENABLE_REG: begin
                    // INTR_ENABLE_REG 是可读寄存器
                    prdata = intr_enable_reg_reg;
                end
                ADDR_INTR_STATUS_REG: begin
                    // INTR_STATUS_REG 是可读寄存器
                    prdata = intr_status_reg_reg;
                end
                ADDR_DATA_REG: begin
                    // DATA_REG 是可读寄存器
                    prdata = data_reg_reg;
                end
                ADDR_CONFIG_REG: begin
                    // CONFIG_REG 是可读寄存器
                    prdata = config_reg_reg;
                end
                ADDR_PULSE_REG: begin
                    // PULSE_REG 是可读寄存器
                    prdata = pulse_reg_reg;
                end
                ADDR_VERSION_REG: begin
                    // VERSION_REG 是可读寄存器
                    prdata = version_reg_reg;
                end
                default: begin
                    // 未知地址，返回0
                    prdata = 32'd0;
                end
            endcase
        end
    end

endmodule 