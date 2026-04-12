#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    #DJANGO_SETTINGS_MODULE用于指定当前 Django 项目应该加载哪个设置模块（通常是 settings.py 文件）
    os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'  # 这行修改系统环境变量
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
