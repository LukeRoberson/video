/**
 * @file videoPlayer.js
 * @description Handles resolution switching functionality for the video player using video.js and the videoJsResolutionSwitcher plugin.
 *
 * Initializes the video.js player, sets up the resolution switcher with a default resolution,
 * and ensures the control bar is visible. Logs resolution changes to the console.
 */


document.addEventListener('DOMContentLoaded', function () {
    const player = videojs('player');
    const videoElement = document.getElementById('player');
    const profileId = videoElement.getAttribute('data-profile-id');
    const videoId = videoElement.getAttribute('data-video-id');
    let lastUpdateTime = 0;
    let hasMarkedWatched = false;

    // Initialize the resolution switcher
    player.videoJsResolutionSwitcher({
        default: 'high',
        ui: true,
        callback: function (resolution) {
            console.log("Resolution changed to:", resolution);
        }
    });

    // Ensure the control bar is visible
    player.controlBar.show();

    // Check if profileId and videoId are available
    if (!profileId || !videoId) {
       console.error('Missing profileId or videoId. Progress tracking will not work.');
        return;
    }

    // Track playback progress
    player.on('timeupdate', function () {
        const currentTime = Math.floor(player.currentTime());
        const duration = Math.floor(player.duration()); // Get the total duration of the video
        const now = Date.now(); // Get the current timestamp in milliseconds

        if (hasMarkedWatched) {
            return; // If already marked as watched, skip further processing
        }

        // Only send progress if at least 2 seconds have passed since the last update
        if (now - lastUpdateTime >= 2000 && currentTime > 5) {
            lastUpdateTime = now; // Update the last update time

            // Send the current time to the server
            fetch('/api/profile/in_progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    video_id: videoId,
                    current_time: currentTime
                })
            }).catch(err => console.error('Error updating progress:', err));
        }

        // Check if the video is considered "watched" (e.g., 96% watched)
        if (currentTime >= duration * 0.96 && !hasMarkedWatched) {
            hasMarkedWatched = true; // Ensure this is only sent once

            // Remove video from in-progress list
            fetch('/api/profile/in_progress', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    video_id: videoId
                })
            }).catch(err => console.error('Error marking video as watched:', err));

            // Mark the video as watched
            fetch('/api/profile/mark_watched', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    video_id: videoId,
                })
            }).catch(err => console.error('Error marking video as watched:', err));
        }
    });
});
