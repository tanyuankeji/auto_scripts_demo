//------------------------------------------------------------------------------
//
//            CADENCE                    Copyright (c) 2002-2015
//                                       Cadence Design Systems, Inc.
//                                       All rights reserved.
//
//  This work may not be copied, modified, re-published, uploaded, executed, or
//  distributed in any way, in any medium, whether in whole or in part, without
//  prior written permission from Cadence Design Systems, Inc.
//------------------------------------------------------------------------------
//
//    Primary Unit Name :      cdns_qspi_ahb_ctrl_registers
//
//          Description :      Register Block for the QSPI Flash Controller
//
//      Original Author :      Ewan McCulloch
//
//------------------------------------------------------------------------------

`include "cdns_qspi_flash_ctrl_defs.v"
`include "cdns_qspi_spi_ctrl_core_defs.v"

module cdns_qspi_ahb_ctrl_registers (

          // Clocks / resets
          pclk,
          n_preset,
          hclk,
          n_hreset,
          `ifdef cdns_qspi_include_ref_clk
          ref_clk,
          n_ref_rst,
          `endif

          // APB Interface
          psel,
          penable,
          pwrite,
          paddr,
          pwdata,
          prdata,
          pslverr,

         // SPI status
          idle_spi,

          //SRAM fill level from SRAM controller (HCLK timed)
          indrd_sram_fill_level,
          indwr_sram_fill_level,

          // FLASH side of indrd xfer has completed
          indrd_xfer_flash_done,

          // AHB side of indwr xfer has completed
          indwr_xfer_ahb_done,

          // Interrupt Sources (NOT APB TIMED, mostly toggles)
          tx_full_hclk,
          tx_notfull_hclk,
          rx_full_refclk,
          rx_notempty_refclk,
          rx_oflow_tog,
          indrd_wmark_trig_tog,
          indwr_wmark_trig_tog,
          ahb_access_err_tog,
          ahb_wr_prot_err_tog,
          ind_oflow_tog,
          indrd_xfer_done_tog,
          indwr_xfer_done_tog,
          tx_uflow_tog,
          indwr_flush_tog,
          indrd_flush_tog,
          expiration_tog,

          // Auto-polling logic
          polling_status,
          max_num_of_polls,
          stig_during_poll_done,

          // Capture pulses to indicate when it is safe for the source to be
          // generated again
          ahb_access_err_capt,
          ahb_wr_prot_err_capt,
          indrd_xfer_done_capt,
          indrd_wmark_trig_capt,
          indwr_xfer_done_capt,
          indwr_wmark_trig_capt,
          indwr_flush_capt,
          indrd_flush_capt,

          //Interrupt output
          interrupt,

          // Dynamic control outputs
          qspi_enable_refclk,
          qspi_enable_hclk,
          ahb_remap_en_hclk,
          ahb_wr_protection_en_hclk,
          dma_pif_en_hclk,
          legacy_mode_en_hclk,
          direct_access_en_hclk,
          start_indrd_hclk,
          cancel_indrd_hclk,
          start_indwr_hclk ,
          cancel_indwr_hclk,
          lb_clk_enable_refclk,
          enter_xip_now_refclk,
          enter_xip_next_refclk,
          ahb_dec_en_hclk,
          ahb_dec_en_refclk,
          dtr_prot_refclk,

          // Static configuration outputs
          // To the Legacy SPI Core ...
          cpha,
          cpol,
          baud_rate,
          pdec,
          device_ss,
          d_init,
          d_after,
          d_btwn,
          d_nss,          
          status_dummy,
          tx_threshold,
          rx_threshold,
          rep_gap_delay_reg,
          poll_count,                                        
          poll_exp_en,   
          poll_disable,  
          poll_polarity, 
          poll_bit_index,
          poll_opcode,   
          write_protect,
          capture_edge_arbiter,
          rd_data_capture_dly,
          instruction_type,
          address_xfer_type_wr,
          address_xfer_type_rd,
          data_xfer_type_wr,
          data_xfer_type_rd,
          dtr_mode,
          wel_precomm_dis,
          dtr_shift_mo,

          // To the AHB Slave Controller
          ahb_remap_addr,
          lower_protection_addr,
          upper_protection_addr,
          ahb_wr_protection_inv,
          num_bytes_in_block,
          cs_size_decoder,

          // To the ind Access Controller
          indrd_wmark,
          indrd_start_add,
          indrd_num_bytes,
          indwr_wmark,
          indwr_start_add,
          indwr_num_bytes,
          ind_ahb_trig_add,
          ind_ahb_trig_add_range,
          sram_partition,

          // To the DMA Peripheral Interface
          bytes_in_burst_type_map,
          bytes_in_single_type_map,

          bytes_in_burst_type,
          bytes_in_single_type,

          // To the Flash Command Generator
          read_opcode,
          write_opcode,
          num_dummy_clks_read,
          num_dummy_clks_write,
          num_addr_bytes,
          mode_bits_en,
          mode_bits,
          num_bytes_in_page,


          // STIG access to the Command generator
          stig_valid,
          stig_during_poll,
          stig_ready,
          stig_opcode,
          stig_addr_en,
          stig_num_addr_bytes,
          stig_add,
          stig_mode_en,
          stig_num_wdata_bytes,
          stig_wdata,
          stig_num_rdata_bytes,
          stig_rdata,
          stig_num_dummy_clks,
          
          // STIG Memory Bank i/f
          stig_mem_bank_en,
          stig_mem_bank_addr,
          stig_mem_bank_rd_data,
          mem_bank_valid,
          stig_mem_bank_ready,
          stig_mem_bank_stages  

     );


// Define local parameters
parameter P_SIZE          = `CDNS_QSPI_SPI_P_SIZE;    // number of periph select lines
parameter [7:0]  MODULE_ID_FIX_PATCH = 8'h01; //fix/path of the revision
parameter [15:0] MODULE_ID           = 16'h0001;  //revision ID
parameter [1:0] CONFIG_ID            = 2'h3;  //Quad
   
// Clocks, Resets
input                   pclk;         // system clock
input                   n_preset;     // system reset
input                   hclk;         // system clock
input                   n_hreset;     // system reset
`ifdef cdns_qspi_include_ref_clk
input                   ref_clk;      // Reference clock (must be >4x spi_clk)
input                   n_ref_rst;    // Reference reset
`endif

// APB interface
input                   psel;         // APB peripheral select
input                   penable;      // APB enable, 2nd transfer cycle
input                   pwrite;       // APB write/read select
input   [7:0]           paddr;        // APB address bus
input   [31:0]          pwdata;       // APB write data bus
output  [31:0]          prdata;       // APB read data
output                  pslverr;      // APB response


// SPI status
input                   idle_spi;     // SPI in the idle state

// SRAM fill level from the SRAM controller
input  [`cdns_qspi_sram_depth-1:0] indrd_sram_fill_level; // SRAM RD fill level
input  [`cdns_qspi_sram_depth-1:0] indwr_sram_fill_level; // SRAM WR fill level

// Indirect Read FLASH side has completed its indirect operation
input                   indrd_xfer_flash_done;

// Indirect Write AHB side has completed its indirect operation
input                   indwr_xfer_ahb_done;

// Auto-polling logic
input  [8:0]            polling_status;

// Interrupt sources
input                   tx_full_hclk;           // HCLK timed source
input                   tx_notfull_hclk;        // HCLK timed source
input                   tx_uflow_tog;           // Toggle source
input                   rx_full_refclk;         // Refclk timed source
input                   rx_notempty_refclk;     // Refclk timed source
input                   rx_oflow_tog;           // Toggle source
input                   indrd_wmark_trig_tog;   // Toggle source
input                   indwr_wmark_trig_tog;   // Toggle source
input                   ahb_access_err_tog;     // Toggle source
input                   ahb_wr_prot_err_tog;    // Toggle source
input                   ind_oflow_tog;          // Toggle source
input                   indrd_xfer_done_tog;    // Toggle source
input                   indwr_xfer_done_tog;    // Toggle source
input                   indrd_flush_tog;        // Toggle source
input                   indwr_flush_tog;        // Toggle source
input                   expiration_tog;         // Toggle source

// Capture pulses to indicate when it is safe for the source to be
// generated again
output                  ahb_access_err_capt;
output                  ahb_wr_prot_err_capt;
output                  indrd_xfer_done_capt;
output                  indrd_wmark_trig_capt;
output                  indwr_xfer_done_capt;
output                  indwr_wmark_trig_capt;
output                  indrd_flush_capt;
output                  indwr_flush_capt;

//Interupt Pulse output
output                  interrupt;    // Maskable interrupt to CPU

// Dynamic Control outputs
output          qspi_enable_refclk;       // Used by legacy core only
output          qspi_enable_hclk;         // Acts as a soft reset to HCLK
output          ahb_remap_en_hclk;        // Enable AHB Remapping logic
output          ahb_wr_protection_en_hclk;// Enable AHB Write protection
output          dma_pif_en_hclk;          // Enable DMA Peripheral Interface
output          legacy_mode_en_hclk;      // Enable legacy mode
output          direct_access_en_hclk;    // Enable direct access controller
output          start_indrd_hclk;         // Trigger ind Read Access
output          cancel_indrd_hclk;        // Cancel ind Read Access
output          start_indwr_hclk ;        // Trigger ind Read Access
output          cancel_indwr_hclk;        // Cancel ind Read Access
output          lb_clk_enable_refclk;     // Don't bypass the loopback clk logic
output          enter_xip_now_refclk;     // Device in XIP mode when this is set
output          enter_xip_next_refclk;    // Device in XIP mode after next read
output          ahb_dec_en_hclk;          // Decode CS based on current ahb address
output          ahb_dec_en_refclk;        // Decode CS based on current ahb address
output          dtr_prot_refclk;      // All commands work in DDR Mode

input           stig_during_poll_done;  // STIG command ready to acknowledge
output  [31:0]  max_num_of_polls;       // maximum number of polls before expiration

// Configuration Outputs
// These signals are assumed static throughout the core and should be
// setup before enabling the spi.
output               cpha;                // Clock phase
output               cpol;                // Clock polarity
output  [3:0]        baud_rate;           // baud rate diviser (div2 to div 16)
output               pdec;                // peripheral decode
output  [P_SIZE-1:0] device_ss;           // peripheral selects
output  [7:0]        d_init;              // delay from slave select to first
                                          // bit period
output  [7:0]        d_after;             // delay between each word xfer
output  [7:0]        d_btwn;              // delay  between chip selects
output  [7:0]        d_nss;               // delay for chip selects
output  [3:0]        status_dummy;        // number of dummy cycles to be inserted into auto-polling
output [`CDNS_QSPI_TXFF_A-1:0] tx_threshold;        // TX fifo threshold value
output [`CDNS_QSPI_RXFF_A-1:0] rx_threshold;        // RX fifo threshold value
output  [7:0]        rep_gap_delay_reg;   // gap size between every poll
output  [7:0]        poll_count;          // additional number of polls after getting expected value                                        
output               poll_exp_en;         // Auto-Polling expiration enable bit   
output               poll_disable;        // Auto-Polling disable bit 
output               poll_polarity;       // Polarity of bit being auto-polled
output  [2:0]        poll_bit_index;      // Index of bit being auto-polled
output  [7:0]        poll_opcode;         // Auto-Polling opcode
output               write_protect;       // Value to drive on WP pin
output               capture_edge_arbiter;// To select edge of capture data logic
output  [3:0]        rd_data_capture_dly; // Number of cycle delays in the
                                          // read data capture logic
output  [3:0]        dtr_shift_mo;        // Delay value of master output data

output          dtr_mode;                 // Command setting in Read Configuration Reg works in DDR mode
output          wel_precomm_dis;          // Disable WEL pre-command before write
output  [31:0]  ahb_remap_addr;           // Amount to remap incoming addresses by
output  [31:0]  lower_protection_addr;    // Lower AHB Write Protection Address
output  [31:0]  upper_protection_addr;    // Lower AHB Write Protection Address
output          ahb_wr_protection_inv;    // Protection region is inverted

output  [31:0]  indrd_wmark;      // ind Access Watermark
output  [31:0]  indrd_start_add;  // ind Access Start Address
output  [31:0]  indrd_num_bytes;  // Num bytes in ind Access
output  [31:0]  indwr_wmark;     // ind Access Watermark
output  [31:0]  indwr_start_add; // ind Access Start Address
output  [31:0]  indwr_num_bytes; // Num bytes in ind Access
output  [31:0]  ind_ahb_trig_add;    // Address the AHB controller uses to pop the SRAM
output  [3:0]   ind_ahb_trig_add_range;    // Address Range the AHB controller uses to pop the SRAM

output  [15:0]   bytes_in_burst_type_map;      // Number of bytes in a DMA burst acc, mapped
output  [15:0]   bytes_in_single_type_map;     // Number of bytes in a DMA single acc, mapped
output  [3:0]    bytes_in_burst_type;      // Number of bytes in a DMA burst acc, mapped
output  [3:0]    bytes_in_single_type;     // Number of bytes in a DMA single acc, mapped

output  [7:0]   read_opcode;              // Read Opcode used by DAC/IDAC
output  [7:0]   write_opcode;             // Write Opcode used by DAC/IDAC
output  [1:0]   instruction_type;         // 0 for extended SPI
output  [1:0]   address_xfer_type_wr;     // 0 for 1pin,1 for 2pins,2 for 4pins
output  [1:0]   address_xfer_type_rd;     // 0 for 1pin,1 for 2pins,2 for 4pins
output  [1:0]   data_xfer_type_wr;        // 0 for SIO, 1 for DIO, 2 for QIO
output  [1:0]   data_xfer_type_rd;        // 0 for SIO, 1 for DIO, 2 for QIO
output  [3:0]   num_addr_bytes;           // Num address bytes to send
output  [4:0]   num_dummy_clks_read;      // Num dummy clocks after address
output  [4:0]   num_dummy_clks_write;     // Num dummy clocks after address
output          mode_bits_en;             // Enable the use of mode bits
output  [7:0]   mode_bits;                // Mode bits to use
output  [7:0]   cs_size_decoder;          // Concise form of size of connected devices
output  [4:0]   num_bytes_in_block;       // configured number bytes in Flash device block
output  [11:0]  num_bytes_in_page;        // configured number bytes in Flash device page

// STIG
output        stig_valid;             // STIG request is valid
input         stig_ready;             // STIG controller is ready
output [7:0]  stig_opcode;            // STIG opcode
output        stig_addr_en;           // STIG address phase enable bit
output [1:0]  stig_num_addr_bytes;    // Number of address bytes to transmit by STIG
output [31:0] stig_add;               // Actual STIG address  
output        stig_mode_en;           // STIG Mode enable bit
output [3:0]  stig_num_wdata_bytes;   // Number of bytes to write by STIG
output [63:0] stig_wdata;             // Data to write by STIG
output [3:0]  stig_num_rdata_bytes;   // Number of bytes to read by STIG 
input  [63:0] stig_rdata;             // Read data by STIG (up to 8 bytes) 
output [4:0]  stig_num_dummy_clks;    // Number of dummy cycles to transmit by STIG
output        stig_during_poll;       // STIG request during auto-polling

// STIG Memory Bank
output        stig_mem_bank_en;       // Enable STIG Memory Bank
output  [`cdns_qspi_stig_mem_bank_addr_width-1:0]    stig_mem_bank_addr; // Address of requested data (Byte index) 
input [7:0]   stig_mem_bank_rd_data;  // Requested Memory Bank STIG Data
output        mem_bank_valid;         // Indicates valid Memory Bank Data request
input         stig_mem_bank_ready;    // Data is stable (returned by Memory Bank Block)
output  [`cdns_qspi_stig_mem_bank_addr_width-3:0] stig_mem_bank_stages;   // Calculated number of Memory Bank Stages

output  [`cdns_qspi_sram_depth-1:0] sram_partition; // configured SRAM partition


