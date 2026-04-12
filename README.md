# lvy-neko 个人博客/导航网站

基于 Django + HTML/CSS/JS 实现的个人博客/导航网站，风格参考 https://lvyovo-wiki.tech（简洁、卡片式、有日历、侧边栏、随机推荐、文章列表等）。

## 功能特性

### 核心功能
1. **文章模块**
   - 支持 Markdown 编辑和渲染（使用 django-markdownx）
   - 文章有标题、发布时间、阅读量、点赞数
   - 首页展示"最新文章"列表（标题 + 日期 + 简介）
   - 每篇文章独立详情页，下方显示"随机推荐文章"

2. **随机推荐区块**
   - 首页侧边栏显示"随机推荐"卡片
   - 每次刷新或点击"换一批"可随机获取 1~2 篇文章

3. **日历组件**
   - 显示当前月份日期，高亮有文章发表的日期
   - 前端用 JS 生成，后端提供文章日期数据接口

4. **社交链接**
   - 显示小红书、Bilibili、GitHub 图标链接（可在后台配置）

5. **"写文章"入口**
   - 前端有一个"写文章"按钮，仅管理员可见
   - 点击跳转到后台管理界面

6. **统计显示**
   - 侧边栏显示文章总数统计（默认显示"1711"）

7. **关于页面**
   - "关于网站"链接，展示网站介绍和个人信息

8. **开发中提示**
   - 对尚未完成的功能（如"我的项目"、"优秀博客"链接）显示"开发中"提示

### 技术特性
- 响应式设计，适配移动端
- 纯前端 JavaScript 实现日历和随机推荐
- 原生 CSS3 动画和过渡效果
- Django 管理后台集成 Markdown 编辑器

## 项目结构

```
blog_project/
├── blog/                          # 博客应用
│   ├── migrations/                # 数据库迁移文件
│   ├── static/blog/               # 静态文件
│   │   ├── css/style.css          # 主样式文件
│   │   └── js/main.js             # 主 JavaScript 文件
│   ├── templates/blog/            # 模板文件
│   │   ├── base.html              # 基础模板
│   │   ├── index.html             # 首页模板
│   │   ├── article_detail.html    # 文章详情页
│   │   └── about.html             # 关于页面
│   ├── __init__.py
│   ├── admin.py                   # 管理后台配置
│   ├── apps.py
│   ├── context_processors.py      # 上下文处理器
│   ├── models.py                  # 数据模型
│   ├── urls.py                    # URL 配置
│   └── views.py                   # 视图函数
├── blog_project/                  # Django 项目配置
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # 项目设置
│   ├── urls.py                    # 项目 URL 配置
│   └── wsgi.py
├── media/                         # 媒体文件目录（运行后生成）
├── staticfiles/                   # 静态文件收集目录（运行后生成）
├── initialize_data.py             # 数据初始化脚本
├── manage.py                      # Django 管理脚本
├── requirements.txt               # Python 依赖包
└── README.md                      # 项目说明
```

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8+ 和 pip。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户

```bash
python manage.py createsuperuser
```
或使用初始化脚本自动创建：
```bash
python manage.py shell < initialize_data.py
```

### 5. 运行开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 查看网站。

### 6. 后台管理

访问 http://127.0.0.1:8000/admin/ 进入管理后台。
- 用户名: admin (如果使用初始化脚本)
- 密码: admin123

## 详细配置

### 初始化数据

项目提供了完整的初始化脚本，可一键创建：
- 超级用户 (admin/admin123)
- 示例分类（技术教程、生活随笔等）
- 示例文章（3篇）
- 社交链接（GitHub、Bilibili、小红书）
- 网站统计

运行初始化脚本：
```bash
python initialize_data.py
```

### 静态文件收集

生产环境需要收集静态文件：
```bash
python manage.py collectstatic
```

### 媒体文件配置

上传的图片等媒体文件存储在 `media/` 目录。
开发环境下会自动创建此目录。

## 功能使用指南

### 1. 发布文章
1. 登录后台管理 (http://127.0.0.1:8000/admin/)
2. 点击"文章" -> "添加文章"
3. 使用 Markdown 编辑器编写内容
4. 设置分类、封面图等
5. 发布文章

### 2. 配置社交链接
1. 进入后台管理
2. 点击"社交链接"
3. 添加或修改平台链接
4. 设置显示顺序和图标

### 3. 网站统计
1. 进入后台管理
2. 点击"网站统计"
3. 可查看和修改统计值
4. 文章总数会自动更新

### 4. 前端功能
- **日历**：自动高亮有文章的日期，可点击查看
- **随机推荐**：点击"换一批"刷新推荐文章
- **移动端菜单**：小屏时点击右上角菜单按钮
- **回到顶部**：页面滚动时显示回到顶部按钮

## 技术栈

- **后端**: Django 4.2 + SQLite（开发）/ PostgreSQL（生产）
- **前端**: HTML5 + CSS3 + 原生 JavaScript
- **编辑器**: django-markdownx（Markdown 支持）
- **图标**: Font Awesome 6.4
- **字体**: Google Fonts (Inter)
- **部署**: 支持 Docker + Nginx + Gunicorn

## 部署建议

### 生产环境配置

1. **修改 settings.py**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'blog_db',
           'USER': 'blog_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **收集静态文件**:
   ```bash
   python manage.py collectstatic
   ```

3. **使用 Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn blog_project.wsgi:application
   ```

4. **配置 Nginx**:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/your/staticfiles/;
       }
       
       location /media/ {
           alias /path/to/your/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 自定义开发

### 修改样式
编辑 `blog/static/blog/css/style.css` 文件。

### 修改脚本
编辑 `blog/static/blog/js/main.js` 文件。

### 添加新功能
1. 在 `blog/models.py` 中添加模型
2. 在 `blog/views.py` 中添加视图
3. 在 `blog/urls.py` 中添加 URL 配置
4. 在 `blog/templates/` 中添加模板文件

### 扩展 API
现有 API 端点：
- `/api/random-articles/` - 获取随机文章
- `/api/calendar-data/` - 获取日历数据
- `/api/articles/` - 获取文章列表（分页）

## 常见问题

### 1. 静态文件无法加载
确保已运行 `python manage.py collectstatic`，并检查 `STATIC_URL` 和 `STATIC_ROOT` 配置。

### 2. 图片上传失败
检查 `MEDIA_ROOT` 目录权限，确保 Django 有写入权限。

### 3. 日历不显示
检查浏览器控制台是否有 JavaScript 错误，确保 `/api/calendar-data/` API 能正常访问。

### 4. Markdown 渲染问题
确保已安装 `django-markdownx` 并正确配置。

### 5. 移动端布局错乱
检查 CSS 媒体查询，确保响应式设计正确实现。

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub: https://github.com/lvy-neko
- Email: admin@example.com

---

**祝您使用愉快！**