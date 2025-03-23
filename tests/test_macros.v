module test_macros (
    input wire clk,
    input wire rst_n,
    output wire [7:0] data_out
);

`define TEST_MACRO 8
`include "some_file.vh"

`ifdef SIMULATION
    wire sim_wire;
`else
    assign debug_signal = test_signal;
`endif

assign data = `TEST_MACRO'd0; // 这里的test_signal应该被识别为未定义信号

endmodule 