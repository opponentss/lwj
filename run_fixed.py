#!/usr/bin/env python
import os
import sys

# 强制修复环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'

# 打印确认
print(f"Fixed DJANGO_SETTINGS_MODULE = {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# 运行 manage.py 命令
sys.argv = ['run_fixed.py'] + sys.argv[1:] if len(sys.argv) > 1 else ['run_fixed.py', 'runserver']

# 导入并执行
try:
    # 模拟 manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
except ImportError as exc:
    print(f"Import error: {exc}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)