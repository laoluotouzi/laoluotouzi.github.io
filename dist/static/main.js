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

        // Build TOC for post pages
        var postContent = document.querySelector('.post-content');
        if (postContent) {
            var headings = postContent.querySelectorAll('h2, h3, h4');
            if (headings.length > 0) {
                for (var k = 0; k < headings.length; k++) {
                    headings[k].id = 'toc-' + k;
                }

                // Determine heading levels present
                var minLevel = 6;
                for (var t = 0; t < headings.length; t++) {
                    var lvl = parseInt(headings[t].tagName.charAt(1));
                    if (lvl < minLevel) minLevel = lvl;
                }

                var tocItems = '';
                for (var h = 0; h < headings.length; h++) {
                    var level = parseInt(headings[h].tagName.charAt(1)) - minLevel;
                    var cls = 'toc-l' + level;
                    tocItems += '<li class="' + cls + '"><a href="#toc-' + h + '">' + headings[h].textContent + '</a></li>';
                }

                var tocWrap = document.createElement('div');
                tocWrap.className = 'post-toc';
                tocWrap.innerHTML = '<div class="post-toc-btn" title="目录">目录</div><div class="post-toc-panel"><div class="post-toc-title">目录</div><ul class="post-toc-list">' + tocItems + '</ul></div>';

                document.body.appendChild(tocWrap);

                var btn = tocWrap.querySelector('.post-toc-btn');
                var panel = tocWrap.querySelector('.post-toc-panel');

                btn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    tocWrap.classList.toggle('open');
                });

                document.addEventListener('click', function (e) {
                    if (!tocWrap.contains(e.target)) {
                        tocWrap.classList.remove('open');
                    }
                });

                // Highlight active TOC item on scroll
                var tocLinks = panel.querySelectorAll('a');

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
