module spi_clk_sel(
    // clk 
    input       spi_scl     ,
    // func 
    input       spi_cs      ,
    input       cpol        ,
    input       cpha        ,
    // dft  
    input       dft_test_mode   ,
    input       dft_scan_clk    ,
    // 
    output wire spi_clk     ,
    output wire spi_clk_n   
    
);
    
    
    // wire spi_clk_buf; 
    // wire sclk_in; 
    // wire spi_clk_n_0; 

    assign spi_clk_buf  = (cpol ^ cpha) ? ~spi_scl : spi_scl;

    assign sclk_in = cpha ? ( spi_cs | spi_clk_buf ) :
                            (~spi_cs | spi_clk_buf ) ;

    /* dft ---------------------------------------------------------------------- */
    CLK_MUX dftmux_spi_clk ( .O(spi_clk), 
                            .I0(sclk_in), 
                            .I1(dft_scan_clk), 
                            .S(dft_test_mode));
    CLKINV libcell_spi_clk_n_0 (
                            .O(spi_clk_n_0), 
                            .I(spi_clk)); 
    CLK_MUX dftmux_spi_clk_n (
                            .O(spi_clk_n), 
                            .I0(spi_clk_n_0), 
                            .I1(dft_scan_clk), 
                            .S(dft_test_mode));


    
endmodule