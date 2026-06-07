/* Main JavaScript for the static blog */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        // Open external links in new tab
        var links = document.querySelectorAll('a[href^="http"]');
        for (var i = 0; i < links.length; i++) {
            if (links[i].hostname !== window.location.hostname) {
                links[i].setAttribute("target", "_blank");
                links[i].setAttribute("rel", "noopener noreferrer");
            }
        }

        // Wrap tables in post content for mobile scroll
        var tables = document.querySelectorAll('.post-content table');
        for (var j = 0; j < tables.length; j++) {
            var table = tables[j];
            if (table.parentNode.classList.contains('table-wrap')) {
                continue;
            }
            var wrapper = document.createElement('div');
            wrapper.className = 'table-wrap';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }

        // Build left-side TOC for post pages
        var postContent = document.querySelector('.post-content');
        var mainContent = document.querySelector('.main-content');
        if (postContent && mainContent) {
            var headings = postContent.querySelectorAll('h2, h3');
            if (headings.length > 0) {
                for (var k = 0; k < headings.length; k++) {
                    headings[k].id = 'toc-' + k;
                }

                var tocItems = '';
                for (var h = 0; h < headings.length; h++) {
                    var tag = headings[h].tagName.toLowerCase();
                    var cls = tag === 'h2' ? 'toc-l1' : 'toc-l2';
                    tocItems += '<li class="' + cls + '"><a href="#toc-' + h + '">' + headings[h].textContent + '</a></li>';
                }

                var tocAside = document.createElement('aside');
                tocAside.className = 'post-toc';
                tocAside.innerHTML = '<div class="post-toc-title">段落导航</div><ul class="post-toc-list">' + tocItems + '</ul>';

                document.body.appendChild(tocAside);

                var post = document.querySelector('.post');

                function positionToc() {
                    var rect = mainContent.getBoundingClientRect();
                    var postRect = post.getBoundingClientRect();
                    var tocLeft = rect.left - 210;
                    tocAside.style.left = tocLeft + 'px';
                    tocAside.style.top = (postRect.top + 40) + 'px';
                    if (tocLeft >= 10) {
                        tocAside.classList.remove('toc-hide');
                    } else {
                        tocAside.classList.add('toc-hide');
                    }
                }

                positionToc();
                window.addEventListener('resize', positionToc);

                // Highlight active TOC item on scroll
                var tocLinks = tocAside.querySelectorAll('.post-toc-list a');

                function highlightToc() {
                    var scrollTop = window.scrollY;
                    var activeIndex = -1;
                    for (var m = headings.length - 1; m >= 0; m--) {
                        if (headings[m].offsetTop <= scrollTop + 100) {
                            activeIndex = m;
                            break;
                        }
                    }
                    for (var n = 0; n < tocLinks.length; n++) {
                        if (n === activeIndex) {
                            tocLinks[n].classList.add('active');
                        } else {
                            tocLinks[n].classList.remove('active');
                        }
                    }
                }

                highlightToc();
                window.addEventListener('scroll', highlightToc);
            }
        }
    });
})();
