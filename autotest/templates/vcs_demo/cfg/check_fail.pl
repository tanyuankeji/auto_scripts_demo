#!/usr/bin/perl -w

###############################################################
## 检查失败脚本
## 描述: 用于检查仿真日志中的错误
###############################################################

# 定义错误关键字
@error_words = ("Error:", "ERROR", "Error", "error:", "Assertion failure", "failed", "Failed", "FAILED", "assertion", "Assertion");

# 获取要检查的文件名
my $file_name = $ARGV[0] || "vcs.log";

# 如果文件不存在，退出
if (!-e $file_name) {
    print "文件不存在: $file_name\n";
    exit(1);
}

# 打开文件进行读取
open(my $fh, '<', $file_name) or die "无法打开文件 '$file_name' : $!";

# 读取整个文件内容
my @lines = <$fh>;
close($fh);

# 检查是否包含错误关键字
my $error_count = 0;
my @error_lines;

foreach my $line (@lines) {
    foreach my $word (@error_words) {
        if ($line =~ /$word/) {
            $error_count++;
            push(@error_lines, $line);
            last;  # 一行只计数一次错误
        }
    }
}

# 输出检查结果
if ($error_count > 0) {
    print "发现 $error_count 个错误:\n";
    print join("", @error_lines);
    exit(1);
} else {
    print "未发现错误\n";
    exit(0);
} 