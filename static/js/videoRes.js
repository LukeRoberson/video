/**
 * @file videoRes.js
 * @description Handles resolution switching functionality for the video player using video.js and the videoJsResolutionSwitcher plugin.
 *
 * Initializes the video.js player, sets up the resolution switcher with a default resolution,
 * and ensures the control bar is visible. Logs resolution changes to the console.
 */


// Initialize video.js player and resolution switcher when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
var player = videojs('player');

// Initialize the resolution switcher
player.videoJsResolutionSwitcher({
    default: 'high',
//   dynamicLabel: true,
    ui: true,
    callback: function (resolution) {
    console.log("Resolution changed to:", resolution);
    }
});

// Ensure the control bar is visible
player.controlBar.show();
});
