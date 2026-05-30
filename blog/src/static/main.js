/* Main JavaScript for the static blog */
(function () {
    "use strict";

    // Open external links in new tab
    document.addEventListener("DOMContentLoaded", function () {
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
    });
})();
