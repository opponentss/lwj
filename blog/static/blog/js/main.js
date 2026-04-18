// 博客网站主 JavaScript 文件

document.addEventListener('DOMContentLoaded', function() {
    // 初始化功能
    initCurrentDate();
    initCalendar();
    initRandomArticles();
    initMobileMenu();
    initRefreshButton();
});

// 1. 显示当前日期
function initCurrentDate() {
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const now = new Date();
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            weekday: 'long'
        };
        dateElement.textContent = now.toLocaleDateString('zh-CN', options);
    }
}

// 2. 日历组件
function initCalendar() {
    const calendarElement = document.getElementById('calendar');
    if (!calendarElement) return;

    // 获取当前日期
    const now = new Date();
    let currentYear = now.getFullYear();
    let currentMonth = now.getMonth(); // 0-11

    // 渲染日历
    function renderCalendar(year, month) {
        // 获取该月第一天和最后一天
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDay = firstDay.getDay(); // 0-6, 0=周日

        // 获取有文章的日期（从后端API）
        fetch(`/api/calendar-data/?year=${year}&month=${month + 1}`)
            .then(response => response.json())
            .then(data => {
                const articleDates = data.dates || [];

                // 生成日历HTML
                let calendarHTML = `
                    <div class="calendar-header">
                        <button class="calendar-nav prev-month" data-action="prev"><</button>
                        <div class="calendar-title">${year}年${month + 1}月</div>
                        <button class="calendar-nav next-month" data-action="next">></button>
                    </div>
                    <div class="calendar-grid">
                        <div class="calendar-day-header">日</div>
                        <div class="calendar-day-header">一</div>
                        <div class="calendar-day-header">二</div>
                        <div class="calendar-day-header">三</div>
                        <div class="calendar-day-header">四</div>
                        <div class="calendar-day-header">五</div>
                        <div class="calendar-day-header">六</div>
                `;

                // 空白单元格（上个月的日期）
                for (let i = 0; i < startingDay; i++) {
                    calendarHTML += `<div class="calendar-day empty"></div>`;
                }

                // 当前月的日期
                const today = new Date();
                const isToday = (day) => 
                    today.getFullYear() === year && 
                    today.getMonth() === month && 
                    today.getDate() === day;

                for (let day = 1; day <= daysInMonth; day++) {
                    const hasArticle = articleDates.includes(day);
                    const todayClass = isToday(day) ? 'today' : '';
                    const articleClass = hasArticle ? 'has-article' : '';
                    
                    calendarHTML += `
                        <div class="calendar-day ${todayClass} ${articleClass}" data-day="${day}">
                            ${day}
                            ${hasArticle ? '<span class="article-indicator"></span>' : ''}
                        </div>
                    `;
                }

                // 补齐剩余空白单元格（下个月的日期）
                const totalCells = 42; // 6行 * 7列
                const remainingCells = totalCells - (startingDay + daysInMonth);
                for (let i = 0; i < remainingCells; i++) {
                    calendarHTML += `<div class="calendar-day empty"></div>`;
                }

                calendarHTML += `</div>`;
                calendarElement.innerHTML = calendarHTML;

                // 添加事件监听器
                document.querySelectorAll('.calendar-nav').forEach(button => {
                    button.addEventListener('click', function() {
                        if (this.dataset.action === 'prev') {
                            month--;
                            if (month < 0) {
                                month = 11;
                                year--;
                            }
                        } else {
                            month++;
                            if (month > 11) {
                                month = 0;
                                year++;
                            }
                        }
                        renderCalendar(year, month);
                    });
                });

                // 日期点击事件
                document.querySelectorAll('.calendar-day:not(.empty)').forEach(dayElement => {
                    dayElement.addEventListener('click', function() {
                        const day = this.dataset.day;
                        // 跳转到该日期的文章列表（可扩展）
                        alert(`跳转到 ${year}年${month + 1}月${day}日的文章`);
                    });
                });
            })
            .catch(error => {
                console.error('加载日历数据失败:', error);
                calendarElement.innerHTML = '<div class="calendar-error">日历加载失败</div>';
            });
    }

    // 初始渲染
    renderCalendar(currentYear, currentMonth);
}

