###############################################################
## 配置文件
## 描述: 用于设置VCS仿真环境
###############################################################

# VCS编译选项
VCS_OPTS = -full64 -debug_all -sverilog -timescale=1ns/1ps -q +lint=TFIPC-L +lint=PCWM +lint=BADPAS +lint=STAVAR +lint=UCSPI
VCS_OPTS += +vcs+loopreport +vcs+loopdetect 
VCS_OPTS += -notice 
VCS_OPTS += +nospecify +notimingcheck
VCS_OPTS += -P $(UVM_HOME)/src/uvm_vcs.tab $(UVM_HOME)/src/dpi/libuvm_dpi.so
VCS_OPTS += +incdir+$(UVM_HOME)/src $(UVM_HOME)/src/uvm.sv $(UVM_HOME)/src/dpi/uvm_dpi.cc
VCS_OPTS += -f ../cfg/tb.f 

# 仿真选项
SIM_OPTS = +vcs+finish+1 +ntb_random_seed_automatic +warn_duplicated_case_patternmatch
SIM_OPTS += +vcs+lic+wait
SIM_OPTS += -gui=verdi

# TC名称
TC_NAME ?= default_test

# 编译规则
compile:
	vcs $(VCS_OPTS) -o simv

# 仿真规则
sim: compile
	./simv $(SIM_OPTS) +tc_name=$(TC_NAME)

# 清理规则
clean:
	rm -rf simv* csrc *.vpd *.log *.key *.pdb *profile* DVEfiles *~
	rm -rf vc_hdrs.h *.vdb .vlogansetup.args
	rm -rf .vcs_lib .vcs_lib_*
	rm -rf verdiLog novas.*
	rm -rf inter.vpd *.daidir

# 帮助规则
help:
	@echo "使用方法:"
	@echo "  make compile       - 仅编译"
	@echo "  make sim           - 编译并运行默认测试"
	@echo "  make TC_NAME=<名称> - 编译并运行指定测试"
	@echo "  make clean         - 清理生成的文件"

.PHONY: compile sim clean help 