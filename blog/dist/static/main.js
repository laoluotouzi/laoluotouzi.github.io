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
    });
})();
