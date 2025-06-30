/**
 * watched.js
 *
 * Handles marking videos as watched in the video manager web app.
 * It sends an AJAX request to the server to update the video's watched status.
 */


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
