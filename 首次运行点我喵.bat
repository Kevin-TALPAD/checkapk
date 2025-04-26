@echo off
cls
echo 1.清华源
echo 2.阿里源
echo 3.官方源
set /p choice="请选择源：(如1）"
if %choice%="1" (
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple androguard
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
）
if %choice%="2" (
   pip install -i https://mirrors.aliyun.com/pypi/simple androguard
   pip install -i https://mirrors.aliyun.com/pypi/simple requests
)
if %choice%="3" (
   pip install androguard
   pip install requests
)