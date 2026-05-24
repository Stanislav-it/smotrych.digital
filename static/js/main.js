(function () {
    function onReady(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    onReady(function () {
        const header = document.querySelector('[data-header]');
        const menuButton = document.querySelector('[data-menu-button]');
        const mobilePanel = document.querySelector('[data-mobile-panel]');
        const mobileLinks = mobilePanel ? mobilePanel.querySelectorAll('a') : [];
        const menuCloseButton = document.querySelector('[data-menu-close]');
        const revealItems = document.querySelectorAll('.reveal');

        let lastScrollY = window.scrollY || 0;

        function updateHeader() {
            if (!header) return;
            const currentScrollY = window.scrollY || 0;
            const scrollingDown = currentScrollY > lastScrollY && currentScrollY > 90;
            const scrollingUp = currentScrollY < lastScrollY;

            header.classList.toggle('is-scrolled', currentScrollY > 12);

            if (document.body.classList.contains('menu-open') || currentScrollY <= 24) {
                header.classList.remove('is-hidden');
            } else if (scrollingDown) {
                header.classList.add('is-hidden');
            } else if (scrollingUp) {
                header.classList.remove('is-hidden');
            }

            lastScrollY = currentScrollY;
        }

        function setMenu(open) {
            if (!menuButton || !mobilePanel) return;
            document.body.classList.toggle('menu-open', open);
            if (open && header) header.classList.remove('is-hidden');
            mobilePanel.classList.toggle('is-open', open);
            menuButton.setAttribute('aria-expanded', String(open));
            menuButton.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
            mobilePanel.setAttribute('aria-hidden', String(!open));
        }

        function initReveal() {
            if (!revealItems.length) return;

            if (!('IntersectionObserver' in window)) {
                revealItems.forEach(function (item) {
                    item.classList.add('is-visible');
                });
                return;
            }

            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                root: null,
                threshold: 0.14,
                rootMargin: '0px 0px -8% 0px'
            });

            revealItems.forEach(function (item) {
                observer.observe(item);
            });
        }

        function initLogoRotator() {
            const rotators = document.querySelectorAll('[data-logo-rotator]');
            if (!rotators.length) return;
            const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

            function shuffle(list) {
                const cloned = list.slice();
                for (let i = cloned.length - 1; i > 0; i -= 1) {
                    const j = Math.floor(Math.random() * (i + 1));
                    const temp = cloned[i];
                    cloned[i] = cloned[j];
                    cloned[j] = temp;
                }
                return cloned;
            }

            rotators.forEach(function (rotator) {
                const items = Array.from(rotator.querySelectorAll('[data-logo-item]'));
                if (!items.length) return;

                const circleItems = items.filter(function (item) {
                    return item.getAttribute('data-has-circle') === 'true';
                });

                function applyMixedState(force) {
                    const shuffled = shuffle(circleItems);
                    const visibleCircles = Math.max(2, Math.min(circleItems.length - 1, 2 + Math.floor(Math.random() * 3)));
                    const keepCircles = new Set(shuffled.slice(0, visibleCircles));

                    items.forEach(function (item, index) {
                        const hasCircle = item.getAttribute('data-has-circle') === 'true';
                        const useCircle = hasCircle && keepCircles.has(item);
                        const nextState = useCircle ? 'circle' : 'text';
                        const currentState = item.classList.contains('is-circle') ? 'circle' : 'text';
                        const delay = force ? 0 : Math.floor(Math.random() * 260) + (index % 2) * 55;
                        item.style.setProperty('--logo-delay', delay + 'ms');
                        if (currentState !== nextState || force) {
                            item.classList.toggle('is-circle', nextState === 'circle');
                            item.classList.toggle('is-text', nextState === 'text');
                        }
                    });
                }

                applyMixedState(true);
                if (reducedMotion) return;

                window.setInterval(function () {
                    applyMixedState(false);
                }, 1450);
            });
        }





        function initMarketingTabs() {
            const sections = document.querySelectorAll('[data-marketing-tabs]');
            if (!sections.length) return;

            sections.forEach(function (section) {
                const buttons = Array.from(section.querySelectorAll('[data-marketing-tab]'));
                const panels = Array.from(section.querySelectorAll('[data-marketing-panel]'));
                if (!buttons.length || !panels.length) return;

                function activate(key) {
                    buttons.forEach(function (button) {
                        const isActive = button.getAttribute('data-marketing-tab') === key;
                        button.classList.toggle('is-active', isActive);
                        button.setAttribute('aria-selected', String(isActive));
                    });

                    panels.forEach(function (panel) {
                        const isActive = panel.getAttribute('data-marketing-panel') === key;
                        panel.classList.toggle('is-active', isActive);
                        panel.hidden = !isActive;
                    });
                }

                buttons.forEach(function (button) {
                    button.addEventListener('click', function () {
                        activate(button.getAttribute('data-marketing-tab'));
                    });
                });
            });
        }

        function initFaqServicesTabs() {
            const sections = document.querySelectorAll('[data-faq-services-tabs]');
            if (!sections.length) return;

            sections.forEach(function (section) {
                const buttons = Array.from(section.querySelectorAll('[data-faq-services-tab]'));
                const panels = Array.from(section.querySelectorAll('[data-faq-services-panel]'));
                if (!buttons.length || !panels.length) return;

                function activate(key) {
                    buttons.forEach(function (button) {
                        const isActive = button.getAttribute('data-faq-services-tab') === key;
                        button.classList.toggle('is-active', isActive);
                        button.setAttribute('aria-selected', String(isActive));
                    });

                    panels.forEach(function (panel) {
                        const isActive = panel.getAttribute('data-faq-services-panel') === key;
                        panel.classList.toggle('is-active', isActive);
                        panel.hidden = !isActive;
                    });
                }

                buttons.forEach(function (button) {
                    button.addEventListener('click', function () {
                        activate(button.getAttribute('data-faq-services-tab'));
                    });
                });
            });
        }

        function initShopAccordion() {
            const sections = document.querySelectorAll('[data-shop-accordion]');
            if (!sections.length) return;

            sections.forEach(function (section) {
                const items = Array.from(section.querySelectorAll('.shops-reference-accordion-item'));
                const triggers = Array.from(section.querySelectorAll('[data-shop-accordion-trigger]'));
                if (!items.length || !triggers.length) return;

                function setState(item, open) {
                    const trigger = item.querySelector('[data-shop-accordion-trigger]');
                    const panel = item.querySelector('[data-shop-accordion-panel]');
                    item.classList.toggle('is-open', open);
                    if (trigger) trigger.setAttribute('aria-expanded', String(open));
                    if (panel) panel.hidden = !open;
                }

                triggers.forEach(function (trigger) {
                    trigger.addEventListener('click', function () {
                        const item = trigger.closest('.shops-reference-accordion-item');
                        const willOpen = !item.classList.contains('is-open');
                        items.forEach(function (other) {
                            setState(other, false);
                        });
                        setState(item, willOpen);
                    });
                });
            });
        }

        function initShopPills() {
            const sections = document.querySelectorAll('[data-shop-pills]');
            if (!sections.length) return;

            sections.forEach(function (section) {
                const buttons = Array.from(section.querySelectorAll('[data-shop-pill]'));
                const panels = Array.from(section.querySelectorAll('[data-shop-panel]'));
                if (!buttons.length || !panels.length) return;

                function activate(key) {
                    buttons.forEach(function (button) {
                        const isActive = button.getAttribute('data-shop-pill') === key;
                        button.classList.toggle('is-active', isActive);
                        button.setAttribute('aria-selected', String(isActive));
                    });

                    panels.forEach(function (panel) {
                        const isActive = panel.getAttribute('data-shop-panel') === key;
                        panel.classList.toggle('is-active', isActive);
                        panel.hidden = !isActive;
                    });
                }

                buttons.forEach(function (button) {
                    button.addEventListener('click', function () {
                        activate(button.getAttribute('data-shop-pill'));
                    });
                });
            });
        }

        function initCountup() {
            const groups = document.querySelectorAll('[data-countup-group]');
            if (!groups.length) return;

            const counters = Array.from(document.querySelectorAll('.stats-counter'));

            function formatCounterValue(value, decimals) {
                return decimals > 0 ? value.toFixed(decimals) : Math.round(value).toString();
            }

            counters.forEach(function (counter) {
                const suffix = counter.getAttribute('data-suffix') || '';
                const decimals = Number(counter.getAttribute('data-decimals') || 0);
                const hasStart = counter.hasAttribute('data-start');
                const startValue = hasStart ? Number(counter.getAttribute('data-start') || 0) : 0;
                counter.textContent = formatCounterValue(startValue, decimals) + suffix;
            });

            function animateCounter(counter) {
                if (counter.dataset.animated === 'true') return;
                counter.dataset.animated = 'true';

                const target = Number(counter.getAttribute('data-target') || 0);
                const suffix = counter.getAttribute('data-suffix') || '';
                const decimals = Number(counter.getAttribute('data-decimals') || 0);
                const hasStart = counter.hasAttribute('data-start');
                const startValue = hasStart ? Number(counter.getAttribute('data-start') || 0) : 0;
                const delta = target - startValue;
                const duration = 950;
                const start = performance.now();

                function tick(now) {
                    const progress = Math.min((now - start) / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    const current = startValue + delta * eased;
                    counter.textContent = formatCounterValue(current, decimals) + suffix;
                    if (progress < 1) {
                        requestAnimationFrame(tick);
                    } else {
                        counter.textContent = formatCounterValue(target, decimals) + suffix;
                    }
                }

                requestAnimationFrame(tick);
            }

            if (!('IntersectionObserver' in window)) {
                counters.forEach(animateCounter);
                return;
            }

            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    entry.target.querySelectorAll('.stats-counter').forEach(animateCounter);
                    observer.unobserve(entry.target);
                });
            }, {
                threshold: 0.3,
                rootMargin: '0px 0px -10% 0px'
            });

            groups.forEach(function (group) {
                observer.observe(group);
            });
        }

        updateHeader();
        initReveal();
        initCountup();
        initLogoRotator();
        initShopPills();
        initShopAccordion();
        initFaqServicesTabs();
        initMarketingTabs();
        window.addEventListener('scroll', updateHeader, { passive: true });

        if (menuButton && mobilePanel) {
            menuButton.addEventListener('click', function (event) {
                event.preventDefault();
                const isOpen = document.body.classList.contains('menu-open');
                setMenu(!isOpen);
            });

            mobileLinks.forEach(function (link) {
                link.addEventListener('click', function () {
                    setMenu(false);
                });
            });

            if (menuCloseButton) {
                menuCloseButton.addEventListener('click', function () {
                    setMenu(false);
                });
            }

            mobilePanel.addEventListener('click', function (event) {
                if (event.target === mobilePanel) setMenu(false);
            });

            document.addEventListener('keydown', function (event) {
                if (event.key === 'Escape') setMenu(false);
            });
        }
    });
}());

