module test_complex_signals (
    input wire clk,
    input wire rst_n,
    output wire [7:0] data_out
);

// 测试各种信号定义
wire simple_wire;
wire [7:0] width_wire;
wire [`PARAM-1:0] param_wire;
wire [DATA_WIDTH-1:0] complex_wire1, complex_wire2, complex_wire3; // 多个信号定义
reg [3:0] simple_reg;
reg [ADDR_WIDTH:0] addr_reg;

// 测试多行定义
wire 
    multi_line_wire1,
    multi_line_wire2;
    
// 测试未定义信号
assign data = undefined_wire;
always @(posedge clk) begin
    if (condition)
        another_undefined = 1'b1;
end

endmodule 