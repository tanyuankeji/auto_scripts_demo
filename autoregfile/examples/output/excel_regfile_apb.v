module excel_regfile (
    // ϵͳ�ź�
    input  wire                     clk,
    input  wire                     rst_n,
    
    // APB���߽ӿ�
    input  wire [7:0]   paddr,
    input  wire                     psel,
    input  wire                     penable,
    input  wire                     pwrite,
    input  wire [31:0]   pwdata,
    output reg  [31:0]   prdata,
    output wire                     pready,
    output wire                     pslverr
);

    // ��ַ��������
    localparam ADDR_CTRL_REG = 8'h0;
    localparam ADDR_STATUS_REG = 8'h0;
    localparam ADDR_INT_FLAGS = 8'h0;
    localparam ADDR_INT_ENABLE = 8'h0;

    // �Ĵ�������
    reg [31:0] ctrl_reg_reg;
    reg [31:0] status_reg_reg;
    reg [31:0] int_flags_reg;
    reg [31:0] int_enable_reg;


    // APB���߿����ź�
    wire apb_write = psel && penable && pwrite;
    wire apb_read  = psel && !pwrite;
    
    // APB���߾����ź� - ���������׼����
    assign pready  = 1'b1;
    
    // APB���ߴ����ź� - ����Ʋ���������
    assign pslverr = 1'b0;
    
    // �Ĵ���д�߼�
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // ��λ���мĴ���
            ctrl_reg_reg <= 32'h00000000;
            status_reg_reg <= 32'h00000000;
            int_flags_reg <= 32'h00000000;
            int_enable_reg <= 32'h00000000;
        end
        else begin
            // Ĭ�����������ź�
            
            // д�߼�
            if (apb_write) begin
                case (paddr)
                    ADDR_CTRL_REG: begin
                        // CTRL_REG ��ReadWrite���ͼĴ���
                        ctrl_reg_reg <= pwdata;
                    end
                    ADDR_STATUS_REG: begin
                        // STATUS_REG ��ֻ���Ĵ���������д����
                    end
                    ADDR_INT_FLAGS: begin
                        // INT_FLAGS ��ReadWrite���ͼĴ���
                        int_flags_reg <= pwdata;
                    end
                    ADDR_INT_ENABLE: begin
                        // INT_ENABLE ��ReadWrite���ͼĴ���
                        int_enable_reg <= pwdata;
                    end
                    default: begin
                        // δ֪��ַ�������κβ���
                    end
                endcase
            end
            
            // �����������������߼�
        end
    end
    
    // �Ĵ������߼�
    always @(*) begin
        prdata = 32'd0; // Ĭ��ֵ
        
        if (apb_read) begin
            case (paddr)
                ADDR_CTRL_REG: begin
                    // CTRL_REG �ǿɶ��Ĵ���
                    prdata = ctrl_reg_reg;
                end
                ADDR_STATUS_REG: begin
                    // STATUS_REG �ǿɶ��Ĵ���
                    prdata = status_reg_reg;
                end
                ADDR_INT_FLAGS: begin
                    // INT_FLAGS �ǿɶ��Ĵ���
                    prdata = int_flags_reg;
                end
                ADDR_INT_ENABLE: begin
                    // INT_ENABLE �ǿɶ��Ĵ���
                    prdata = int_enable_reg;
                end
                default: begin
                    // δ֪��ַ������0
                    prdata = 32'd0;
                end
            endcase
        end
    end

endmodule 