wire            read_enable;                  // APB read enable
wire            write_enable;                 // APB write enable

reg   [31:0]    prdata;                       // APB Read data
reg             pslverr;                      // APB response

// Configuration fields
reg   [20:0]    config_reg;
reg   [20:0]    dev_rd_instr_cfg_reg;
reg   [17:0]    dev_wr_instr_cfg_reg;
reg   [28:0]    dev_size_cfg_reg;
reg   [31:0]    dev_delay_reg;
reg   [24:0]    cmd_ctrl_reg;
reg   [31:0]    cmd_add_reg;
reg   [63:0]    cmd_rdata_reg;
reg   [63:0]    cmd_wdata_reg;
reg   [3:0]     dtr_shift_mo;
reg   [5:0]     rdata_capture_reg;
reg   [31:0]    indrd_xfer_wmark_reg;
reg   [31:0]    indrd_xfer_start_add_reg;
reg   [31:0]    indrd_xfer_num_bytes_reg;
reg   [31:0]    indwr_xfer_wmark_reg;
reg   [31:0]    indwr_xfer_start_add_reg;
reg   [31:0]    indwr_xfer_num_bytes_reg;
reg   [31:0]    ind_ahb_trig_add_reg;
reg   [3:0]     ind_ahb_trig_add_range_reg;
reg   [7:0]     dma_periph_config_reg;
reg   [31:0]    remap_add_reg;
reg   [14:0]    int_status_reg;
reg   [14:0]    int_mask_reg;
reg   [7:0]     mode_bits;
reg   [31:0]    write_protect_lower_reg;
reg   [31:0]    write_protect_upper_reg;
reg   [1:0]     write_protect_ctrl_reg;
reg   [`CDNS_QSPI_TXFF_A-1:0] tx_threshold;        // TX fifo threshold value
reg   [`CDNS_QSPI_RXFF_A-1:0] rx_threshold;        // RX fifo threshold value
reg   [31:0]    max_num_of_polls;
reg   [7:0]     rep_gap_delay_reg;
reg   [7:0]     poll_count;          // additional number of polls after getting expected value                                        
reg             poll_exp_en;         // Auto-Polling expiration enable bit   
reg             poll_disable;        // Auto-Polling disable bit 
reg             poll_polarity;       // Polarity of bit being auto-polled
reg   [2:0]     poll_bit_index;      // Index of bit being auto-polled
reg   [7:0]     poll_opcode;         // Auto-Polling opcode
reg   [3:0]     status_dummy;
reg             interrupt;

// Synchronization logic
wire            tx_uflow_sync;
reg             tx_uflow_d1;
wire            indrd_xfer_done_sync;
reg             indrd_xfer_done_d1;
wire            indwr_xfer_done_sync;
reg             indwr_xfer_done_d1;
wire            indrd_flush_sync;
reg             indrd_flush_d1;
wire            indwr_flush_sync;
reg             indwr_flush_d1;
wire            ind_oflow_sync;
reg             ind_oflow_d1;
wire            ahb_wr_prot_err_sync;
reg             ahb_wr_prot_err_d1;
wire            ahb_access_err_sync;
reg             ahb_access_err_d1;
wire            ahb_dec_en_refclk_sync;
wire            ahb_dec_en_sync;
wire            ahb_remap_en_sync;
wire            ahb_wr_protection_en_sync;
wire            indrd_wmark_trig_sync;
reg             indrd_wmark_trig_d1;
wire            indwr_wmark_trig_sync;
reg             indwr_wmark_trig_d1;
wire            rx_overflow_sync;
reg             rx_overflow_d1;
wire            rx_notempty_sync;
reg             rx_notempty_d1;
wire            rx_full_sync;
reg             rx_full_d1;
wire            tx_notempty_sync;
reg             tx_notempty_d1;
wire            tx_full_sync;
reg             tx_full_d1;
wire            idle_spi_sync;
reg             ahb_access_err_capt_tog;
wire            ahb_access_err_capt_sync;
reg             ahb_access_err_capt_d1;
reg             ahb_wr_prot_err_capt_tog;
wire            ahb_wr_prot_err_capt_sync;
reg             ahb_wr_prot_err_capt_d1;
reg             indrd_xfer_done_capt_tog;
wire            indrd_xfer_done_capt_sync;
reg             indrd_xfer_done_capt_d1;
reg             indrd_wmark_trig_capt_tog;
wire            indrd_wmark_trig_capt_sync;
reg             indrd_wmark_trig_capt_d1;
reg             indwr_xfer_done_capt_tog;
wire            indwr_xfer_done_capt_sync;
reg             indwr_xfer_done_capt_d1;
reg             indrd_flush_capt_tog;
wire            indrd_flush_capt_sync;
reg             indrd_flush_capt_d1;
reg             indwr_flush_capt_tog;
wire            indwr_flush_capt_sync;
reg             indwr_flush_capt_d1;
reg             indwr_wmark_trig_capt_tog;
wire            indwr_wmark_trig_capt_sync;
reg             indwr_wmark_trig_capt_d1;
wire            start_indrd_sync;
reg             start_indrd_d1;
wire            cancel_indrd_sync;
reg             cancel_indrd_d1;
wire            start_indwr_sync;
reg             start_indwr_d1;
wire            cancel_indwr_sync;
reg             cancel_indwr_d1;
reg             sample_sram_fill;
reg  [(`cdns_qspi_sram_depth*2)-1:0]   sram_fill_hold;
reg             initial_capt_hclk;
wire            sram_fill_captured_sync;
reg             sram_fill_captured_d1;
wire            sample_sram_sync;
reg             sample_sram_d1;
wire            expiration_sync;
reg             expiration_d1;
reg             sram_fill_captured_pclk;
reg  [(`cdns_qspi_sram_depth*2)-1:0]  sram_fill_level_pclk;
reg             ind_trigger_oflow;
wire            direct_access_en_sync;
wire            dma_pif_en_sync;
wire            enter_xip_next_refclk_sync;
wire            enter_xip_now_refclk_sync;
wire            initial_capt_hclk_sync;
wire            lb_clk_enable_sync;
wire            legacy_mode_en_sync;
wire            qspi_enable_hc_sync;
wire            qspi_enable_rc_sync;
wire            write_protect_sync;