// Services submenu v20260523_services_submenu_02
(function () {
    const panel = document.querySelector('[data-mobile-panel]');
    if (!panel) return;

    const card = panel.querySelector('.mobile-panel-card');
    const openers = panel.querySelectorAll('[data-submenu-open]');
    const submenus = panel.querySelectorAll('[data-submenu]');
    const backButtons = panel.querySelectorAll('[data-submenu-back]');

    function openSubmenu(name) {
        if (!card) return;
        card.classList.add('submenu-open');
        submenus.forEach(function (submenu) {
            const active = submenu.getAttribute('data-submenu') === name;
            submenu.classList.toggle('is-open', active);
            submenu.setAttribute('aria-hidden', active ? 'false' : 'true');
        });
    }

    function closeSubmenus() {
        if (card) card.classList.remove('submenu-open');
        submenus.forEach(function (submenu) {
            submenu.classList.remove('is-open');
            submenu.setAttribute('aria-hidden', 'true');
        });
    }

    openers.forEach(function (opener) {
        opener.addEventListener('click', function (event) {
            event.preventDefault();
            openSubmenu(opener.getAttribute('data-submenu-open'));
        });
    });

    backButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            closeSubmenus();
        });
    });

    panel.querySelectorAll('[data-menu-close]').forEach(function (button) {
        button.addEventListener('click', closeSubmenus);
    });

    panel.querySelectorAll('.mobile-submenu-list a').forEach(function (link) {
        link.addEventListener('click', closeSubmenus);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') closeSubmenus();
    });

    const observer = new MutationObserver(function () {
        if (!document.body.classList.contains('menu-open')) closeSubmenus();
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
})();


