/**
 * This module embeds an AWS QuickSight dashboard.
 *
 * global QuickSightEmbedding
 */
(function() {
    'use strict';

    /**
     * Embed QuickSight dashboard at a specific location.
     *
     * @param {HTMLElement} embedLocation
     * @param {string} embedUrl
     */
    function embedDashboard(embedLocation, embedUrl) {
        var options = {
            url: embedUrl,
            container: embedLocation,
            scrolling: "no",
            height: "500px",
            width: "850px"
        };
        QuickSightEmbedding.embedDashboard(options);
    }

    // Embed Dashboard after the window loads.
    window.addEventListener('load', function() {
        var embedLocation = document.getElementById("dashboardContainer");
        var embedUrl = embedLocation.dataset.url;
        embedDashboard(embedLocation, embedUrl);
    });

})();