// Interrupts
wire            expiration;
wire            tx_underflow;
wire            indrd_xfer_done;
wire            indwr_xfer_done;
wire            ind_oflow;
wire            ahb_wr_prot_err;
wire            ahb_access_err;
wire            rx_overflow;
wire            rx_notempty;
wire            rx_full;
wire            tx_notempty;
wire            tx_full;

wire  [14:0]    int_status_src_pulse; // All interrupt sources, pulsed, APB timed
wire  [14:0]    int_status_lat;       // Level sensitive int status bus
wire            ahb_access_err_capt;
wire            ahb_wr_prot_err_capt;
wire            indrd_flush;
wire            indwr_flush;
wire            indrd_wmark_trig; // Indirect read watermark trigger
wire            indwr_wmark_trig; // Indirect write watermark trigger

wire [8:0]      polling_status;

// part of the ind Read Transfer Control register
reg   [1:0]     num_indrd_completed;
reg             indrd_comp_status;
reg             indrd_2_queued;
reg             sram_full_ind_err;
reg             indrd_in_progress;
reg             cancel_indrd_pclk;
reg             start_indrd_pclk;
reg             start_indrd_hclk;
reg             start_indrd_hold;
reg             indrd_xfer_in_prog_hclk;
reg   [`cdns_qspi_sram_depth-1:0] sram_partition;

// part of the ind Write Transfer Control register
reg   [1:0]     num_indwr_completed;
reg             indwr_comp_status;
reg             indwr_2_queued;
reg             indwr_in_progress;
reg             cancel_indwr_pclk;
reg             start_indwr_pclk;
reg             start_indwr_reg ;
wire            start_indwr_hclk ;
reg             start_indwr_hold;
reg             indwr_xfer_in_prog_hclk;

// STIG logic
reg             stig_valid;
reg             stig_during_poll_valid;
wire            stig_during_poll_sync;
reg             trigger_stig_tog;
wire            trigger_stig_tog_sync;
reg             trigger_stig_tog_d1;  // into AHB
wire            stig_in_progress_sync;
reg             stig_in_progress_d1;  // Back into APB
reg             stig_in_progress;
reg             stig_in_progress_waiting;
reg             stig_in_progress_pck_d1;
reg             stig_completion;
reg             stig_done_tog_hclk;
wire            stig_during_poll_done_sync;
reg             stig_during_poll_done_d1;
reg             stig_during_poll_ack;

// STIG Memory Bank logic
reg             stig_mem_bank_en;
reg             mem_bank_valid;
reg             trigger_mem_bank_tog;
wire            trigger_mem_bank_tog_sync;
reg             trigger_mem_bank_tog_d1;  // into AHB
wire            mem_bank_in_progress_sync;
reg             mem_bank_in_progress_d1;  // Back into APB
reg             mem_bank_in_progress;
reg             mem_bank_done_tog_hclk;
reg [`cdns_qspi_stig_mem_bank_addr_width-1:0]    stig_mem_bank_addr;
reg [`cdns_qspi_stig_mem_bank_data_pck-1:0] stig_mem_bank_no_of_bytes;
reg [7:0]       mem_bank_rdata;
wire  [`cdns_qspi_stig_mem_bank_addr_width-3:0] stig_mem_bank_stages_precalc;      



// DTR logic
wire            dtr_prot_sync;


// General APB read/write signals
  assign read_enable    = (psel & ~penable & ~pwrite);
  assign write_enable   = (psel & penable &  pwrite);


