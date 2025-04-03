// 简化版testbench - 由autotest工具自动生成
// 适用于模块: i3c_regs
// 完整版路径: i3c_regs_verification/top/testbench_i3c_regs.sv

`define DELAY(N, clk) begin \
	repeat(N) @(posedge clk);\
	#1ps;\
end

module testbench();

//-------------------------------------{{common cfg
timeunit 1ns;
timeprecision 1ps;
initial $timeformat(-9,3,"ns",6);

string tc_name;
int tc_seed;

initial begin
    if(!$value$plusargs("tc_name=%s", tc_name)) $error("no tc_name!");
    else $display("tc name = %0s", tc_name);
    if(!$value$plusargs("ntb_random_seed=%0d", tc_seed)) $error("no tc_seed");
    else $display("tc seed = %0d", tc_seed);
end
//-------------------------------------}}

//-------------------------------------{{{parameter declare
parameter ID_48B = 48'h0;
parameter ID_AS_REGS = 12'd0;
parameter ID_BCR = 8'd0;
parameter ID_DCR = 8'd0;
parameter SADDR_P = 0;
parameter ENA_MAPPED = 5'd0;
parameter MAP_CNT = 4'd1;
parameter MAP_I2CID = 24'd0;
parameter MAP_DA_DAA = 0;
parameter ENA_IBI_MR_HJ = 0;
parameter CLK_SLOW_BITS = 6;
parameter CLK_SLOW_MATCH = 6'd47;
parameter CLK_SLOW_HJMUL = 10'd1000;
parameter ERROR_HANDLING = 3'd0;
parameter ENA_CCC_HANDLING = 6'd0;
parameter RSTACT_CONFIG = 26'd0;
parameter MAX_RDLEN = 0;
parameter MAX_WRLEN = 0;
parameter MAX_DS_WR = 0;
parameter MAX_DS_RD = 0;
parameter MAX_DS_RDTURN = 0;
parameter SEL_BUS_IF = 0;
parameter FIFO_TYPE = 0;
parameter EXT_FIFO = 3'd0;
parameter ENA_TOBUS_FIFO = 0;
parameter ENA_FROMBUS_FIFO = 0;
parameter ENA_HDR = 0;
parameter ENA_TIMEC = 6'b000010;
parameter BLOCK_ID = 0;
parameter ENA_MASTER = 0;
parameter MPMX = 12'h11C;
//-------------------------------------}}}

//-------------------------------------{{{signal declare
logic  PRESETn;
logic  PCLK;
logic  PSEL;
logic  PENA;
logic [11:2] PADDR;
logic  PWRITE;
logic [31:0] PRDATA;
logic [31:0] PWDATA;
logic  PREADY;
logic  wr_err;
logic [1:0] ign_mwrite;
logic  cf_SlvEna;
logic  cf_SlvNack;
logic [7:0] cf_SlvSA;
logic [3:0] cf_IdInst;
logic  cf_IdRand;
logic  cf_Offline;
logic [31:0] cf_Partno;
logic [7:0] cf_IdBcr;
logic [7:0] cf_IdDcr;
logic [14:0] cf_IdVid;
logic  cf_DdrOK;
logic  cf_TspOK;
logic  cf_TslOK;
logic [11:0] cf_MaxRd;
logic [11:0] cf_MaxWr;
logic [23:0] cf_RstActTim;
logic [7:0] cf_BAMatch;
logic [15:0] cf_TCclk;
logic  cf_s0ignore;
logic  cf_matchss;
logic  cf_IbiExtData;
logic [3:0] cf_IbiMapIdx;
logic [2:0] cf_i2c_dev_rev;
logic [1:0] cf_HdrCmd;
logic [8:0] cf_vgpio;
logic [6:0] cf_CccMask;
logic [MAP_CNT-1:0] map_daa_use;
logic [7:0] SetDA;
logic [(MAP_CNT*10)-1:0] SetMappedDASA;
logic [2:0] SetSA10b;
logic  is_slave;
logic  master_comp;
logic [29:28] raw_ActState;
logic [27:24] raw_EvState;
logic [2:0] raw_TimeC;
logic [6:0] raw_Request;
logic [7:0] raw_DynAddr;
logic [2:0] raw_DynChgCause;
logic [12:0] raw_match_idx;
logic [19:8] reg_IntEna;
logic [5:0] reg_DmaCtrl;
logic [19:8] inp_IntStates;
logic [2:0] reg_EvPend;
logic [7:0] reg_EvIbiByte;
logic  inp_EvNoCancel;
logic [22:20] inp_EvDet;
logic [5:0] inp_GenErr;
logic [11:8] inp_DataErr;
logic [5:0] msk_GenErr;
logic [11:8] msk_DataErr;
logic  inp_err_loc;
logic [19:8] reg_clrIntStates;
logic [5:0] reg_clrGenErr;
logic [11:8] reg_clrDataErr;
logic  reg_holdOErr;
logic  inpflg_MaxRd;
logic  inpflg_MaxWr;
logic [11:0] inp_MaxRW;
logic  reg_TbEnd;
logic  reg_TbFlush;
logic  reg_FbFlush;
logic  inp_dma_last_tb;
logic [5:4] reg_TxTrig;
logic [7:6] reg_RxTrig;
logic [20:16] inp_TxCnt;
logic [28:24] inp_RxCnt;
logic  inp_TxFull;
logic  inp_RxEmpty;
logic [1:0] regflg_wr_cnt;
logic [7:0] reg_wdata;
logic [1:0] regflg_rd_cnt;
logic [7:0] inp_fb_data;
logic [8:7] reg_ActMode;
logic [3:0] reg_PendInt;
logic [15:8] reg_StatusRes;
logic  hdr_new_cmd;
logic [7:0] raw_hdr_cmd;
logic  map_rstdaa;
logic  map_setaasa;
logic  map_daa_ena;
logic [3:0] map_sa_idx;
logic [7:1] map_daa_da;
logic [10:0] ibi_wr_fifo;
logic  ibi_wr_ack;
logic  exp_owrite_err;
logic  exp_oread_err;
logic sys_clk;
logic sys_rstn;
//-------------------------------------}}}

//-------------------------------------{{clk/rst cfg
// 初始化时钟和复位信号
initial begin
    sys_clk = 1'b0;
    sys_rstn = 1'b0;
end

// 时钟生成
initial forever #5ns sys_clk = ~sys_clk;

// 复位控制
initial begin
    sys_rstn = 1'b0;
	`DELAY(30, sys_clk);
	sys_rstn = 1'b1;
