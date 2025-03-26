module auto_addr_example (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // 自定义总线接口
    input  wire [7:0]   addr,
    input  wire                     chip_select,
    input  wire                     write_en,
    input  wire                     read_en,
    input  wire [31:0]   write_data,
    output reg  [31:0]   read_data,
    output wire                     data_valid
);

    // 地址常量定义
    localparam ADDR_CTRL_REG = 8'h0;
    localparam ADDR_STATUS_REG = 8'h0;
    localparam ADDR_INTR_REG = 8'h0;
    localparam ADDR_CONFIG1_REG = 8'h0;
    localparam ADDR_CONFIG2_REG = 8'h0;
    localparam ADDR_VERSION_REG = 8'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] intr_reg_reg;
    reg [31:0] config1_reg_reg;
    reg [31:0] config2_reg_reg;
    reg [31:0] version_reg_reg;


    // 总线控制信号
    wire write_active = chip_select && write_en;
    wire read_active  = chip_select && read_en;
    
    // 数据有效信号（读操作完成）
    reg  read_valid_reg;
    assign data_valid = read_valid_reg;
    
    // 寄存器写逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // 复位所有寄存器
            ctrl_reg_reg <= 32'h00000000;
            status_reg_reg <= 32'h00000000;
            intr_reg_reg <= 32'h00000000;
            config1_reg_reg <= 32'h00000000;
            config2_reg_reg <= 32'h00000000;
            version_reg_reg <= 32'h00010000;
        end
        else begin
            // 默认清零脉冲信号
            
            // 写逻辑
            if (write_active) begin
                case (addr)
                    ADDR_CTRL_REG: begin
                        // CTRL_REG 是ReadWrite类型寄存器
                        ctrl_reg_reg <= write_data;
                    end
                    ADDR_STATUS_REG: begin
                        // STATUS_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_INTR_REG: begin
                        // INTR_REG 是写1清零寄存器
                        intr_reg_reg <= intr_reg_reg & ~write_data;
                    end
                    ADDR_CONFIG1_REG: begin
                        // CONFIG1_REG 是ReadWrite类型寄存器
                        config1_reg_reg <= write_data;
                    end
                    ADDR_CONFIG2_REG: begin
                        // CONFIG2_REG 是ReadWrite类型寄存器
                        config2_reg_reg <= write_data;
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
    
    // 数据有效信号逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            read_valid_reg <= 1'b0;
        end
        else begin
            read_valid_reg <= read_active;
        end
    end
    
    // 寄存器读逻辑
    always @(*) begin
        read_data = 32'd0; // 默认值
        
        if (read_active) begin
            case (addr)
                ADDR_CTRL_REG: begin
                    // CTRL_REG 是可读寄存器
                    read_data = ctrl_reg_reg;
                end
                ADDR_STATUS_REG: begin
                    // STATUS_REG 是可读寄存器
                    read_data = status_reg_reg;
                end
                ADDR_INTR_REG: begin
                    // INTR_REG 是可读寄存器
                    read_data = intr_reg_reg;
                end
                ADDR_CONFIG1_REG: begin
                    // CONFIG1_REG 是可读寄存器
                    read_data = config1_reg_reg;
                end
                ADDR_CONFIG2_REG: begin
                    // CONFIG2_REG 是可读寄存器
                    read_data = config2_reg_reg;
                end
                ADDR_VERSION_REG: begin
                    // VERSION_REG 是可读寄存器
                    read_data = version_reg_reg;
                end
                default: begin
                    // 未知地址，返回0
                    read_data = 32'd0;
                end
            endcase
        end
    end

endmodule 