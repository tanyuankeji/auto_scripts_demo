
`timescale	1ns/1ns

module dff_pn(clk,rst_n,din, dout);

	parameter DATA_WIDTH = 1      ;
	parameter DATA_VALUE = 0      ;
    
	input  clk        ;
   	input  rst_n       ;
	
	input	[DATA_WIDTH - 1 : 0]	din;
	
	output	[DATA_WIDTH - 1 : 0]	dout;
	reg		[DATA_WIDTH - 1 : 0]	dout;
   	
always @ (posedge clk or negedge rst_n)
  	begin
    if(!rst_n)
       begin
          dout <= #1 DATA_VALUE; //从0计数
       end
    else begin
          dout <= #1 din;
    	end
	end

endmodule
	



