module xx_regfile(
// clk & rstn
input   clk ,
input   rstn,

// register write interface
input [ADDR-1:0]  reg_wr_addr_i,
input [DATA-1:0]  reg_wr_data_i,
input   wr_data_vld_i,
input [DATA/8-1:0]  reg_wr_byte_en_i,
input   reg_wr_req_i,
output wire  invalid_wr_addr_o,
output wire  invalid_wr_access_o,
output wire  undefined_wr_addr_o,

// register read interface
input [ADDR-1:0]  reg_rd_addr_i,
input   reg_rd_req_i,

output wire  [DATA-1:0]  reg_rd_data_o,
output wire  valid_rd_addr_o,
output wire  invalid_rd_addr_o,
output wire  invalid_rd_access_o,
output wire  undefined_rd_addr_o,



);
    
endmodule //xx_regfile