// 3. 随机推荐文章
function initRandomArticles() {
    const container = document.getElementById('random-articles');
    if (!container) return;

    function loadRandomArticles() {
        container.innerHTML = '<div class="loading">加载中...</div>';
        
        fetch('/api/random-articles/?count=2')
            .then(response => response.json())
            .then(data => {
                if (data.articles && data.articles.length > 0) {
                    let articlesHTML = '';
                    data.articles.forEach(article => {
                        articlesHTML += `
                            <div class="random-article">
                                <h4 class="random-article-title">
                                    <a href="/article/${article.slug}/">${article.title}</a>
                                </h4>
                                <p class="random-article-excerpt">${article.excerpt}</p>
                                <div class="random-article-meta">
                                    <span class="random-article-date">${article.published_at}</span>
                                    <span class="random-article-views">${article.views} 阅读</span>
                                </div>
                            </div>
                        `;
                    });
                    container.innerHTML = articlesHTML;
                } else {
                    container.innerHTML = '<div class="no-articles">暂无推荐文章</div>';
                }
            })
            .catch(error => {
                console.error('加载随机文章失败:', error);
                container.innerHTML = '<div class="error">加载失败，请重试</div>';
            });
    }

    // 初始加载
    loadRandomArticles();
}

// 4. 随机推荐刷新按钮
function initRefreshButton() {
    const refreshBtn = document.getElementById('refresh-random');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 加载中...';
            this.disabled = true;
            
            initRandomArticles();
            
            // 1秒后恢复按钮状态
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-redo"></i> 换一批';
                this.disabled = false;
            }, 1000);
        });
    }
}

// 5. 移动端菜单
function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.innerHTML = mobileMenu.classList.contains('active') 
                ? '<i class="fas fa-times"></i>' 
                : '<i class="fas fa-bars"></i>';
        });

        // 点击菜单外区域关闭菜单
        document.addEventListener('click', function(event) {
            if (!menuBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.remove('active');
                menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }
}

// 6. 文章点赞功能（在文章详情页使用）
function initArticleLikes() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const articleId = this.dataset.articleId;
            if (!articleId) return;
            
            const likeCountElement = document.getElementById('like-count');
            const currentLikes = parseInt(likeCountElement.textContent);
            
            // 发送点赞请求
            fetch(`/api/article/${articleId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    likeCountElement.textContent = data.likes;
                    this.innerHTML = `<i class="fas fa-heart"></i> 已点赞 (${data.likes})`;
                    this.classList.add('liked');
                }
            })
            .catch(error => {
                console.error('点赞失败:', error);
            });
        });
    });
}

// 辅助函数：获取 CSRF token
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 7. 页面滚动效果
function initScrollEffects() {
    // 导航栏阴影
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
            } else {
                navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            }
        });
    }

    // 回到顶部按钮（可扩展）
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: var(--accent);
        color: white;
        border: none;
        cursor: pointer;
        display: none;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 5px 15px rgba(53, 191, 171, 0.4);
        z-index: 999;
        transition: opacity 0.3s, transform 0.3s;
    `;
    
    document.body.appendChild(scrollToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollToTopBtn.style.display = 'flex';
            setTimeout(() => {
                scrollToTopBtn.style.opacity = '1';
                scrollToTopBtn.style.transform = 'translateY(0)';
            }, 10);
        } else {
            scrollToTopBtn.style.opacity = '0';
            scrollToTopBtn.style.transform = 'translateY(20px)';
            setTimeout(() => {
                if (window.scrollY <= 300) {
                    scrollToTopBtn.style.display = 'none';
                }
            }, 300);
        }
    });
    
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 初始化所有功能
initScrollEffects();