// ملف JavaScript الرئيسي لمنصة تروفي
// تاريخ الإنشاء: 21 أبريل 2025

  /* Go Top
  -------------------------------------------------------------------------------------*/


// التأكد من تحميل المستند بالكامل قبل تنفيذ أي كود
document.addEventListener('DOMContentLoaded', function() {
    // إضافة سلوك القائمة المتجاوبة للشاشات الصغيرة
    const menuToggle = document.createElement('button');
    menuToggle.classList.add('menu-toggle');
    menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    const navMenu = document.querySelector('.nav-menu');
    const headerContainer = document.querySelector('.header-container');
    
    // إضافة زر القائمة فقط في الشاشات الصغيرة
    function handleResponsiveMenu() {
        if (window.innerWidth <= 992 && !document.querySelector('.menu-toggle')) {
            headerContainer.insertBefore(menuToggle, navMenu);
            navMenu.classList.add('nav-menu-hidden');
            
            menuToggle.addEventListener('click', function() {
                navMenu.classList.toggle('nav-menu-active');
                menuToggle.classList.toggle('active');
            });
        } else if (window.innerWidth > 992) {
            if (document.querySelector('.menu-toggle')) {
                document.querySelector('.menu-toggle').remove();
            }
            navMenu.classList.remove('nav-menu-hidden', 'nav-menu-active');
        }
    }
    
    // تنفيذ الدالة عند تحميل الصفحة وعند تغيير حجم النافذة
    handleResponsiveMenu();
    window.addEventListener('resize', handleResponsiveMenu);
    
    // إضافة تأثيرات التمرير السلس للروابط الداخلية
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // تأثير تثبيت الشريط العلوي عند التمرير
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
        
        lastScrollTop = scrollTop;
    });
});
