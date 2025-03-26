module axi_lite_example (
    // 系统信号
    input  wire                     clk,
    input  wire                     rst_n,
    
    // AXI-Lite写地址通道
    input  wire [11:0]   s_axil_awaddr,
    input  wire                     s_axil_awvalid,
    output reg                      s_axil_awready,
    
    // AXI-Lite写数据通道
    input  wire [31:0]   s_axil_wdata,
    input  wire [3:0]  s_axil_wstrb,
    input  wire                     s_axil_wvalid,
    output reg                      s_axil_wready,
    
    // AXI-Lite写响应通道
    output reg  [1:0]               s_axil_bresp,
    output reg                      s_axil_bvalid,
    input  wire                     s_axil_bready,
    
    // AXI-Lite读地址通道
    input  wire [11:0]   s_axil_araddr,
    input  wire                     s_axil_arvalid,
    output reg                      s_axil_arready,
    
    // AXI-Lite读数据通道
    output reg  [31:0]   s_axil_rdata,
    output reg  [1:0]               s_axil_rresp,
    output reg                      s_axil_rvalid,
    input  wire                     s_axil_rready
);

    // AXI-Lite响应类型常量
    localparam RESP_OKAY   = 2'b00;  // 成功
    localparam RESP_EXOKAY = 2'b01;  // 排他访问成功
    localparam RESP_SLVERR = 2'b10;  // 从设备错误
    localparam RESP_DECERR = 2'b11;  // 解码错误

    // 地址常量定义
    localparam ADDR_CTRL_REG = 12'h0;
    localparam ADDR_STATUS_REG = 12'h0;
    localparam ADDR_INTR_ENABLE_REG = 12'h0;
    localparam ADDR_INTR_STATUS_REG = 12'h0;
    localparam ADDR_TX_DATA_REG = 12'h0;
    localparam ADDR_RX_DATA_REG = 12'h0;
    localparam ADDR_CONFIG1_REG = 12'h0;
    localparam ADDR_CONFIG2_REG = 12'h0;
    localparam ADDR_TRIGGER_REG = 12'h0;
    localparam ADDR_ERROR_CODE_REG = 12'h0;
    localparam ADDR_VERSION_REG = 12'h0;
    localparam ADDR_ID_REG = 12'h0;

    // 寄存器定义
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] intr_enable_reg_reg;
    reg [31:0] intr_status_reg_reg;
    reg [31:0] tx_data_reg_reg;
    reg [31:0] rx_data_reg_reg;
    reg [31:0] config1_reg_reg;
    reg [31:0] config2_reg_reg;
    reg [31:0] trigger_reg_reg;
    reg [31:0] error_code_reg_reg;
    reg [31:0] version_reg_reg;
    reg [31:0] id_reg_reg;


    // 写操作相关状态
    reg [11:0] write_addr;
    reg                     write_addr_valid;
    reg [31:0] write_data;
    reg [3:0] write_strb;
    reg                     write_data_valid;
    reg                     write_resp_pending;
    
    // 读操作相关状态
    reg [11:0] read_addr;
    reg                     read_addr_valid;
    reg                     read_resp_pending;
    
    // 写地址通道处理
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s_axil_awready <= 1'b1;
            write_addr <= 12'd0;
            write_addr_valid <= 1'b0;
        end 
        else begin
            // 如果总线提供了有效的写地址，且从设备准备好接收
            if (s_axil_awvalid && s_axil_awready) begin
                write_addr <= s_axil_awaddr;
                write_addr_valid <= 1'b1;
                s_axil_awready <= 1'b0;  // 表示已接收地址
            end
            // 如果写响应已完成，准备接收新的地址
            else if (s_axil_bvalid && s_axil_bready) begin
                write_addr_valid <= 1'b0;
                s_axil_awready <= 1'b1;
            end
        end
    end
    
    // 写数据通道处理
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s_axil_wready <= 1'b1;
            write_data <= 32'd0;
            write_strb <= 4'd0;
            write_data_valid <= 1'b0;
        end 
        else begin
            // 如果总线提供了有效的写数据，且从设备准备好接收
            if (s_axil_wvalid && s_axil_wready) begin
                write_data <= s_axil_wdata;
                write_strb <= s_axil_wstrb;
                write_data_valid <= 1'b1;
                s_axil_wready <= 1'b0;  // 表示已接收数据
            end
            // 如果写响应已完成，准备接收新的数据
            else if (s_axil_bvalid && s_axil_bready) begin
                write_data_valid <= 1'b0;
                s_axil_wready <= 1'b1;
            end
        end
    end
    
    // 写响应通道处理
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s_axil_bvalid <= 1'b0;
            s_axil_bresp <= RESP_OKAY;
            write_resp_pending <= 1'b0;
        end 
        else begin
            // 如果同时收到了有效的地址和数据，准备发送响应
            if (write_addr_valid && write_data_valid && !write_resp_pending) begin
                s_axil_bvalid <= 1'b1;
                s_axil_bresp <= RESP_OKAY;  // 假设所有写操作都成功
                write_resp_pending <= 1'b1;
            end
            // 如果主设备已接收到响应，清除响应状态
            else if (s_axil_bvalid && s_axil_bready) begin
                s_axil_bvalid <= 1'b0;
                write_resp_pending <= 1'b0;
            end
        end
    end
    
    // 读地址通道处理
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s_axil_arready <= 1'b1;
            read_addr <= 12'd0;
            read_addr_valid <= 1'b0;
        end 
        else begin
            // 如果总线提供了有效的读地址，且从设备准备好接收
            if (s_axil_arvalid && s_axil_arready) begin
                read_addr <= s_axil_araddr;
                read_addr_valid <= 1'b1;
                s_axil_arready <= 1'b0;  // 表示已接收地址
            end
            // 如果读响应已完成，准备接收新的地址
            else if (s_axil_rvalid && s_axil_rready) begin
                read_addr_valid <= 1'b0;
                s_axil_arready <= 1'b1;
            end
        end
    end
    
    // 读数据通道处理
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s_axil_rvalid <= 1'b0;
            s_axil_rresp <= RESP_OKAY;
            s_axil_rdata <= 32'd0;
            read_resp_pending <= 1'b0;
        end 
        else begin
            // 如果收到了有效的读地址，准备发送数据
            if (read_addr_valid && !read_resp_pending) begin
                s_axil_rvalid <= 1'b1;
                s_axil_rresp <= RESP_OKAY;  // 假设所有读操作都成功
                
                // 根据地址选择相应的寄存器值
                case (read_addr)
                    ADDR_CTRL_REG: begin
                        // CTRL_REG 是可读寄存器
                        s_axil_rdata <= ctrl_reg_reg;
                    end
                    ADDR_STATUS_REG: begin
                        // STATUS_REG 是可读寄存器
                        s_axil_rdata <= status_reg_reg;
                    end
                    ADDR_INTR_ENABLE_REG: begin
                        // INTR_ENABLE_REG 是可读寄存器
                        s_axil_rdata <= intr_enable_reg_reg;
                    end
                    ADDR_INTR_STATUS_REG: begin
                        // INTR_STATUS_REG 是可读寄存器
                        s_axil_rdata <= intr_status_reg_reg;
                    end
                    ADDR_TX_DATA_REG: begin
                        // TX_DATA_REG 是只写寄存器，读取返回0
                        s_axil_rdata <= 32'd0;
                    end
                    ADDR_RX_DATA_REG: begin
                        // RX_DATA_REG 是可读寄存器
                        s_axil_rdata <= rx_data_reg_reg;
                    end
                    ADDR_CONFIG1_REG: begin
                        // CONFIG1_REG 是可读寄存器
                        s_axil_rdata <= config1_reg_reg;
                    end
                    ADDR_CONFIG2_REG: begin
                        // CONFIG2_REG 是可读寄存器
                        s_axil_rdata <= config2_reg_reg;
                    end
                    ADDR_TRIGGER_REG: begin
                        // TRIGGER_REG 是可读寄存器
                        s_axil_rdata <= trigger_reg_reg;
                    end
                    ADDR_ERROR_CODE_REG: begin
                        // ERROR_CODE_REG 是可读寄存器
                        s_axil_rdata <= error_code_reg_reg;
                    end
                    ADDR_VERSION_REG: begin
                        // VERSION_REG 是可读寄存器
                        s_axil_rdata <= version_reg_reg;
                    end
                    ADDR_ID_REG: begin
                        // ID_REG 是可读寄存器
                        s_axil_rdata <= id_reg_reg;
                    end
                    default: begin
                        // 未知地址，返回0
                        s_axil_rdata <= 32'd0;
                        s_axil_rresp <= RESP_DECERR;  // 解码错误
                    end
                endcase
                
                read_resp_pending <= 1'b1;
            end
            // 如果主设备已接收到数据，清除响应状态
            else if (s_axil_rvalid && s_axil_rready) begin
                s_axil_rvalid <= 1'b0;
                read_resp_pending <= 1'b0;
            end
        end
    end
    
    // 寄存器写逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // 复位所有寄存器
            ctrl_reg_reg <= 32'h00000000;
            status_reg_reg <= 32'h00000000;
            intr_enable_reg_reg <= 32'h00000000;
            intr_status_reg_reg <= 32'h00000000;
            tx_data_reg_reg <= 32'h00000000;
            rx_data_reg_reg <= 32'h00000000;
            config1_reg_reg <= 32'h00000000;
            config2_reg_reg <= 32'h00000000;
            trigger_reg_reg <= 32'h00000000;
            trigger_reg_pulse <= 32'd0;
            error_code_reg_reg <= 32'h00000000;
            version_reg_reg <= 32'h00020001;
            id_reg_reg <= 32'hABCD1234;
        end
        else begin
            // 默认清零脉冲信号
            trigger_reg_pulse <= 32'd0;
            
            // 处理写操作
            if (write_addr_valid && write_data_valid && !write_resp_pending) begin
                case (write_addr)
                    ADDR_CTRL_REG: begin
                        // CTRL_REG 是ReadWrite类型寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                ctrl_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                            end
                        end
                    end
                    ADDR_STATUS_REG: begin
                        // STATUS_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_INTR_ENABLE_REG: begin
                        // INTR_ENABLE_REG 是ReadWrite类型寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                intr_enable_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                            end
                        end
                    end
                    ADDR_INTR_STATUS_REG: begin
                        // INTR_STATUS_REG 是写1清零寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                intr_status_reg_reg[i*8 +: 8] <= intr_status_reg_reg[i*8 +: 8] & ~write_data[i*8 +: 8];
                            end
                        end
                    end
                    ADDR_TX_DATA_REG: begin
                        // TX_DATA_REG 是WriteOnly类型寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                tx_data_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                            end
                        end
                    end
                    ADDR_RX_DATA_REG: begin
                        // RX_DATA_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_CONFIG1_REG: begin
                        // CONFIG1_REG 是ReadWrite类型寄存器
                        if (!config1_reg_locked) begin
                            // 应用写屏蔽
                            for (int i = 0; i < 4; i = i + 1) begin
                                if (write_strb[i]) begin
                                    config1_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                                end
                            end
                        end
                    end
                    ADDR_CONFIG2_REG: begin
                        // CONFIG2_REG 是ReadWrite类型寄存器
                        if (!config2_reg_locked) begin
                            // 应用写屏蔽
                            for (int i = 0; i < 4; i = i + 1) begin
                                if (write_strb[i]) begin
                                    config2_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                                end
                            end
                        end
                    end
                    ADDR_TRIGGER_REG: begin
                        // TRIGGER_REG 是写1产生脉冲寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                trigger_reg_pulse[i*8 +: 8] <= write_data[i*8 +: 8];
                            end
                        end
                        trigger_reg_reg <= 32'd0;
                    end
                    ADDR_ERROR_CODE_REG: begin
                        // ERROR_CODE_REG 是ReadClean类型寄存器
                        // 应用写屏蔽
                        for (int i = 0; i < 4; i = i + 1) begin
                            if (write_strb[i]) begin
                                error_code_reg_reg[i*8 +: 8] <= write_data[i*8 +: 8];
                            end
                        end
                    end
                    ADDR_VERSION_REG: begin
                        // VERSION_REG 是只读寄存器，忽略写操作
                    end
                    ADDR_ID_REG: begin
                        // ID_REG 是只读寄存器，忽略写操作
                    end
                    default: begin
                        // 未知地址，不做任何操作
                    end
                endcase
            end
            
            // 读操作触发的特殊逻辑
            // 如果读取了ERROR_CODE_REG，则清零（ReadClean类型）
            if (read_addr_valid && read_addr == ADDR_ERROR_CODE_REG && s_axil_rvalid && s_axil_rready) begin
                error_code_reg_reg <= 32'd0;
            end
        end
    end

endmodule 