end

// 测试超时控制
initial begin
    #100000ns $finish;
end
//-------------------------------------}}

//-------------------------------------{{{valid sig assign
//-------------------------------------}}}

//-------------------------------------{{{ready sig assign
//-------------------------------------}}}

//-------------------------------------{{{data sig assign
//-------------------------------------}}}

//-------------------------------------{{{other sig assign
initial begin
    PRESETn = $urandom;
    PCLK = $urandom;
    PSEL = $urandom;
    PENA = $urandom;
    PADDR = $urandom;
    PWRITE = $urandom;
    PWDATA = $urandom;
    ign_mwrite = $urandom;
    is_slave = $urandom;
    master_comp = $urandom;
    raw_ActState = $urandom;
    raw_EvState = $urandom;
    raw_TimeC = $urandom;
    raw_Request = $urandom;
    raw_DynAddr = $urandom;
    raw_DynChgCause = $urandom;
    raw_match_idx = $urandom;
    inp_IntStates = $urandom;
    inp_EvNoCancel = $urandom;
    inp_EvDet = $urandom;
    inp_GenErr = $urandom;
    inp_DataErr = $urandom;
    inp_err_loc = $urandom;
    inpflg_MaxRd = $urandom;
    inpflg_MaxWr = $urandom;
    inp_MaxRW = $urandom;
    inp_dma_last_tb = $urandom;
    inp_TxCnt = $urandom;
    inp_RxCnt = $urandom;
    inp_TxFull = $urandom;
    inp_RxEmpty = $urandom;
    inp_fb_data = $urandom;
    hdr_new_cmd = $urandom;
    raw_hdr_cmd = $urandom;
    map_rstdaa = $urandom;
    map_setaasa = $urandom;
    map_daa_ena = $urandom;
    map_sa_idx = $urandom;
    map_daa_da = $urandom;
    ibi_wr_ack = $urandom;
    `DELAY(50, sys_clk);
end
//-------------------------------------}}}

//-------------------------------------{{rtl inst
i3c_regs #(
    .ID_48B(ID_48B),
    .ID_AS_REGS(ID_AS_REGS),
    .ID_BCR(ID_BCR),
    .ID_DCR(ID_DCR),
    .SADDR_P(SADDR_P),
    .ENA_MAPPED(ENA_MAPPED),
    .MAP_CNT(MAP_CNT),
    .MAP_I2CID(MAP_I2CID),
    .MAP_DA_DAA(MAP_DA_DAA),
    .ENA_IBI_MR_HJ(ENA_IBI_MR_HJ),
    .CLK_SLOW_BITS(CLK_SLOW_BITS),
    .CLK_SLOW_MATCH(CLK_SLOW_MATCH),
    .CLK_SLOW_HJMUL(CLK_SLOW_HJMUL),
    .ERROR_HANDLING(ERROR_HANDLING),
    .ENA_CCC_HANDLING(ENA_CCC_HANDLING),
    .RSTACT_CONFIG(RSTACT_CONFIG),
    .MAX_RDLEN(MAX_RDLEN),
    .MAX_WRLEN(MAX_WRLEN),
    .MAX_DS_WR(MAX_DS_WR),
    .MAX_DS_RD(MAX_DS_RD),
    .MAX_DS_RDTURN(MAX_DS_RDTURN),
    .SEL_BUS_IF(SEL_BUS_IF),
    .FIFO_TYPE(FIFO_TYPE),
    .EXT_FIFO(EXT_FIFO),
    .ENA_TOBUS_FIFO(ENA_TOBUS_FIFO),
    .ENA_FROMBUS_FIFO(ENA_FROMBUS_FIFO),
    .ENA_HDR(ENA_HDR),
    .ENA_TIMEC(ENA_TIMEC),
    .BLOCK_ID(BLOCK_ID),
    .ENA_MASTER(ENA_MASTER),
    .MPMX(MPMX)
) 
u_i3c_regs(
    .PRESETn(PRESETn),
    .PCLK(PCLK),
    .PSEL(PSEL),
    .PENA(PENA),
    .PADDR(PADDR),
    .PWRITE(PWRITE),
    .PRDATA(PRDATA),
    .PWDATA(PWDATA),
    .PREADY(PREADY),
    .wr_err(wr_err),
    .ign_mwrite(ign_mwrite),
    .cf_SlvEna(cf_SlvEna),
    .cf_SlvNack(cf_SlvNack),
    .cf_SlvSA(cf_SlvSA),
    .cf_IdInst(cf_IdInst),
    .cf_IdRand(cf_IdRand),
    .cf_Offline(cf_Offline),
    .cf_Partno(cf_Partno),
    .cf_IdBcr(cf_IdBcr),
    .cf_IdDcr(cf_IdDcr),
    .cf_IdVid(cf_IdVid),
    .cf_DdrOK(cf_DdrOK),
    .cf_TspOK(cf_TspOK),
    .cf_TslOK(cf_TslOK),
    .cf_MaxRd(cf_MaxRd),
    .cf_MaxWr(cf_MaxWr),
    .cf_RstActTim(cf_RstActTim),
    .cf_BAMatch(cf_BAMatch),
    .cf_TCclk(cf_TCclk),
    .cf_s0ignore(cf_s0ignore),
    .cf_matchss(cf_matchss),
    .cf_IbiExtData(cf_IbiExtData),
    .cf_IbiMapIdx(cf_IbiMapIdx),
    .cf_i2c_dev_rev(cf_i2c_dev_rev),
    .cf_HdrCmd(cf_HdrCmd),
    .cf_vgpio(cf_vgpio),
    .cf_CccMask(cf_CccMask),
    .map_daa_use(map_daa_use),
    .SetDA(SetDA),
    .SetMappedDASA(SetMappedDASA),
    .SetSA10b(SetSA10b),
    .is_slave(is_slave),
    .master_comp(master_comp),
    .raw_ActState(raw_ActState),
    .raw_EvState(raw_EvState),
    .raw_TimeC(raw_TimeC),
    .raw_Request(raw_Request),
    .raw_DynAddr(raw_DynAddr),
    .raw_DynChgCause(raw_DynChgCause),
    .raw_match_idx(raw_match_idx),
    .reg_IntEna(reg_IntEna),
    .reg_DmaCtrl(reg_DmaCtrl),
    .inp_IntStates(inp_IntStates),
    .reg_EvPend(reg_EvPend),
    .reg_EvIbiByte(reg_EvIbiByte),
    .inp_EvNoCancel(inp_EvNoCancel),
    .inp_EvDet(inp_EvDet),
    .inp_GenErr(inp_GenErr),
    .inp_DataErr(inp_DataErr),
    .msk_GenErr(msk_GenErr),
    .msk_DataErr(msk_DataErr),
    .inp_err_loc(inp_err_loc),
    .reg_clrIntStates(reg_clrIntStates),
    .reg_clrGenErr(reg_clrGenErr),
    .reg_clrDataErr(reg_clrDataErr),
    .reg_holdOErr(reg_holdOErr),
    .inpflg_MaxRd(inpflg_MaxRd),
    .inpflg_MaxWr(inpflg_MaxWr),
    .inp_MaxRW(inp_MaxRW),
    .reg_TbEnd(reg_TbEnd),
    .reg_TbFlush(reg_TbFlush),
    .reg_FbFlush(reg_FbFlush),
    .inp_dma_last_tb(inp_dma_last_tb),
    .reg_TxTrig(reg_TxTrig),
    .reg_RxTrig(reg_RxTrig),
    .inp_TxCnt(inp_TxCnt),
    .inp_RxCnt(inp_RxCnt),
    .inp_TxFull(inp_TxFull),
    .inp_RxEmpty(inp_RxEmpty),
    .regflg_wr_cnt(regflg_wr_cnt),
    .reg_wdata(reg_wdata),
    .regflg_rd_cnt(regflg_rd_cnt),
    .inp_fb_data(inp_fb_data),
    .reg_ActMode(reg_ActMode),
    .reg_PendInt(reg_PendInt),
    .reg_StatusRes(reg_StatusRes),
    .hdr_new_cmd(hdr_new_cmd),
    .raw_hdr_cmd(raw_hdr_cmd),
    .map_rstdaa(map_rstdaa),
    .map_setaasa(map_setaasa),
    .map_daa_ena(map_daa_ena),
    .map_sa_idx(map_sa_idx),
    .map_daa_da(map_daa_da),
    .ibi_wr_fifo(ibi_wr_fifo),
    .ibi_wr_ack(ibi_wr_ack),
    .exp_owrite_err(exp_owrite_err),
    .exp_oread_err(exp_oread_err)
);
//-------------------------------------}}}

endmodule