// Testimonials slider v20260523_reviews_01
(function () {
    function initTestimonials() {
        const blocks = document.querySelectorAll('[data-testimonials]');
        if (!blocks.length) return;
        const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        blocks.forEach(function (block) {
            const slides = Array.from(block.querySelectorAll('[data-testimonial-slide]'));
            const companyOutput = block.querySelector('[data-testimonial-company]');
            const countOutput = block.querySelector('[data-testimonial-count]');
            const prevButton = block.querySelector('[data-testimonial-prev]');
            const nextButton = block.querySelector('[data-testimonial-next]');
            if (!slides.length || !companyOutput || !countOutput) return;

            let current = 0;
            let initialized = false;
            let typingTimer = null;

            function typeCompany(name) {
                if (!companyOutput) return;
                window.clearTimeout(typingTimer);
                if (reducedMotion) {
                    companyOutput.textContent = name;
                    return;
                }
                companyOutput.textContent = '';
                let index = 0;
                (function step() {
                    companyOutput.textContent = name.slice(0, index + 1);
                    index += 1;
                    if (index < name.length) {
                        typingTimer = window.setTimeout(step, 48);
                    }
                }());
            }

            function render(index) {
                current = (index + slides.length) % slides.length;
                slides.forEach(function (slide, slideIndex) {
                    slide.classList.toggle('is-active', slideIndex === current);
                    slide.setAttribute('aria-hidden', slideIndex === current ? 'false' : 'true');
                });
                countOutput.textContent = (current + 1) + ' / ' + slides.length;
                const company = slides[current].getAttribute('data-company') || '';
                typeCompany(company);
            }

            function start() {
                if (initialized) return;
                initialized = true;
                render(0);
            }

            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            start();
                            observer.disconnect();
                        }
                    });
                }, { threshold: 0.32 });
                observer.observe(block);
            } else {
                start();
            }

            if (prevButton) {
                prevButton.addEventListener('click', function () {
                    if (!initialized) start();
                    render(current - 1);
                });
            }

            if (nextButton) {
                nextButton.addEventListener('click', function () {
                    if (!initialized) start();
                    render(current + 1);
                });
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTestimonials);
    } else {
        initTestimonials();
    }
}());


