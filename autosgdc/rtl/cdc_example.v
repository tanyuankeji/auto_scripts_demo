// CDC示例设计，包含多个时钟域和跨时钟域信号
// 该文件用于测试 AutoSGDC 工具

module cdc_example (
    // 时钟和复位
    input wire clk_fast,       // 快时钟，例如100MHz
    input wire clk_slow,       // 慢时钟，例如25MHz
    input wire rst_n,          // 低电平有效复位
    
    // 输入信号
    input wire [7:0] data_in_fast,    // 快时钟域输入数据
    input wire data_valid_fast,       // 快时钟域数据有效
    input wire [7:0] data_in_slow,    // 慢时钟域输入数据
    input wire data_valid_slow,       // 慢时钟域数据有效
    
    // 输出信号
    output reg [7:0] data_out_fast,   // 快时钟域输出数据
    output reg data_ready_fast,       // 快时钟域数据就绪
    output reg [7:0] data_out_slow,   // 慢时钟域输出数据
    output reg data_ready_slow        // 慢时钟域数据就绪
);

    // 内部信号 - 快时钟域
    reg [7:0] fast_data_reg;
    reg fast_valid_reg;
    reg fast_toggle;           // 切换信号，用于CDC
    reg [1:0] slow_toggle_sync; // 同步器，用于从慢时钟域同步到快时钟域
    reg slow2fast_valid;
    reg [7:0] slow2fast_data;
    
    // 内部信号 - 慢时钟域
    reg [7:0] slow_data_reg;
    reg slow_valid_reg;
    reg slow_toggle;           // 切换信号，用于CDC
    reg [1:0] fast_toggle_sync; // 同步器，用于从快时钟域同步到慢时钟域
    reg fast2slow_valid;
    reg [7:0] fast2slow_data;
    
    // CDC同步器 - 从快时钟域到慢时钟域的脉冲同步
    always @(posedge clk_slow or negedge rst_n) begin
        if (!rst_n) begin
            fast_toggle_sync <= 2'b00;
            fast2slow_valid <= 1'b0;
            fast2slow_data <= 8'h00;
        end else begin
            // 2级触发器同步器
            fast_toggle_sync <= {fast_toggle_sync[0], fast_toggle};
            
            // 边沿检测
            if (fast_toggle_sync[1] != fast_toggle_sync[0]) begin
                fast2slow_valid <= 1'b1;
                fast2slow_data <= fast_data_reg;  // 跨时钟域数据传输
            end else begin
                fast2slow_valid <= 1'b0;
            end
        end
    end
    
    // CDC同步器 - 从慢时钟域到快时钟域的脉冲同步
    always @(posedge clk_fast or negedge rst_n) begin
        if (!rst_n) begin
            slow_toggle_sync <= 2'b00;
            slow2fast_valid <= 1'b0;
            slow2fast_data <= 8'h00;
        end else begin
            // 2级触发器同步器
            slow_toggle_sync <= {slow_toggle_sync[0], slow_toggle};
            
            // 边沿检测
            if (slow_toggle_sync[1] != slow_toggle_sync[0]) begin
                slow2fast_valid <= 1'b1;
                slow2fast_data <= slow_data_reg;  // 跨时钟域数据传输
            end else begin
                slow2fast_valid <= 1'b0;
            end
        end
    end
    
    // 快时钟域逻辑
    always @(posedge clk_fast or negedge rst_n) begin
        if (!rst_n) begin
            fast_data_reg <= 8'h00;
            fast_valid_reg <= 1'b0;
            fast_toggle <= 1'b0;
            data_out_fast <= 8'h00;
            data_ready_fast <= 1'b0;
        end else begin
            // 默认值
            data_ready_fast <= 1'b0;
            
            // 处理来自快时钟域的输入
            if (data_valid_fast) begin
                fast_data_reg <= data_in_fast;
                fast_valid_reg <= 1'b1;
                fast_toggle <= ~fast_toggle;  // 切换信号，触发CDC
            end else begin
                fast_valid_reg <= 1'b0;
            end
            
            // 处理来自慢时钟域的同步数据
            if (slow2fast_valid) begin
                data_out_fast <= slow2fast_data;
                data_ready_fast <= 1'b1;
            end
        end
    end
    
    // 慢时钟域逻辑
    always @(posedge clk_slow or negedge rst_n) begin
        if (!rst_n) begin
            slow_data_reg <= 8'h00;
            slow_valid_reg <= 1'b0;
            slow_toggle <= 1'b0;
            data_out_slow <= 8'h00;
            data_ready_slow <= 1'b0;
        end else begin
            // 默认值
            data_ready_slow <= 1'b0;
            
            // 处理来自慢时钟域的输入
            if (data_valid_slow) begin
                slow_data_reg <= data_in_slow;
                slow_valid_reg <= 1'b1;
                slow_toggle <= ~slow_toggle;  // 切换信号，触发CDC
            end else begin
                slow_valid_reg <= 1'b0;
            end
            
            // 处理来自快时钟域的同步数据
            if (fast2slow_valid) begin
                data_out_slow <= fast2slow_data;
                data_ready_slow <= 1'b1;
            end
        end
    end

endmodule 