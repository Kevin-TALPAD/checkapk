@echo off
cls
echo 1.�廪Դ
echo 2.����Դ
echo 3.�ٷ�Դ
set /p choice="��ѡ��Դ��(��1��"
if %choice%="1" (
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple androguard
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
��
if %choice%="2" (
   pip install -i https://mirrors.aliyun.com/pypi/simple androguard
   pip install -i https://mirrors.aliyun.com/pypi/simple requests
)
if %choice%="3" (
   pip install androguard
   pip install requests
)