// SEO tabs and pill navigation v20260523_seo_tabs_01
(function () {
    function initSeoTabs() {
        document.querySelectorAll('[data-seo-tabs]').forEach(function (root) {
            const mainTabs = Array.from(root.querySelectorAll('[data-seo-tab]'));
            const panels = Array.from(root.querySelectorAll('[data-seo-panel]'));

            function activatePanel(name) {
                mainTabs.forEach(function (tab) {
                    const active = tab.getAttribute('data-seo-tab') === name;
                    tab.classList.toggle('is-active', active);
                    tab.setAttribute('aria-selected', active ? 'true' : 'false');
                    if (active && tab.scrollIntoView) {
                        tab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                    }
                });

                panels.forEach(function (panel) {
                    const active = panel.getAttribute('data-seo-panel') === name;
                    panel.classList.toggle('is-active', active);
                    panel.setAttribute('aria-hidden', active ? 'false' : 'true');
                    if (active) {
                        const firstPill = panel.querySelector('[data-seo-item]');
                        if (firstPill) activateItem(panel, firstPill.getAttribute('data-seo-item'));
                    }
                });
            }

            function activateItem(panel, item) {
                panel.querySelectorAll('[data-seo-item]').forEach(function (pill) {
                    const active = pill.getAttribute('data-seo-item') === item;
                    pill.classList.toggle('is-active', active);
                    pill.setAttribute('aria-pressed', active ? 'true' : 'false');
                    if (active && pill.scrollIntoView) {
                        pill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                    }
                });

                panel.querySelectorAll('[data-seo-copy]').forEach(function (copy) {
                    const active = copy.getAttribute('data-seo-copy') === item;
                    copy.classList.toggle('is-active', active);
                    copy.setAttribute('aria-hidden', active ? 'false' : 'true');
                });
            }

            mainTabs.forEach(function (tab) {
                tab.addEventListener('click', function () {
                    activatePanel(tab.getAttribute('data-seo-tab'));
                });
            });

            panels.forEach(function (panel) {
                panel.querySelectorAll('[data-seo-item]').forEach(function (pill) {
                    pill.addEventListener('click', function () {
                        activateItem(panel, pill.getAttribute('data-seo-item'));
                    });
                });
            });

            const initial = root.querySelector('[data-seo-tab].is-active');
            activatePanel(initial ? initial.getAttribute('data-seo-tab') : 'strony');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSeoTabs);
    } else {
        initSeoTabs();
    }
}());

// About accordion v20260524_about_01
(function () {
    function initAboutAccordion() {
        document.querySelectorAll('[data-about-accordion]').forEach(function (root) {
            const items = Array.from(root.querySelectorAll('.about-capability'));
            items.forEach(function (item) {
                const button = item.querySelector('.about-capability-toggle');
                const symbol = item.querySelector('.about-capability-symbol');
                if (!button) return;
                button.addEventListener('click', function () {
                    items.forEach(function (other) {
                        const isCurrent = other === item;
                        other.classList.toggle('is-open', isCurrent);
                        const otherButton = other.querySelector('.about-capability-toggle');
                        const otherSymbol = other.querySelector('.about-capability-symbol');
                        if (otherButton) otherButton.setAttribute('aria-expanded', isCurrent ? 'true' : 'false');
                        if (otherSymbol) otherSymbol.textContent = isCurrent ? '−' : '+';
                    });
                    if (symbol) symbol.textContent = '−';
                });
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAboutAccordion);
    } else {
        initAboutAccordion();
    }
}());

// Force every internal page navigation to start from the top v20260525_scroll_top_01
(function () {
    try {
        if ('scrollRestoration' in window.history) {
            window.history.scrollRestoration = 'manual';
        }
    } catch (error) {}

    function shouldForceTop() {
        return !window.location.hash;
    }

    function forceTop() {
        if (!shouldForceTop()) return;
        var root = document.documentElement;
        var body = document.body;
        var oldRootBehavior = root ? root.style.scrollBehavior : '';
        var oldBodyBehavior = body ? body.style.scrollBehavior : '';
        if (root) root.style.scrollBehavior = 'auto';
        if (body) body.style.scrollBehavior = 'auto';
        window.scrollTo(0, 0);
        if (root) root.scrollTop = 0;
        if (body) body.scrollTop = 0;
        window.setTimeout(function () {
            if (root) root.style.scrollBehavior = oldRootBehavior;
            if (body) body.style.scrollBehavior = oldBodyBehavior;
        }, 120);
    }

    document.addEventListener('click', function (event) {
        var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
        if (!link) return;
        var target = link.getAttribute('target');
        if (target && target !== '_self') return;
        var href = link.getAttribute('href') || '';
        if (!href || href.charAt(0) === '#') return;
        try {
            var nextUrl = new URL(link.href, window.location.href);
            if (nextUrl.origin === window.location.origin && !nextUrl.hash) {
                try { sessionStorage.setItem('smotrychForceTop', '1'); } catch (error) {}
            }
        } catch (error) {}
    }, true);

    if (shouldForceTop()) {
        forceTop();
        window.setTimeout(forceTop, 0);
        window.setTimeout(forceTop, 80);
        window.setTimeout(forceTop, 250);
        window.setTimeout(forceTop, 700);
    }

    window.addEventListener('pageshow', function () {
        if (!shouldForceTop()) return;
        forceTop();
        window.setTimeout(forceTop, 0);
        window.setTimeout(forceTop, 80);
        window.setTimeout(forceTop, 250);
        window.setTimeout(forceTop, 700);
    });
}());
