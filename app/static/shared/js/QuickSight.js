/**
 * This module embeds an AWS QuickSight dashboard.
 *
 * It depends on the quicksight-embedding-js-sdk being
 * loaded in the window.
 */
(function() {
    'use strict';

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

    window.addEventListener('load', function() {
        var embedLocation = document.getElementById("dashboardContainer");
        var embedUrl = embedLocation.dataset.url;
        embedDashboard(embedLocation, embedUrl);
    });

})();
