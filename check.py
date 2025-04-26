# 安装依赖： pip install androguard requests

import os
from androguard.misc import AnalyzeAPK

# 定义危险权限列表
dangerous_permissions = [
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.RECORD_AUDIO",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.READ_CONTACTS",
    "android.permission.CAMERA",
    "android.permission.INTERNET"
]

def check_permissions(a):
    app_permissions = a.get_permissions()
    issues = []
    for perm in app_permissions:
        if perm in dangerous_permissions:
            issues.append(f"[危险权限] {perm}")
    return issues

def check_signature(a):
    certs = a.get_certificates()
    if not certs:
        return ["[签名问题] 找不到签名证书"]
    return []

def check_obfuscation(dx):
    no_obfuscation_keywords = ['com.example', 'MainActivity', 'Test']
    for cls in dx.get_classes():
        class_name = cls.name
        if any(keyword in class_name for keyword in no_obfuscation_keywords):
            return ["[混淆警告] 代码可能未混淆"]
    return []

def check_sensitive_apis(dx):
    sensitive_apis = [
        'Landroid/telephony/SmsManager;->sendTextMessage',
        'Landroid/location/LocationManager;->getLastKnownLocation',
        'Landroid/media/MediaRecorder;->start',
        'Landroid/hardware/Camera;->open',
        'Ljava/net/HttpURLConnection;->connect'
    ]
    issues = []
    for method in dx.get_methods():
        for api in sensitive_apis:
            if api in method.get_method().get_descriptor():
                issues.append(f"[敏感API] {api} 被调用在 {method.name}")
    return issues

def check_http_traffic(a):
    urls = a.get_urls()
    issues = []
    for url in urls:
        if url.startswith('http://'):
            issues.append(f"[不安全传输] 发现HTTP明文连接: {url}")
    return issues

def check_packers(a):
    issues = []
    packers_keywords = ['360', 'Baidu', 'Tencent', '梆梆']
    for file in a.get_files():
        if any(keyword in file for keyword in packers_keywords):
            issues.append(f"[加壳检测] 可能存在加壳：{file}")
    return issues

def scan_apk(apk_path):
    print(f"\n正在扫描：{apk_path}")
    try:
        a, d, dx = AnalyzeAPK(apk_path)
        results = []

        results.extend(check_permissions(a))
        results.extend(check_signature(a))
        results.extend(check_obfuscation(dx))
        results.extend(check_sensitive_apis(dx))
        results.extend(check_http_traffic(a))
        results.extend(check_packers(a))

        if results:
            for issue in results:
                print(issue)
        else:
            print("未发现重大安全问题")
    except Exception as e:
        print(f"扫描失败：{e}")

def main():
    apk_files = [f for f in os.listdir('.') if f.lower().endswith('.apk')]
    
    if not apk_files:
        print("当前目录下没有找到APK文件。")
        return

    for apk in apk_files:
        scan_apk(apk)

if __name__ == "__main__":
    main()