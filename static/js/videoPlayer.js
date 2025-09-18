/**
 * @file videoPlayer.js
 * @description Handles everything related to the video.js player
 *
 * Initializes the video.js player
 * Sets up the resolution switcher with a default resolution
 * Ensures the control bar is visible
 * Tracks video playback progress
 * Marks a video as watched when 96% of it has been viewed
 * Handles the form submission for marking a video as watched
 */


/**
 * An event listener for the DOMContentLoaded event that initializes the video player,
 * sets up the resolution switcher, and tracks video playback progress.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize the video.js player with custom options
    const player = videojs('player', {
        controlBar: {
            skipButtons: {
                forward: 10,
                backward: 5
            },
            qualitySelector: true,
            currentTimeDisplay: true,
            remainingTimeDisplay: {
                displayNegative: false
            }
        },
        aspectRatio: '16:9',
        fluid: true,
        enableSmoothSeeking: true
    });
    
    // Check if this device is a TV
    let isTV = window.tvDetection.isTV();
    
    // Function to apply TV-specific settings
    function applyTVSettings() {
        if (isTV) {
            // Larger control bar for TV
            player.ready(function() {
                const controlBar = player.controlBar.el();
                controlBar.style.height = '60px';
                controlBar.style.fontSize = '1.2em';
                
                // Auto-hide controls after longer delay on TV
                player.off('userinactive');
                player.on('userinactive', function() {
                    setTimeout(() => {
                        if (!player.paused()) {
                            player.userActive(false);
                        }
                    }, 8000); // 8 seconds instead of default 3
                });
            });
        }
    }

    // Apply initial TV settings
    applyTVSettings();

    // Listen for TV mode changes
    window.addEventListener('tvModeChanged', (e) => {
        isTV = e.detail.isTV;
        applyTVSettings();
    });
    
    // Get the parent of the video player (the div)
    const container = document.getElementById('player').parentElement;

    // Customise the video player
    player.ready(function() {
        // Create context menu element (right click menu)
        const contextMenu = document.createElement('div');
        contextMenu.className = 'video-context-menu';
        
        const menuItem = document.createElement('div');
        menuItem.textContent = 'Copy link at current time';
        menuItem.className = 'video-context-menu-item';

        contextMenu.appendChild(menuItem);
        document.body.appendChild(contextMenu);
        
        // Function to generate timestamped URL
        function getTimestampedUrl() {
            const currentTime = Math.floor(player.currentTime());
            const url = new URL(window.location.href);
            url.searchParams.set('t', currentTime);
            return url.toString();
        }
        
        // Handle right-click on progress bar
        const progressControl = player.controlBar.progressControl.el();
        progressControl.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            
            // Disable video player interactions while menu is open
            player.el().style.pointerEvents = 'none';

            // Position the context menu
            contextMenu.style.left = e.pageX + 'px';
            contextMenu.style.top = e.pageY + 'px';
            contextMenu.style.display = 'block';
            
            // Adjust position if menu would go off screen
            const rect = contextMenu.getBoundingClientRect();
            if (rect.right > window.innerWidth) {
                contextMenu.style.left = (e.pageX - rect.width) + 'px';
            }
            if (rect.bottom > window.innerHeight) {
                contextMenu.style.top = (e.pageY - rect.height) + 'px';
            }

            return false;
        });

        // Prevent right-click from resuming a paused video
        progressControl.addEventListener('mousedown', function(e) {
            if (e.button === 2) { // Right mouse button
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        });
        
        progressControl.addEventListener('mouseup', function(e) {
            if (e.button === 2) { // Right mouse button
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        });

        // Handle menu item click
        menuItem.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
           
            const timestampedUrl = getTimestampedUrl();
            
            navigator.clipboard.writeText(timestampedUrl).then(function() {
                showNotification('Link copied to clipboard!');
            }).catch(function(err) {
                console.error('Could not copy text: ', err);
                showNotification('Could not copy text!');
            });
            
            contextMenu.style.display = 'none';
            
            // Re-enable video player clicks
            player.el().style.pointerEvents = '';
        });
        
        // Hide context menu when clicking elsewhere - use capture phase
        document.addEventListener('click', function(e) {
            if (contextMenu.style.display === 'block') {
                if (!contextMenu.contains(e.target)) {
                    contextMenu.style.display = 'none';

                    // Re-enable video player clicks
                    player.el().style.pointerEvents = '';
                    
                    // Stop this click from doing anything else
                    e.preventDefault();
                    e.stopPropagation();
                }
            }
        }, true); // Capture phase

        // Show notification function
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.className = 'video-notification';
            
            document.body.appendChild(notification);
            
            // Trigger animation
            setTimeout(() => {
                notification.classList.add('show');
            }, 10);
            
            // Remove after 3 seconds
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentNode) {
                        document.body.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }

        // Add a custom button (for theatre mode)
        const Button = videojs.getComponent('Button');
        class TheatreButton extends Button {
            constructor(player, options) {
                super(player, options);
                this.controlText("Theatre Mode");
                this.addClass('vjs-theatre-button');
            }
            handleClick() {
                container.classList.toggle('theatre-mode');
            }
        }

        // Register the custom button with video.js
        videojs.registerComponent('TheatreButton', TheatreButton);
        
        // Find the index of the fullscreen button in the control bar    
        const controlBar = player.getChild('controlBar');
        const fullscreenIndex = controlBar.children().findIndex(child => child.name && child.name() === 'FullscreenToggle');

        // Insert TheatreButton just before the fullscreen button (second from right)
        const insertIndex = fullscreenIndex > 0 ? fullscreenIndex : controlBar.children().length - 1;
        controlBar.addChild('TheatreButton', {}, insertIndex);
    });

    // Enhanced keyboard controls for TV remotes
    // Only add these if the player has focus
    document.addEventListener('keydown', function(e) {
        // Only handle these keys if the video player area has focus
        if (!document.activeElement || !document.activeElement.closest('.video-js')) {
            return; // Let the main TV navigation handle it
        }

        // Only apply these controls in TV mode
        if (!isTV) return;

        switch(e.key) {
            case "ArrowLeft": // Left arrow - rewind 10s
                e.preventDefault();
                player.currentTime(Math.max(0, player.currentTime() - 10));
                break;
            
            case "ArrowRight": // Right arrow - fast forward 10s
                e.preventDefault();
                player.currentTime(player.currentTime() + 10);
                break;
            
            case "ArrowUp": // Up arrow - volume up
                e.preventDefault();
                player.volume(Math.min(1, player.volume() + 0.1));
                break;
            
            case "ArrowDown": // Down arrow - volume down
                e.preventDefault();
                player.volume(Math.max(0, player.volume() - 0.1));
                break;
            
            case "Enter": // Enter - play/pause
                e.preventDefault();
                if (player.paused()) {
                    player.play();
                } else {
                    player.pause();
                }
                break;
        }
    });


    // Check if there is a 't' parameter in the URL to jump to a specific time
    const urlParams = new URLSearchParams(window.location.search);
    const jumpTo = urlParams.get('t');
    if (jumpTo) {
        player.ready(function() {
            player.currentTime(parseInt(jumpTo, 10));
            player.pause();
            player.bigPlayButton.hide();
            player.on('seeked', function() {
                player.bigPlayButton.show();
                player.posterImage.hide();
                player.controlBar.show();
            });
        });
    }
    
    // Get the video element and its data attributes
    const videoElement = document.getElementById('player');
    const profileId = videoElement.getAttribute('data-profile-id');
    const videoId = videoElement.getAttribute('data-video-id');
    const currentTime = parseInt(videoElement.getAttribute('data-current-time'), 10) || 0;

    // Initialize variables for tracking playback progress
    let lastUpdateTime = 0;
    let hasMarkedWatched = false;

    // Set the starting position when the player is ready
    player.on('loadedmetadata', function () {
        if (currentTime > 0) {
            console.log('Setting playback position to:', currentTime);
            player.currentTime(currentTime); // Set the playback position
        }
    });

    // Remove the custom progress bar when the video starts playing
    player.on('play', function () {
        const progressOverlay = document.querySelector('.progress-overlay');
        if (progressOverlay) {
            progressOverlay.remove(); // Remove the progress bar overlay
            console.log('Custom progress bar removed.');
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

    // Check if the video is completely done
    player.on('ended', function () {
        console.log('Video playback completed.');
        if (container.classList.contains('theatre-mode')) {
            container.classList.remove('theatre-mode');
        }
    });
});



/**
 * Handles the form submission for marking a video as watched.
 * It prevents the default form submission, sends an AJAX request,
 * and updates the button text to indicate success.
 */
document.getElementById('markWatchedForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Get the API URL and video ID from data attributes
    const apiUrl = this.dataset.apiUrl;
    const videoId = this.dataset.videoId;

    // Send a POST request to the server to mark the video as watched
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ video_id: videoId })
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        // If the server responds with success, update the button
        if (data.success && this.dataset.apiUrl === '/api/profile/mark_watched') {
            this.querySelector('button').textContent = 'Watched!';
            this.dataset.apiUrl = '/api/profile/mark_unwatched';
        }
        else if (data.success && this.dataset.apiUrl === '/api/profile/mark_unwatched') {
            this.querySelector('button').textContent = 'Unwatched!';
            this.dataset.apiUrl = '/api/profile/mark_watched';
        }
    });
});