//   Read Mux Control Block
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
      prdata <= 32'h00000000;

    else if (read_enable)
    begin
      case (paddr)
       `CDNS_QSPI_CONFIG:            prdata <= {idle_spi_sync,6'h00,config_reg[20:3],4'h0,config_reg[2:0]};
       `CDNS_QSPI_DEV_RDINSTR_CONFIG:prdata <= { 3'b000,
                                            dev_rd_instr_cfg_reg[20:16],
                                            3'h0,
                                            dev_rd_instr_cfg_reg[15],
                                            2'b00,
                                            dev_rd_instr_cfg_reg[14:13],
                                            2'b00,
                                            dev_rd_instr_cfg_reg[12:11],
                                            1'b0,
                                            dev_rd_instr_cfg_reg[10],
                                            dev_rd_instr_cfg_reg[9:0]};
       `CDNS_QSPI_DEV_WRINSTR_CONFIG:prdata <= {3'b000,
                                           dev_wr_instr_cfg_reg[17:13],
                                           6'h00,
                                           dev_wr_instr_cfg_reg[12:11],
                                           2'b00,
                                           dev_wr_instr_cfg_reg[10:9],
                                           3'b000,
                                           dev_wr_instr_cfg_reg[8],
                                           dev_wr_instr_cfg_reg[7:0]};
       `CDNS_QSPI_DEV_SIZE_CONFIG:   prdata <= {3'b000,dev_size_cfg_reg};
       `CDNS_QSPI_DEV_DELAY:         prdata <= {dev_delay_reg[31:0]};
       `CDNS_QSPI_FLASH_CMD_MEM:     prdata <= {{12-`cdns_qspi_stig_mem_bank_addr_width{1'b0}},stig_mem_bank_addr,
                                               {4-`cdns_qspi_stig_mem_bank_data_pck{1'b0}},stig_mem_bank_no_of_bytes,
                                               mem_bank_rdata,6'h00,mem_bank_in_progress,1'b0};       
       `CDNS_QSPI_FLASH_CMD_CTRL:    prdata <= {cmd_ctrl_reg[24:0],4'h0,stig_mem_bank_en,stig_in_progress | stig_in_progress_waiting,1'b0};
       `CDNS_QSPI_FLASH_CMD_ADD:     prdata <= {cmd_add_reg};
       `CDNS_QSPI_FLASH_CMD_RDATA_L: prdata <= {cmd_rdata_reg[31:0]};
       `CDNS_QSPI_FLASH_CMD_RDATA_U: prdata <= {cmd_rdata_reg[63:32]};
       `CDNS_QSPI_FLASH_CMD_WDATA_L: prdata <= {cmd_wdata_reg[31:0]};
       `CDNS_QSPI_FLASH_CMD_WDATA_U: prdata <= {cmd_wdata_reg[63:32]};
       `CDNS_QSPI_READ_DATA_CAPTURE: prdata <= {12'h000,dtr_shift_mo[3:0],10'h000,rdata_capture_reg[5:0]};
       `CDNS_QSPI_SRAM_FILL_LEVEL:   prdata <= {{16-`cdns_qspi_sram_depth{1'b0}},
                                            sram_fill_level_pclk[`cdns_qspi_sram_depth*2-1:`cdns_qspi_sram_depth],
                                           {16-`cdns_qspi_sram_depth{1'b0}},
                                            sram_fill_level_pclk[`cdns_qspi_sram_depth-1:0]};
       `CDNS_QSPI_SRAM_PARTITION:       prdata <= {{32-`cdns_qspi_sram_depth{1'b0}},sram_partition};
       `CDNS_QSPI_IND_RD_XFER_CTRL:     prdata <= {24'h000000,num_indrd_completed, indrd_comp_status, indrd_2_queued, sram_full_ind_err, indrd_in_progress, 2'b00};
       `CDNS_QSPI_IND_RD_XFER_WMARK:    prdata <= {indrd_xfer_wmark_reg[31:0]};
       `CDNS_QSPI_IND_RD_XFER_START_ADD:prdata <= {indrd_xfer_start_add_reg[31:0]};
       `CDNS_QSPI_IND_RD_XFER_NUM_BYTES:prdata <= {indrd_xfer_num_bytes_reg[31:0]};
       `CDNS_QSPI_IND_WR_XFER_CTRL:     prdata <= {24'h000000,num_indwr_completed, indwr_comp_status, indwr_2_queued, 1'b0, indwr_in_progress, 2'b00};
       `CDNS_QSPI_IND_WR_XFER_WMARK:    prdata <= {indwr_xfer_wmark_reg[31:0]};
       `CDNS_QSPI_IND_WR_XFER_START_ADD:prdata <= {indwr_xfer_start_add_reg[31:0]};
       `CDNS_QSPI_IND_WR_XFER_NUM_BYTES:prdata <= {indwr_xfer_num_bytes_reg[31:0]};
       `CDNS_QSPI_IND_AHB_TRIGGER:      prdata <= {ind_ahb_trig_add_reg[31:0]};
       `CDNS_QSPI_IND_AHB_TRIGGER_RANGE:prdata <= {28'h0000000,ind_ahb_trig_add_range_reg[3:0]};
       `CDNS_QSPI_PERIPH_CFG:           prdata <= {20'h00000,
                                            dma_periph_config_reg[7:4],
                                            4'h0,
                                            dma_periph_config_reg[3:0]};
       `CDNS_QSPI_REMAP_ADD:         prdata <= {remap_add_reg};
       `CDNS_QSPI_INT_STATUS:        prdata <= {17'h00000,int_status_lat[14:0]};
       `CDNS_QSPI_MODE_BIT:          prdata <= {24'h000000,mode_bits};
       `CDNS_QSPI_INT_MASK:          prdata <= {17'h00000,int_mask_reg[14:0]};
       `CDNS_QSPI_WRITE_PROT_L:      prdata <= {write_protect_lower_reg[31:0]};
       `CDNS_QSPI_WRITE_PROT_U:      prdata <= {write_protect_upper_reg[31:0]};
       `CDNS_QSPI_WRITE_PROT_CTRL:   prdata <= {30'h00000000,write_protect_ctrl_reg[1:0]};
       `CDNS_QSPI_MODULE_ID:         prdata <= {MODULE_ID_FIX_PATCH,MODULE_ID,6'h00,CONFIG_ID};
       `CDNS_QSPI_TX_THRESH:         prdata <= {{(32-`CDNS_QSPI_TXFF_A){1'b0}},tx_threshold};
       `CDNS_QSPI_RX_THRESH:         prdata <= {{(32-`CDNS_QSPI_RXFF_A){1'b0}},rx_threshold};
       `CDNS_QSPI_WRITE_COMP_CTRL:   prdata <= {rep_gap_delay_reg,poll_count,poll_exp_en,poll_disable,poll_polarity,2'b00,poll_bit_index,poll_opcode};
       `CDNS_QSPI_MAX_NO_OF_POLLS:   prdata <= {max_num_of_polls[31:0]};
       `CDNS_QSPI_FLASH_STATUS:      prdata <= {12'h000,status_dummy,7'h00,polling_status};
        default:                prdata <= 32'h00000000;
      endcase
    end

    else
      prdata <= 32'h00000000;
  end

  // PERR
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
      pslverr <= 1'b0;
    else if (!psel || penable)
      pslverr <= 1'b0;

    else if (psel && !penable)
    begin
      case (paddr)
       `CDNS_QSPI_CONFIG:               pslverr <= 1'b0;
       `CDNS_QSPI_DEV_RDINSTR_CONFIG:   pslverr <= 1'b0;
       `CDNS_QSPI_DEV_WRINSTR_CONFIG:   pslverr <= 1'b0;
       `CDNS_QSPI_DEV_SIZE_CONFIG:      pslverr <= 1'b0;
       `CDNS_QSPI_DEV_DELAY:            pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_MEM:        pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_CTRL:       pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_ADD:        pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_RDATA_L:    pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_RDATA_U:    pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_WDATA_L:    pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_CMD_WDATA_U:    pslverr <= 1'b0;
       `CDNS_QSPI_READ_DATA_CAPTURE:    pslverr <= 1'b0;
       `CDNS_QSPI_SRAM_FILL_LEVEL:      pslverr <= 1'b0;
       `CDNS_QSPI_SRAM_PARTITION :      pslverr <= 1'b0;
       `CDNS_QSPI_IND_RD_XFER_CTRL:     pslverr <= 1'b0;
       `CDNS_QSPI_IND_RD_XFER_WMARK:    pslverr <= 1'b0;
       `CDNS_QSPI_IND_RD_XFER_START_ADD:pslverr <= 1'b0;
       `CDNS_QSPI_IND_RD_XFER_NUM_BYTES:pslverr <= 1'b0;
       `CDNS_QSPI_IND_WR_XFER_CTRL:     pslverr <= 1'b0;
       `CDNS_QSPI_IND_WR_XFER_WMARK:    pslverr <= 1'b0;
       `CDNS_QSPI_IND_WR_XFER_START_ADD:pslverr <= 1'b0;
       `CDNS_QSPI_IND_WR_XFER_NUM_BYTES:pslverr <= 1'b0;
       `CDNS_QSPI_IND_AHB_TRIGGER:      pslverr <= 1'b0;
       `CDNS_QSPI_IND_AHB_TRIGGER_RANGE:pslverr <= 1'b0;
       `CDNS_QSPI_PERIPH_CFG:           pslverr <= 1'b0;
       `CDNS_QSPI_REMAP_ADD:            pslverr <= 1'b0;
       `CDNS_QSPI_INT_STATUS:           pslverr <= 1'b0;
       `CDNS_QSPI_MODE_BIT:             pslverr <= 1'b0;
       `CDNS_QSPI_INT_MASK:             pslverr <= 1'b0;
       `CDNS_QSPI_WRITE_PROT_L:         pslverr <= 1'b0;
       `CDNS_QSPI_WRITE_PROT_U:         pslverr <= 1'b0;
       `CDNS_QSPI_WRITE_PROT_CTRL:      pslverr <= 1'b0;
       `CDNS_QSPI_MODULE_ID:            pslverr <= 1'b0;
       `CDNS_QSPI_TX_THRESH:            pslverr <= 1'b0;
       `CDNS_QSPI_RX_THRESH:            pslverr <= 1'b0;
       `CDNS_QSPI_WRITE_COMP_CTRL:      pslverr <= 1'b0;
       `CDNS_QSPI_MAX_NO_OF_POLLS:      pslverr <= 1'b0;
       `CDNS_QSPI_FLASH_STATUS:         pslverr <= 1'b0;
        default:                        pslverr <= 1'b1;
      endcase
    end
  end

  // Registers that are writeable in APB address map
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      cancel_indrd_pclk     <= 1'b0;
      start_indrd_pclk      <= 1'b0;
      indrd_in_progress     <= 1'b0;
      indrd_comp_status     <= 1'b0;
      num_indrd_completed   <= 2'b00;
      indrd_2_queued        <= 1'b0;
      sram_full_ind_err     <= 1'b0;

      cancel_indwr_pclk     <= 1'b0;
      start_indwr_pclk      <= 1'b0;
      indwr_in_progress     <= 1'b0;
      indwr_comp_status     <= 1'b0;
      num_indwr_completed   <= 2'b00;
      indwr_2_queued        <= 1'b0;

      trigger_stig_tog      <= 1'b0;
      trigger_mem_bank_tog  <= 1'b0;
      stig_mem_bank_en      <= 1'b0;
      config_reg            <= {`cdns_qspi_boot_dtr_prot,`cdns_qspi_boot_ahb_decoder,`cdns_qspi_boot_baud_rate,`cdns_qspi_boot_xip,4'h0,`cdns_qspi_boot_perph_sel,
                                `cdns_qspi_boot_perph_dec,2'b01,`cdns_qspi_boot_cpha,`cdns_qspi_boot_cpol,1'b1};
      dev_rd_instr_cfg_reg  <= {`cdns_qspi_boot_read_dummy,1'b0,`cdns_qspi_boot_data_type,`cdns_qspi_boot_addr_type,
                                `cdns_qspi_boot_ddr_en,`cdns_qspi_boot_instr_type,`cdns_qspi_boot_read_opcode};
      dev_wr_instr_cfg_reg  <= 18'h00002;
      dev_size_cfg_reg      <= {`cdns_qspi_boot_size_of_cs3,`cdns_qspi_boot_size_of_cs2,`cdns_qspi_boot_size_of_cs1,`cdns_qspi_boot_size_of_cs0,
                                `cdns_qspi_boot_bytes_per_blk,`cdns_qspi_boot_bytes_per_page,`cdns_qspi_boot_addr_size};
      dev_delay_reg         <= {`cdns_qspi_boot_csda,`cdns_qspi_boot_csdads,`cdns_qspi_boot_cseot,`cdns_qspi_boot_cssot};
      stig_mem_bank_addr    <= {`cdns_qspi_stig_mem_bank_addr_width{1'b0}};
      stig_mem_bank_no_of_bytes <= {`cdns_qspi_stig_mem_bank_data_pck{1'b0}};
      cmd_ctrl_reg          <= 25'h0000000;
      cmd_add_reg           <= 32'h00000000;
      cmd_wdata_reg         <= 64'h00000000_00000000;
      dtr_shift_mo          <= {`cdns_qspi_boot_shift_mo};
      rdata_capture_reg     <= {`cdns_qspi_boot_data_capt_edge,`cdns_qspi_boot_data_capt,1'b1};
      indrd_xfer_wmark_reg    <= 32'h00000000;
      indrd_xfer_start_add_reg<= 32'h00000000;
      indrd_xfer_num_bytes_reg<= 32'h00000000;
      indwr_xfer_wmark_reg    <= 32'hffffffff;
      indwr_xfer_start_add_reg<= 32'h00000000;
      indwr_xfer_num_bytes_reg<= 32'h00000000;
      ind_ahb_trig_add_reg  <= 32'h00000000;
      ind_ahb_trig_add_range_reg  <= 4'h4;
      dma_periph_config_reg <= 8'h00;
      remap_add_reg         <= 32'h00000000;
      int_mask_reg          <= 15'h0000;
      mode_bits             <= 8'h00;
      write_protect_lower_reg <= 32'h00000000;
      write_protect_upper_reg <= 32'h00000000;
      write_protect_ctrl_reg<= 2'h0;
      tx_threshold          <= {{`CDNS_QSPI_TXFF_A-1{1'b0}},1'b1};
      rx_threshold          <= {{`CDNS_QSPI_RXFF_A-1{1'b0}},1'b1};
      rep_gap_delay_reg     <= 8'h00;
      poll_count            <= 8'h01;
      poll_exp_en           <= 1'b0;
      poll_disable          <= 1'b0;
      poll_polarity         <= 1'b0;
      poll_bit_index        <= 3'h0;
      poll_opcode           <= 8'h05;
      sram_partition        <= {1'b1,{`cdns_qspi_sram_depth-1{1'b0}}};      
      status_dummy          <= 4'h0;      
      max_num_of_polls      <= 32'hffffffff;
    end
    else
    begin
      // calculate some indirect mode signals
      if (ind_oflow)
        sram_full_ind_err <= 1'b1;
      else if (write_enable && paddr == `CDNS_QSPI_IND_RD_XFER_CTRL && pwdata[3])
        sram_full_ind_err <= 1'b0;

      if (indrd_flush && indrd_in_progress)
      begin
        indrd_comp_status <= 1'b1;
        indrd_2_queued <= 1'b0;
        indrd_in_progress <= 1'b0;

        if (indrd_2_queued)
          num_indrd_completed <= 2'b10;
        else if (pwdata[5] && write_enable && paddr == `CDNS_QSPI_IND_RD_XFER_CTRL)
          num_indrd_completed <= num_indrd_completed;
        else
          num_indrd_completed <= num_indrd_completed + 2'b01;
      end

      else if (write_enable && paddr == `CDNS_QSPI_IND_RD_XFER_CTRL)
      begin
        cancel_indrd_pclk <= pwdata[1] ? ~cancel_indrd_pclk : cancel_indrd_pclk;
        start_indrd_pclk <= pwdata[0] ? ~start_indrd_pclk : start_indrd_pclk;

        if (indrd_xfer_done && indrd_in_progress)
        begin
          indrd_comp_status <= 1'b1;
          indrd_2_queued <= indrd_2_queued ? pwdata[0] : 1'b0;
          if (!indrd_2_queued && !pwdata[0])
            indrd_in_progress <= 1'b0;
          if (pwdata[5] && indrd_comp_status)
            num_indrd_completed <= num_indrd_completed;
          else
            num_indrd_completed <= num_indrd_completed + 2'b01;
        end
        else
        begin
          if (pwdata[0])
          begin
            indrd_2_queued <= indrd_in_progress;
            indrd_in_progress <= 1'b1;
          end
          if (pwdata[5] && indrd_comp_status)
          begin
            indrd_comp_status <= ~(num_indrd_completed == 2'b01);
            num_indrd_completed <= num_indrd_completed - 2'b01;
          end
        end
      end
      else
      begin
        if (indrd_xfer_done && indrd_in_progress)
        begin
          indrd_comp_status <= 1'b1;
          indrd_2_queued <= 1'b0;
          num_indrd_completed <= num_indrd_completed + 2'b01;
          if (!indrd_2_queued)
            indrd_in_progress <= 1'b0;
        end
      end

      if (indwr_flush && indwr_in_progress)
      begin
        indwr_comp_status <= 1'b1;
        indwr_2_queued <= 1'b0;
        if (!pwdata[0])
          indwr_in_progress <= 1'b0;

        if (indwr_2_queued)
          num_indwr_completed <= 2'b10;
        else if (pwdata[5] && write_enable && paddr == `CDNS_QSPI_IND_WR_XFER_CTRL)
          num_indwr_completed <= num_indwr_completed;
        else
          num_indwr_completed <= num_indwr_completed + 2'b01;
      end

      else if (write_enable && paddr == `CDNS_QSPI_IND_WR_XFER_CTRL)
      begin
        cancel_indwr_pclk <= pwdata[1] ? ~cancel_indwr_pclk : cancel_indwr_pclk;
        start_indwr_pclk <= pwdata[0] ? ~start_indwr_pclk : start_indwr_pclk;

        if (indwr_xfer_done && indwr_in_progress)
        begin
          indwr_comp_status <= 1'b1;
          indwr_2_queued <= indwr_2_queued ? pwdata[0] : 1'b0;
          if (!indwr_2_queued && !pwdata[0])
            indwr_in_progress <= 1'b0;
          if (pwdata[5] && indwr_comp_status)
            num_indwr_completed <= num_indwr_completed;
          else
            num_indwr_completed <= num_indwr_completed + 2'b01;
        end
        else
        begin
          if (pwdata[0])
          begin
            indwr_2_queued <= indwr_in_progress;
            indwr_in_progress <= 1'b1;
          end
          if (pwdata[5] && indwr_comp_status)
          begin
            indwr_comp_status <= ~(num_indwr_completed == 2'b01);
            num_indwr_completed <= num_indwr_completed - 2'b01;
          end
        end
      end
      else
      begin
        if (indwr_xfer_done && indwr_in_progress)
        begin
          indwr_comp_status <= 1'b1;
          indwr_2_queued <= 1'b0;
          num_indwr_completed <= num_indwr_completed + 2'b01;
          if (!indwr_2_queued)
            indwr_in_progress <= 1'b0;
        end
      end


      // STIG - Flash Command Control register ...
      // Ignore a write to bit zero if an existing command is in progress ....
      if (write_enable && paddr == `CDNS_QSPI_FLASH_CMD_CTRL)
      begin
        cmd_ctrl_reg <= pwdata[31:7];
        stig_mem_bank_en <= pwdata[2];
        if (pwdata[0])
          trigger_stig_tog  <= ~trigger_stig_tog;
      end
      
      // STIG - Using Memory Bank (similar triggering approach as for basic STIG)
      // Ignore a write to bit zero if an existing command is in progress ....
      if (write_enable && paddr == `CDNS_QSPI_FLASH_CMD_MEM)
      begin
        stig_mem_bank_addr        <=  pwdata[20+`cdns_qspi_stig_mem_bank_addr_width-1:20]; 
        stig_mem_bank_no_of_bytes <=  pwdata[16+`cdns_qspi_stig_mem_bank_data_pck-1:16]; 
        if (pwdata[0])
          trigger_mem_bank_tog  <= ~trigger_mem_bank_tog;
      end      

      if (write_enable)
      begin
        case (paddr)
         `CDNS_QSPI_CONFIG:            config_reg <= {pwdata[24:7],pwdata[2:0]};
         `CDNS_QSPI_DEV_RDINSTR_CONFIG:dev_rd_instr_cfg_reg <= { pwdata[28:24],// dummy
                                                            pwdata[20],   // mode en
                                                            pwdata[17:16],// data type
                                                            pwdata[13:12],// addr type
                                                            pwdata[10],   // dtr en
                                                            pwdata[9:0]}; // opcode+instr type
         `CDNS_QSPI_DEV_WRINSTR_CONFIG:dev_wr_instr_cfg_reg <= { pwdata[28:24],// dummy
                                                            pwdata[17:16],// data type
                                                            pwdata[13:12],// addr type
                                                            pwdata[8],    // WEL disable
                                                            pwdata[7:0]}; // opcode
         `CDNS_QSPI_DEV_SIZE_CONFIG:   dev_size_cfg_reg <= pwdata[28:0];
         `CDNS_QSPI_DEV_DELAY:         dev_delay_reg <= pwdata[31:0];
         `CDNS_QSPI_FLASH_CMD_ADD:     cmd_add_reg <= pwdata[31:0];
         `CDNS_QSPI_FLASH_CMD_WDATA_L: cmd_wdata_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_FLASH_CMD_WDATA_U: cmd_wdata_reg[63:32] <= pwdata[31:0];
         `CDNS_QSPI_READ_DATA_CAPTURE: begin
                                        rdata_capture_reg[5:0] <= pwdata[5:0]; 
                                        dtr_shift_mo[3:0] <= pwdata[19:16]; 
                                       end
         `CDNS_QSPI_SRAM_PARTITION   : sram_partition[`cdns_qspi_sram_depth-1:0] <= pwdata[`cdns_qspi_sram_depth-1:0];
         `CDNS_QSPI_IND_RD_XFER_WMARK:    indrd_xfer_wmark_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_RD_XFER_START_ADD:if (!indrd_2_queued)
                                        indrd_xfer_start_add_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_RD_XFER_NUM_BYTES:if (!indrd_2_queued)
                                        indrd_xfer_num_bytes_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_WR_XFER_WMARK:    indwr_xfer_wmark_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_WR_XFER_START_ADD:if (!indwr_2_queued)
                                        indwr_xfer_start_add_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_WR_XFER_NUM_BYTES:if (!indwr_2_queued)
                                        indwr_xfer_num_bytes_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_AHB_TRIGGER:   ind_ahb_trig_add_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_IND_AHB_TRIGGER_RANGE:   ind_ahb_trig_add_range_reg <= pwdata[3:0];
         `CDNS_QSPI_PERIPH_CFG:        dma_periph_config_reg <= {pwdata[11:8],pwdata[3:0]};
         `CDNS_QSPI_REMAP_ADD:         remap_add_reg <= pwdata[31:0];
         `CDNS_QSPI_MODE_BIT:          mode_bits <= pwdata[7:0];
         `CDNS_QSPI_INT_MASK:          int_mask_reg[14:0] <= pwdata[14:0];
         `CDNS_QSPI_WRITE_PROT_L:      write_protect_lower_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_WRITE_PROT_U:      write_protect_upper_reg[31:0] <= pwdata[31:0];
         `CDNS_QSPI_WRITE_PROT_CTRL:   write_protect_ctrl_reg[1:0] <= pwdata[1:0];
         `CDNS_QSPI_TX_THRESH:         tx_threshold <= pwdata[`CDNS_QSPI_TXFF_A-1:0];
         `CDNS_QSPI_RX_THRESH:         rx_threshold <= pwdata[`CDNS_QSPI_RXFF_A-1:0];
         `CDNS_QSPI_WRITE_COMP_CTRL:   begin                                
                                        rep_gap_delay_reg <= pwdata[31:24];
                                        poll_count        <= pwdata[23:16];                                    
                                        poll_exp_en       <= pwdata[15];
                                        poll_disable      <= pwdata[14];
                                        poll_polarity     <= pwdata[13];
                                        poll_bit_index    <= pwdata[10:8];
                                        poll_opcode       <= pwdata[7:0];  
                                       end
         `CDNS_QSPI_MAX_NO_OF_POLLS:   max_num_of_polls <= pwdata[31:0];
         `CDNS_QSPI_FLASH_STATUS:      status_dummy <= pwdata[19:16];
          default:                ;
        endcase
      end
    end
  end



  // ------------------------------------------------------------------------------
  // Interrupt Logic
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      int_status_reg        <= 15'h0000;
    end
    else
    begin
      `ifdef CDNS_QSPI_INT_READ_CLEAR
      if (read_enable && paddr == `CDNS_QSPI_INT_STATUS)
        int_status_reg[14:0] <= int_status_src_pulse & int_mask_reg;
      else
        int_status_reg[14:0] <= (int_status_src_pulse | int_status_reg) & int_mask_reg ;
      `else
      if (write_enable && paddr == `CDNS_QSPI_INT_STATUS)
        int_status_reg[14:0] <= ((int_status_reg & ~pwdata[14:0]) | int_status_src_pulse)
                                  & int_mask_reg;
      else
        int_status_reg[14:0] <= (int_status_src_pulse | int_status_reg) & int_mask_reg ;
      `endif
    end
  end

  assign int_status_lat = (int_status_reg | int_status_src_pulse) & int_mask_reg;

  // ---------------------------------------------------------
  // Interrupt Logic
  // Most of the sources come from non-apb clock domains., so we need
  // to resync them

  // First create toggles from pulse inputs
  // Those sources that are not included here are already toggles







cdns_syncflop i_cdns_qspi_tx_uflow_meta (
  .clk     (pclk),
  .reset_n (n_preset),
  .din     (tx_uflow_tog),
  .dout    (tx_uflow_sync)
);

cdns_syncflop i_cdns_qspi_indrd_xfer_done_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indrd_xfer_done_tog),
  .dout  (indrd_xfer_done_sync)
);

cdns_syncflop i_cdns_qspi_indwr_xfer_done_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indwr_xfer_done_tog),
  .dout  (indwr_xfer_done_sync)
);

cdns_syncflop i_cdns_qspi_indrd_flush_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indrd_flush_tog),
  .dout  (indrd_flush_sync)
);

cdns_syncflop i_cdns_qspi_indwr_flush_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indwr_flush_tog),
  .dout  (indwr_flush_sync)
);

cdns_syncflop i_cdns_qspi_ind_oflow_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (ind_oflow_tog),
  .dout  (ind_oflow_sync)
);

cdns_syncflop i_cdns_qspi_ahb_wr_prot_err_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (ahb_wr_prot_err_tog),
  .dout  (ahb_wr_prot_err_sync)
);

cdns_syncflop i_cdns_qspi_ahb_access_err_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (ahb_access_err_tog),
  .dout  (ahb_access_err_sync)
);

cdns_syncflop i_cdns_qspi_indrd_wmark_trig_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indrd_wmark_trig_tog),
  .dout  (indrd_wmark_trig_sync)
);

cdns_syncflop i_cdns_qspi_indwr_wmark_trig_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (indwr_wmark_trig_tog),
  .dout  (indwr_wmark_trig_sync)
);

cdns_syncflop i_cdns_qspi_rx_overflow_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (rx_oflow_tog),
  .dout  (rx_overflow_sync)
);

cdns_syncflop i_cdns_qspi_rx_notempty_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (rx_notempty_refclk),
  .dout  (rx_notempty_sync)
);

cdns_syncflop i_cdns_qspi_rx_full_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (rx_full_refclk),
  .dout  (rx_full_sync)
);

cdns_syncflop i_cdns_qspi_tx_notempty_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (tx_notfull_hclk),
  .dout  (tx_notempty_sync)
);

cdns_syncflop i_cdns_qspi_tx_full_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (tx_full_hclk),
  .dout  (tx_full_sync)
);

cdns_syncflop i_cdns_qspi_idle_spi_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (idle_spi),
  .dout  (idle_spi_sync)
);

cdns_syncflop i_cdns_qspi_expiration_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (expiration_tog),
  .dout  (expiration_sync)
);


  // Interrupt source of the STIG completion is located in
  // pclk domain hence toggle source for it can be generated
  // separately:
  
  // This creates delayed stig_in_progress indicator 
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
      stig_in_progress_pck_d1 <= 1'b0;
    else
      stig_in_progress_pck_d1 <= stig_in_progress | stig_in_progress_waiting;
  end
  
  // This generates pulse for STIG completion interrupt toggle source
  // The pulse is generated when stig_in_progress signal goes to low
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      stig_completion <= 1'b0;
    end
    else
    begin
      stig_completion <= ~(stig_in_progress | stig_in_progress_waiting) & stig_in_progress_pck_d1;  
    end
  end  
  
  // Synchronize ref_clk / hclk signals into apb domain
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      tx_uflow_d1             <= 1'b0;
      indrd_xfer_done_d1      <= 1'b0;
      indwr_xfer_done_d1      <= 1'b0;
      ind_oflow_d1            <= 1'b0;
      ahb_wr_prot_err_d1      <= 1'b0;
      ahb_access_err_d1       <= 1'b0;
      indrd_wmark_trig_d1     <= 1'b0;
      indwr_wmark_trig_d1     <= 1'b0;
      indrd_flush_d1          <= 1'b0;
      indwr_flush_d1          <= 1'b0;
      rx_overflow_d1          <= 1'b0;
      rx_notempty_d1          <= 1'b0;
      rx_full_d1              <= 1'b0;
      tx_notempty_d1          <= 1'b0;
      tx_full_d1              <= 1'b0;
      ind_trigger_oflow       <= 1'b0;
      expiration_d1           <= 1'b0;
    end
    else
    begin
      tx_uflow_d1             <= tx_uflow_sync;
      indrd_xfer_done_d1      <= indrd_xfer_done_sync;
      indwr_xfer_done_d1      <= indwr_xfer_done_sync;
      indrd_flush_d1          <= indrd_flush_sync;
      indwr_flush_d1          <= indwr_flush_sync;
      ind_oflow_d1            <= ind_oflow_sync;
      ahb_wr_prot_err_d1      <= ahb_wr_prot_err_sync;
      ahb_access_err_d1       <= ahb_access_err_sync;
      indrd_wmark_trig_d1     <= indrd_wmark_trig_sync;
      indwr_wmark_trig_d1     <= indwr_wmark_trig_sync;
      rx_overflow_d1          <= rx_overflow_sync;
      rx_notempty_d1          <= rx_notempty_sync;
      rx_full_d1              <= rx_full_sync;
      tx_notempty_d1          <= tx_notempty_sync;
      tx_full_d1              <= tx_full_sync;
      ind_trigger_oflow       <= (write_enable & paddr == `CDNS_QSPI_IND_RD_XFER_CTRL &
                                  pwdata[0] & indrd_2_queued) |
                                 (write_enable & paddr == `CDNS_QSPI_IND_WR_XFER_CTRL &
                                  pwdata[0] & indwr_2_queued);
      expiration_d1           <= expiration_sync;
    end
  end
  assign tx_underflow       = tx_uflow_d1           ^ tx_uflow_sync;
  assign indrd_xfer_done    = indrd_xfer_done_d1    ^ indrd_xfer_done_sync;
  assign indwr_xfer_done    = indwr_xfer_done_d1    ^ indwr_xfer_done_sync;
  assign ind_oflow          = ind_oflow_d1          ^ ind_oflow_sync;
  assign indrd_flush        = indrd_flush_d1        ^ indrd_flush_sync;
  assign indwr_flush        = indwr_flush_d1        ^ indwr_flush_sync;
  assign ahb_wr_prot_err    = ahb_wr_prot_err_d1    ^ ahb_wr_prot_err_sync;
  assign ahb_access_err     = ahb_access_err_d1     ^ ahb_access_err_sync;
  assign indrd_wmark_trig   = indrd_wmark_trig_d1   ^ indrd_wmark_trig_sync;
  assign indwr_wmark_trig   = indwr_wmark_trig_d1   ^ indwr_wmark_trig_sync;
  assign rx_overflow        = rx_overflow_d1        ^ rx_overflow_sync;
  assign rx_notempty        = rx_notempty_d1        ^ rx_notempty_sync;
  assign rx_full            = rx_full_d1            ^ rx_full_sync;
  assign tx_notempty        = tx_notempty_d1        ^ tx_notempty_sync;
  assign tx_full            = tx_full_d1            ^ tx_full_sync;
  assign expiration         = expiration_d1         ^ expiration_sync;

  assign int_status_src_pulse = {
                                  stig_completion,
                                  expiration,
                                  ind_oflow,
                                  rx_full,
                                  rx_notempty,
                                  tx_full,
                                  tx_notempty,
                                  rx_overflow,
                                  (indrd_wmark_trig|indwr_wmark_trig),
                                  ahb_access_err,
                                  ahb_wr_prot_err,
                                  ind_trigger_oflow,
                                  ( indrd_xfer_done|
                                    indwr_xfer_done|
                                    indrd_flush|
                                    indwr_flush),
                                  tx_underflow,
                                  1'b0
                                };

  // Capture pulses
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      ahb_access_err_capt_tog  <= 1'b0;
      ahb_wr_prot_err_capt_tog <= 1'b0;
      indrd_xfer_done_capt_tog <= 1'b0;
      indrd_wmark_trig_capt_tog <= 1'b0;
      indwr_xfer_done_capt_tog <= 1'b0;
      indwr_wmark_trig_capt_tog <= 1'b0;
      indrd_flush_capt_tog <= 1'b0;
      indwr_flush_capt_tog <= 1'b0;
    end
    else
    begin
      if (ahb_access_err)
        ahb_access_err_capt_tog  <= ~ahb_access_err_capt_tog;
      if (ahb_wr_prot_err)
        ahb_wr_prot_err_capt_tog <= ~ahb_wr_prot_err_capt_tog;
      if (indrd_xfer_done)
        indrd_xfer_done_capt_tog <= ~indrd_xfer_done_capt_tog;
      if (indwr_xfer_done)
        indwr_xfer_done_capt_tog <= ~indwr_xfer_done_capt_tog;
      if (indrd_wmark_trig)
        indrd_wmark_trig_capt_tog <= ~indrd_wmark_trig_capt_tog;
      if (indwr_wmark_trig)
        indwr_wmark_trig_capt_tog <= ~indwr_wmark_trig_capt_tog;
      if (indrd_flush)
        indrd_flush_capt_tog <= ~indrd_flush_capt_tog;
      if (indwr_flush)
        indwr_flush_capt_tog <= ~indwr_flush_capt_tog;
    end
  end

cdns_syncflop i_cdns_qspi_ahb_access_err_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (ahb_access_err_capt_tog),
  .dout  (ahb_access_err_capt_sync)
);

cdns_syncflop i_cdns_qspi_ahb_wr_prot_err_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (ahb_wr_prot_err_capt_tog),
  .dout  (ahb_wr_prot_err_capt_sync)
);

cdns_syncflop i_cdns_qspi_indrd_xfer_done_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indrd_xfer_done_capt_tog),
  .dout  (indrd_xfer_done_capt_sync)
);

cdns_syncflop i_cdns_qspi_indrd_wmark_trig_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indrd_wmark_trig_capt_tog),
  .dout  (indrd_wmark_trig_capt_sync)
);

cdns_syncflop i_cdns_qspi_indwr_xfer_done_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indwr_xfer_done_capt_tog),
  .dout  (indwr_xfer_done_capt_sync)
);

cdns_syncflop i_cdns_qspi_indwr_wmark_trig_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indwr_wmark_trig_capt_tog),
  .dout  (indwr_wmark_trig_capt_sync)
);

cdns_syncflop i_cdns_qspi_indrd_flush_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indrd_flush_capt_tog),
  .dout  (indrd_flush_capt_sync)
);

cdns_syncflop i_cdns_qspi_indwr_flush_capt_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (indwr_flush_capt_tog),
  .dout  (indwr_flush_capt_sync)
);

  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
    begin
      ahb_access_err_capt_d1    <= 1'b0;
      ahb_wr_prot_err_capt_d1   <= 1'b0;
      indrd_xfer_done_capt_d1   <= 1'b0;
      indrd_wmark_trig_capt_d1  <= 1'b0;
      indwr_xfer_done_capt_d1   <= 1'b0;
      indwr_wmark_trig_capt_d1  <= 1'b0;
      indrd_flush_capt_d1       <= 1'b0;
      indwr_flush_capt_d1       <= 1'b0;
    end
    else
    begin
      ahb_access_err_capt_d1    <= ahb_access_err_capt_sync;
      ahb_wr_prot_err_capt_d1   <= ahb_wr_prot_err_capt_sync;
      indrd_xfer_done_capt_d1   <= indrd_xfer_done_capt_sync;
      indrd_wmark_trig_capt_d1    <= indrd_wmark_trig_capt_sync;
      indwr_xfer_done_capt_d1   <= indwr_xfer_done_capt_sync;
      indwr_wmark_trig_capt_d1    <= indwr_wmark_trig_capt_sync;
      indrd_flush_capt_d1       <= indrd_flush_capt_sync;
      indwr_flush_capt_d1       <= indwr_flush_capt_sync;
    end
  end
assign ahb_access_err_capt   = ahb_access_err_capt_d1 ^ ahb_access_err_capt_sync;
assign ahb_wr_prot_err_capt  = ahb_wr_prot_err_capt_d1 ^ ahb_wr_prot_err_capt_sync;
assign indrd_xfer_done_capt  = indrd_xfer_done_capt_d1 ^ indrd_xfer_done_capt_sync;
assign indwr_xfer_done_capt  = indwr_xfer_done_capt_d1 ^ indwr_xfer_done_capt_sync;
assign indrd_wmark_trig_capt = indrd_wmark_trig_capt_d1 ^ indrd_wmark_trig_capt_sync;
assign indwr_wmark_trig_capt = indwr_wmark_trig_capt_d1 ^ indwr_wmark_trig_capt_sync;
assign indrd_flush_capt = indrd_flush_capt_d1 ^ indrd_flush_capt_sync;
assign indwr_flush_capt = indwr_flush_capt_d1 ^ indwr_flush_capt_sync;


always @ (posedge pclk or negedge n_preset)
begin
  if (!n_preset)
   interrupt <= 1'b0;
  else
   interrupt <= |int_status_lat;
end

cdns_syncflop i_cdns_qspi_sram_fill_captured_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (sram_fill_captured_pclk),
  .dout  (sram_fill_captured_sync)
);

// Synchronize SRAM fill level into pclk domain
always @ (posedge hclk or negedge n_hreset)
  if (!n_hreset)
  begin
    sample_sram_fill        <= 1'b0;
    sram_fill_hold          <= {(`cdns_qspi_sram_depth*2){1'b0}};
    initial_capt_hclk       <= 1'b0;
    sram_fill_captured_d1   <= 1'b0;
  end
  else
  begin
    sram_fill_captured_d1   <= sram_fill_captured_sync;
    initial_capt_hclk       <= qspi_enable_hclk;
    if (sram_fill_captured_d1 ^ sram_fill_captured_sync)
    begin
      sample_sram_fill  <= ~sample_sram_fill;
      sram_fill_hold    <= {indwr_sram_fill_level,indrd_sram_fill_level};
    end
  end

cdns_syncflop i_cdns_qspi_sample_sram_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (sample_sram_fill),
  .dout  (sample_sram_sync)
);
cdns_syncflop i_cdns_qspi_initial_capt_hclk_meta (
  .clk   (pclk),
  .reset_n (n_preset),
  .din   (initial_capt_hclk),
  .dout  (initial_capt_hclk_sync)
);

  reg initial_capt_hclk_sync_d1;
  // Ensure the first sample point occurs after both HCLK and PCLK is running
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      sample_sram_d1          <= 1'b0;
      sram_fill_captured_pclk <= 1'b0;
      initial_capt_hclk_sync_d1 <= 1'b0;
      sram_fill_level_pclk    <= {(`cdns_qspi_sram_depth*2){1'b0}};
    end
    else
    begin
      sample_sram_d1    <= sample_sram_sync;
      initial_capt_hclk_sync_d1 <= initial_capt_hclk_sync;
      if ((sample_sram_d1 ^ sample_sram_sync) || (initial_capt_hclk_sync ^ initial_capt_hclk_sync_d1))
      begin
        sram_fill_captured_pclk <= ~sram_fill_captured_pclk;
        sram_fill_level_pclk    <= sram_fill_hold;
      end
    end
  end

// sync modules into hclk  

cdns_syncflop i_cdns_qspi_ahb_dec_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[19]),
  .dout  (ahb_dec_en_sync)
);

cdns_syncflop i_cdns_qspi_ahb_remap_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[12]),
  .dout  (ahb_remap_en_sync)
);

cdns_syncflop i_cdns_qspi_dma_pif_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[11]),
  .dout  (dma_pif_en_sync)
);

cdns_syncflop i_cdns_qspi_legacy_mode_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[4]),
  .dout  (legacy_mode_en_sync)
);

cdns_syncflop i_cdns_qspi_direct_access_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[3]),
  .dout  (direct_access_en_sync)
);

cdns_syncflop i_cdns_qspi_qspi_enable_hc_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (config_reg[0]),
  .dout  (qspi_enable_hc_sync)
);

cdns_syncflop i_cdns_qspi_start_indrd_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (start_indrd_pclk),
  .dout  (start_indrd_sync)
);

cdns_syncflop i_cdns_qspi_cancel_indrd_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (cancel_indrd_pclk),
  .dout  (cancel_indrd_sync)
);

cdns_syncflop i_cdns_qspi_start_indwr_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (start_indwr_pclk),
  .dout  (start_indwr_sync)
);

cdns_syncflop i_cdns_qspi_cancel_indwr_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (cancel_indwr_pclk),
  .dout  (cancel_indwr_sync)
);

cdns_syncflop i_cdns_qspi_ahb_wr_protection_en_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (write_protect_ctrl_reg[1]),
  .dout  (ahb_wr_protection_en_sync)
);

cdns_syncflop i_cdns_qspi_trigger_stig_tog_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (trigger_stig_tog),
  .dout  (trigger_stig_tog_sync)
);

cdns_syncflop i_cdns_qspi_trigger_mem_bank_tog_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (trigger_mem_bank_tog),
  .dout  (trigger_mem_bank_tog_sync)
);

// Assign configuration signals from APB registers
  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
    begin
      start_indrd_d1            <= 1'b0;
      cancel_indrd_d1           <= 1'b0;
      start_indwr_d1            <= 1'b0;
      cancel_indwr_d1           <= 1'b0;
      trigger_stig_tog_d1       <= 1'b0;
      trigger_mem_bank_tog_d1   <= 1'b0;
    end
    else
    begin
      start_indrd_d1            <= start_indrd_sync;
      cancel_indrd_d1           <= cancel_indrd_sync;
      start_indwr_d1            <= start_indwr_sync;
      cancel_indwr_d1           <= cancel_indwr_sync;
      trigger_stig_tog_d1       <= trigger_stig_tog_sync;
      trigger_mem_bank_tog_d1   <= trigger_mem_bank_tog_sync;
    end
  end

//sync modules into ref_clk
cdns_syncflop i_cdns_qspi_write_protect_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[10]),
  .dout  (write_protect_sync)
);

cdns_syncflop i_cdns_qspi_qspi_enable_rc_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[0]),
  .dout  (qspi_enable_rc_sync)
);

cdns_syncflop i_cdns_qspi_lb_clk_enable_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (~rdata_capture_reg[0]),
  .dout  (lb_clk_enable_sync)
);

cdns_syncflop i_cdns_qspi_enter_xip_next_refclk_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[13]),
  .dout  (enter_xip_next_refclk_sync)
);

cdns_syncflop i_cdns_qspi_enter_xip_now_refclk_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[14]),
  .dout  (enter_xip_now_refclk_sync)
);

cdns_syncflop i_cdns_qspi_ahb_dec_en_refclk_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[19]),
  .dout  (ahb_dec_en_refclk_sync)
);


cdns_syncflop i_cdns_qspi_dtr_prot_refclk_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (config_reg[20]),
  .dout  (dtr_prot_sync)
);


// STIG logic
  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
    begin
      stig_valid <= 1'b0;
      stig_done_tog_hclk  <= 1'b0;
    end
    else
    begin
      if (stig_valid && stig_ready)
      begin
        stig_done_tog_hclk  <= ~stig_done_tog_hclk;
        stig_valid <= 1'b0;
      end
      else if ((trigger_stig_tog_d1 ^ trigger_stig_tog_sync) && !stig_valid && !polling_status[8])
        stig_valid <= 1'b1;
    end
  end
  
  // STIG Memory bank logic
  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
    begin
      mem_bank_valid <= 1'b0;
      mem_bank_done_tog_hclk  <= 1'b0;
    end
    else
    begin
      if (mem_bank_valid && stig_mem_bank_ready)
      begin
        mem_bank_done_tog_hclk  <= ~mem_bank_done_tog_hclk;
        mem_bank_valid <= 1'b0;
      end
      else if ((trigger_mem_bank_tog_d1 ^ trigger_mem_bank_tog_sync) && !mem_bank_valid)
        mem_bank_valid <= 1'b1;
    end
  end  

  // Detection of STIG during auto-polling phase
  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
    begin
      stig_during_poll_valid <= 1'b0;
    end
    else
    begin
      if ((trigger_stig_tog_d1 ^ trigger_stig_tog_sync) && polling_status[8])
        stig_during_poll_valid <= 1'b1;
      else if (stig_during_poll_ack)
        stig_during_poll_valid <= 1'b0;
    end
  end

  cdns_syncflop i_cdns_qspi_stig_during_poll_done_meta (
  .clk   (hclk),
  .reset_n (n_hreset),
  .din   (stig_during_poll_done),
  .dout  (stig_during_poll_done_sync)
);

  always @ (posedge hclk or negedge n_hreset)
  begin
    if (!n_hreset)
      begin
        stig_during_poll_done_d1 <= 1'b0;
        stig_during_poll_ack     <= 1'b0;
      end
      else
      begin
        stig_during_poll_done_d1 <= stig_during_poll_done_sync;
        stig_during_poll_ack <= ~stig_during_poll_done_sync & stig_during_poll_done_d1;
      end
  end

  // Synchronization to the reference domain
cdns_syncflop i_cdns_qspi_stig_during_poll_meta (
  `ifdef cdns_qspi_include_ref_clk
    .clk   (ref_clk),
    .reset_n   (n_ref_rst),
  `else
    .clk   (hclk),
    .reset_n (n_hreset),
  `endif
  .din   (stig_during_poll_valid),
  .dout  (stig_during_poll_sync)
);

  assign stig_during_poll = stig_during_poll_sync;

  // Generate the STIG in progress status bit and sample the data back from the CMD GEN

cdns_syncflop i_cdns_qspi_stig_in_progress_meta (
  .clk   (pclk),
  .reset_n   (n_preset),
  .din   (stig_done_tog_hclk),
  .dout  (stig_in_progress_sync)
);

  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      stig_in_progress_d1   <= 1'b0;
      stig_in_progress      <= 1'b0;
      cmd_rdata_reg         <= 64'h0000000000000000;
    end
    else
    begin
      stig_in_progress_d1   <= stig_in_progress_sync;
      if (stig_in_progress_d1 ^ stig_in_progress_sync) // sample the stig_rdata bus - should be stable
      begin
        cmd_rdata_reg     <= stig_rdata;
        stig_in_progress  <= 1'b0;
      end
      else if (write_enable && paddr == `CDNS_QSPI_FLASH_CMD_CTRL && pwdata[0])
        stig_in_progress  <= 1'b1;
    end
  end

  // wait until SPI transfer is launched
  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      stig_in_progress_waiting   <= 1'b0;
    end
    else
    begin
      // set this signal only when STIG was granted during idle state
      // it would effect only for tx_direction commands because for
      // bi-directional ones STIG returns ready flag after SPI transfer
      if ((stig_in_progress_d1 ^ stig_in_progress_sync) & idle_spi_sync & ~|stig_num_rdata_bytes)
      begin
        stig_in_progress_waiting     <= 1'b1;
      end
      else if (~idle_spi_sync)
        stig_in_progress_waiting  <= 1'b0;
    end
  end
  

  // Generate Memory Bank request status
cdns_syncflop i_cdns_qspi_mem_bank_in_progress_meta (
  .clk   (pclk),
  .reset_n   (n_preset),
  .din   (mem_bank_done_tog_hclk),
  .dout  (mem_bank_in_progress_sync)
);

  always @ (posedge pclk or negedge n_preset)
  begin
    if (!n_preset)
    begin
      mem_bank_in_progress_d1   <= 1'b0;
      mem_bank_in_progress      <= 1'b0;
      mem_bank_rdata            <= 8'h00;
    end
    else
    begin
      mem_bank_in_progress_d1   <= mem_bank_in_progress_sync;
      if (mem_bank_in_progress_d1 ^ mem_bank_in_progress_sync) // sample the rdata bus - should be stable
      begin
        mem_bank_rdata    <= stig_mem_bank_rd_data;
        mem_bank_in_progress  <= 1'b0;
      end
      else if (write_enable && paddr == `CDNS_QSPI_FLASH_CMD_MEM && pwdata[0])
        mem_bank_in_progress  <= 1'b1;
    end
  end  


// QSPI Config Reg
assign ahb_dec_en_hclk      = ahb_dec_en_sync;
assign ahb_dec_en_refclk    = ahb_dec_en_refclk_sync;
assign dtr_prot_refclk      = dtr_prot_sync;
assign baud_rate            = config_reg[18:15];
assign enter_xip_now_refclk   = enter_xip_now_refclk_sync;
assign enter_xip_next_refclk  = enter_xip_next_refclk_sync;
assign ahb_remap_en_hclk    = ahb_remap_en_sync;
assign dma_pif_en_hclk      = dma_pif_en_sync;
assign write_protect        = write_protect_sync;
assign device_ss            = config_reg[6+P_SIZE-1:6];
assign pdec                 = config_reg[5];
assign legacy_mode_en_hclk  = legacy_mode_en_sync;
assign direct_access_en_hclk= direct_access_en_sync;
assign cpha                 = config_reg[2];
assign cpol                 = config_reg[1];
assign qspi_enable_refclk   = qspi_enable_rc_sync;
assign qspi_enable_hclk     = qspi_enable_hc_sync;

// Device RD Config Register
assign num_dummy_clks_read  = dev_rd_instr_cfg_reg[20:16];
assign mode_bits_en         = dev_rd_instr_cfg_reg[15];
assign data_xfer_type_rd    = dev_rd_instr_cfg_reg[14:13];
assign address_xfer_type_rd = dev_rd_instr_cfg_reg[12:11];
assign dtr_mode             = dev_rd_instr_cfg_reg[10];
assign instruction_type     = dev_rd_instr_cfg_reg[9:8];
assign read_opcode          = dev_rd_instr_cfg_reg[7:0];

// Device WR Config Register
assign num_dummy_clks_write = dev_wr_instr_cfg_reg[17:13];
assign data_xfer_type_wr    = dev_wr_instr_cfg_reg[12:11];
assign address_xfer_type_wr = dev_wr_instr_cfg_reg[10:9];
assign wel_precomm_dis      = dev_wr_instr_cfg_reg[8];
assign write_opcode         = dev_wr_instr_cfg_reg[7:0];

// Device Size Config Register
assign cs_size_decoder      = dev_size_cfg_reg[28:21];
assign num_bytes_in_block   = dev_size_cfg_reg[20:16];
assign num_bytes_in_page    = dev_size_cfg_reg[15:4];
assign num_addr_bytes       = dev_size_cfg_reg[3:0];

// QSPI Device Delay Register
assign d_init               = dev_delay_reg[7:0];
assign d_after              = dev_delay_reg[15:8];
assign d_btwn               = dev_delay_reg[23:16];
assign d_nss                = dev_delay_reg[31:24];

// QSPI Flash Command Control Register
assign stig_opcode          = cmd_ctrl_reg[24:17];
assign stig_num_rdata_bytes = cmd_ctrl_reg[16:13];
assign stig_addr_en         = cmd_ctrl_reg[12];
assign stig_mode_en         = cmd_ctrl_reg[11];
assign stig_num_addr_bytes  = cmd_ctrl_reg[10:9];
assign stig_num_wdata_bytes = cmd_ctrl_reg[8:5];
assign stig_num_dummy_clks  = cmd_ctrl_reg[4:0];
assign stig_add             = cmd_add_reg;
assign stig_wdata           = cmd_wdata_reg;

// Read Data Capture Register
assign capture_edge_arbiter = rdata_capture_reg[5];
assign rd_data_capture_dly  = rdata_capture_reg[4:1];
assign lb_clk_enable_refclk = lb_clk_enable_sync;

                           
// Calculation of Memory Bank data stages (in the power of two)
// When value configured number of bytes to transfer in extended STIG exceeds the Memory Bank size, the maximum possible value is being assigned automatically
// (equals Memory Bank size)
assign stig_mem_bank_stages_precalc = ({{{`cdns_qspi_stig_mem_bank_addr_width-4}{1'b0}},2'b10}) << stig_mem_bank_no_of_bytes;
assign stig_mem_bank_stages = |stig_mem_bank_stages_precalc ? stig_mem_bank_stages_precalc : ({1'b1,{{`cdns_qspi_stig_mem_bank_addr_width-3}{1'b0}}}); 

// ind xfer Control
assign cancel_indrd_hclk = cancel_indrd_sync ^ cancel_indrd_d1;
always @(posedge hclk or negedge n_hreset)
begin
  if (!n_hreset)
  begin
    start_indrd_hclk  <= 1'b0;
    start_indrd_hold       <= 1'b0;
    indrd_xfer_in_prog_hclk <= 1'b0;
  end
  else
  begin
    if ((start_indrd_sync ^ start_indrd_d1) && !start_indrd_hold)
    begin
      indrd_xfer_in_prog_hclk <= 1'b1;
      if (indrd_xfer_in_prog_hclk)
      begin
        if (indrd_xfer_flash_done || indrd_flush_capt)
        begin
          start_indrd_hclk  <= 1'b1;
          start_indrd_hold  <= 1'b0;
        end
        else
        begin
          start_indrd_hclk  <= 1'b0;
          start_indrd_hold  <= 1'b1;
        end
      end
      else
      begin
        start_indrd_hclk  <= 1'b1;
        start_indrd_hold  <= 1'b0;
      end
    end
    else
    begin
      if (indrd_flush_capt)
      begin
        start_indrd_hclk  <= 1'b0;
        start_indrd_hold  <= 1'b0;
        indrd_xfer_in_prog_hclk <= 1'b0;
      end
      else if (indrd_xfer_in_prog_hclk)
      begin
        if (indrd_xfer_flash_done)
        begin
          start_indrd_hclk  <= start_indrd_hold;
          start_indrd_hold  <= 1'b0;
          indrd_xfer_in_prog_hclk <= start_indrd_hold;
        end
        else
        begin
          start_indrd_hclk  <= 1'b0;
          start_indrd_hold  <= start_indrd_hold;
          indrd_xfer_in_prog_hclk <= indrd_xfer_in_prog_hclk;
        end
      end
      else
      begin
        start_indrd_hclk  <= 1'b0;
        start_indrd_hold  <= 1'b0;
        indrd_xfer_in_prog_hclk <= indrd_xfer_in_prog_hclk;
      end
    end
  end
end

// Other ind Registers
assign indrd_wmark = indrd_xfer_wmark_reg;
assign indrd_start_add = indrd_xfer_start_add_reg;
assign indrd_num_bytes = indrd_xfer_num_bytes_reg;
assign indwr_wmark = indwr_xfer_wmark_reg;
assign indwr_start_add = indwr_xfer_start_add_reg;
assign indwr_num_bytes = indwr_xfer_num_bytes_reg;
assign ind_ahb_trig_add = ind_ahb_trig_add_reg;
assign ind_ahb_trig_add_range = ind_ahb_trig_add_range_reg;

assign cancel_indwr_hclk = cancel_indwr_sync ^ cancel_indwr_d1;
always @(posedge hclk or negedge n_hreset)
begin
  if (!n_hreset)
  begin
    start_indwr_reg   <= 1'b0;
    start_indwr_hold       <= 1'b0;
    indwr_xfer_in_prog_hclk <= 1'b0;
  end
  else
  begin
    if ((start_indwr_sync ^ start_indwr_d1) && !start_indwr_hold)
    begin
      indwr_xfer_in_prog_hclk <= 1'b1;
      if (indwr_xfer_in_prog_hclk)
      begin
        if (indwr_xfer_ahb_done || indwr_flush_capt)
        begin
          start_indwr_reg   <= 1'b1;
          start_indwr_hold  <= 1'b0;
        end
        else
        begin
          start_indwr_reg   <= 1'b0;
          start_indwr_hold  <= 1'b1;
        end
      end
      else
      begin
        start_indwr_reg   <= 1'b1;
        start_indwr_hold  <= 1'b0;
      end
    end
    else
    begin
      if (indwr_flush_capt)
      begin
        start_indwr_reg   <= 1'b0;
        start_indwr_hold  <= 1'b0;
        indwr_xfer_in_prog_hclk <= 1'b0;
      end
      else if (indwr_xfer_in_prog_hclk)
      begin
        if (indwr_xfer_ahb_done)
        begin
          start_indwr_reg   <= 1'b0;
          start_indwr_hold  <= 1'b0;
          indwr_xfer_in_prog_hclk <= start_indwr_hold;
        end
        else
        begin
          start_indwr_reg   <= 1'b0;
          start_indwr_hold  <= start_indwr_hold;
          indwr_xfer_in_prog_hclk <= indwr_xfer_in_prog_hclk;
        end
      end
      else
      begin
        start_indwr_reg   <= 1'b0;
        start_indwr_hold  <= 1'b0;
        indwr_xfer_in_prog_hclk <= indwr_xfer_in_prog_hclk;
      end
    end
  end
end
assign start_indwr_hclk = start_indwr_reg | (indwr_xfer_ahb_done & start_indwr_hold);


// DMA Peripheral Interface Register
wire  [3:0] bytes_in_burst_type, bytes_in_single_type;
reg   [15:0] bytes_in_burst_type_map, bytes_in_single_type_map;

assign bytes_in_burst_type  = dma_periph_config_reg[7:4];
assign bytes_in_single_type = dma_periph_config_reg[3:0];

always @* begin
  case(bytes_in_burst_type)
    4'b0000:
      bytes_in_burst_type_map = 16'h0001;
    4'b0001:
      bytes_in_burst_type_map = 16'h0002;
    4'b0010:
      bytes_in_burst_type_map = 16'h0004;
    4'b0011:
      bytes_in_burst_type_map = 16'h0008;
    4'b0100:
      bytes_in_burst_type_map = 16'h0010;
    4'b0101:
      bytes_in_burst_type_map = 16'h0020;
    4'b0110:
      bytes_in_burst_type_map = 16'h0040;
    4'b0111:
      bytes_in_burst_type_map = 16'h0080;
    4'b1000:
      bytes_in_burst_type_map = 16'h0100;
    4'b1001:
      bytes_in_burst_type_map = 16'h0200;
    4'b1010:
      bytes_in_burst_type_map = 16'h0400;
    4'b1011:
      bytes_in_burst_type_map = 16'h0800;
    4'b1100:
      bytes_in_burst_type_map = 16'h1000;
    4'b1101:
      bytes_in_burst_type_map = 16'h2000;
    4'b1110:
      bytes_in_burst_type_map = 16'h4000;
    default:
      bytes_in_burst_type_map = 16'h8000;
  endcase // bytes_in_burst_type
end

always @* begin
  case(bytes_in_single_type)
    4'b0000:
      bytes_in_single_type_map = 16'h0001;
    4'b0001:
      bytes_in_single_type_map = 16'h0002;
    4'b0010:
      bytes_in_single_type_map = 16'h0004;
    4'b0011:
      bytes_in_single_type_map = 16'h0008;
    4'b0100:
      bytes_in_single_type_map = 16'h0010;
    4'b0101:
      bytes_in_single_type_map = 16'h0020;
    4'b0110:
      bytes_in_single_type_map = 16'h0040;
    4'b0111:
      bytes_in_single_type_map = 16'h0080;
    4'b1000:
      bytes_in_single_type_map = 16'h0100;
    4'b1001:
      bytes_in_single_type_map = 16'h0200;
    4'b1010:
      bytes_in_single_type_map = 16'h0400;
    4'b1011:
      bytes_in_single_type_map = 16'h0800;
    4'b1100:
      bytes_in_single_type_map = 16'h1000;
    4'b1101:
      bytes_in_single_type_map = 16'h2000;
    4'b1110:
      bytes_in_single_type_map = 16'h4000;
    default:
      bytes_in_single_type_map = 16'h8000;
  endcase // bytes_in_sing_type_map
end


// Remap Addr Register
assign ahb_remap_addr = remap_add_reg;

// Write Protection Registers
assign lower_protection_addr = write_protect_lower_reg;
assign upper_protection_addr = write_protect_upper_reg;
assign ahb_wr_protection_inv = write_protect_ctrl_reg[0];
assign ahb_wr_protection_en_hclk = ahb_wr_protection_en_sync;


endmodule

