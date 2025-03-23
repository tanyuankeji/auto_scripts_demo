module test_multiline_comments (
    input wire clk,
    input wire rst_n,
    output wire [7:0] data_out
);

/* 
这是一个多行注释
wire test_wire1;
wire test_wire2;
*/

// 这是单行注释 wire test_wire3;

assign data = some_signal; // 这里的some_signal应该被识别为未定义信号

/* 嵌套的 /* 多行注释 */ 也应该被正确处理 */

assign another_data = another_signal;

endmodule 