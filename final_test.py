import sys
import os
import time
import subprocess
import urllib.request
import urllib.error

# 启动开发服务器
server = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '8090', '--noreload'],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)

try:
    # 测试静态文件
    static_url = 'http://localhost:8090/static/blog/css/style.css'
    req = urllib.request.Request(static_url)
    response = urllib.request.urlopen(req)
    print('静态文件状态:', response.status)
    # 测试页面
    page_url = 'http://localhost:8090/'
    req2 = urllib.request.Request(page_url)
    response2 = urllib.request.urlopen(req2)
    html = response2.read().decode('utf-8')
    # 检查CSS链接
    if 'http://localhost/static/blog/css/style.css' in html:
        print('页面中包含正确的CSS链接')
    else:
        # 查找所有CSS链接
        import re
        links = re.findall(r'<link[^>]*href="([^"]*)"', html)
        print('找到的CSS链接:', links)
        # 检查是否有相对链接
        for link in links:
            if 'style.css' in link:
                print('样式表链接:', link)
except urllib.error.URLError as e:
    print('错误:', e)
except Exception as e:
    print('其他错误:', e)
finally:
    server.terminate()
    server.wait()
    print('服务器已停止')