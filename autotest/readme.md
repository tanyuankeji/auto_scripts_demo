# auto_testbench更新说明

## 2023/11/26

1.在生成的tb.f中，增加了+incdir+文件所在路径，以提供对`include "xxx_param.v"的支持

## 2023/10/25

1.增加了demo模式，在demo模式下可以不后缀任何参数来产生一个单纯的可编译环境：

```
{script_path}/auto_testbench
```

2.增加了自动比对环境的使用示例bypass_fifo_verification；
