/**
 * @file videoAdd.js
 * @description API call to add a video to the database
 *
 * Used on the admin page to handle the addition of videos to the database.
 * This script is triggered when the "Add to Database" button is clicked per video.
 */


/**
 * Build a table to display videos that can be added to the database.
 * Calls the API endpoint to fetch video data in JSON format, which is converted to an array.
 */
document.getElementById('listVideosBtn').addEventListener('click', function() {
    fetch('/api/videos/csv')
        .then(response => response.json())
        .then(data => {
            console.log('Videos data:', data);

            // Convert the object to an array
            const items = Array.isArray(data) ? data : Object.values(data);

            if (!items.length) {
                document.getElementById('videosTableContainer').innerHTML = '<p class="text-warning">No videos found.</p>';
                return;
            }

            // Create a table to display the videos
            let table = '<table class="table table-dark table-striped">';
            table += `
                <thead>
                    <tr>
                        <th>Video Name</th>
                        <th>URL</th>
                        <th>Main Cat</th>
                        <th>Sub Cat</th>
                        <th>1080</th>
                        <th>720</th>
                        <th>480</th>
                        <th>360</th>
                        <th>240</th>
                        <th>Thumb</th>
                        <th>Time</th>
                    </tr>
                </thead>`;
            table += '<tbody>';
                
            // Loop through the items, add to table
            items.forEach(element => {
                table += `
                    <tr>
                        <td>${element.video_name || 'N/A'}</td>
                        <td>${element.video_url ? `<span style="color: green;" title="${element.video_url}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.main_cat_name || 'N/A'}</td>
                        <td>${element.sub_cat_name || 'N/A'}</td>
                        <td>${element.url_1080 ? `<span style="color: green;" title="${element.url_1080}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.url_720 ? `<span style="color: green;" title="${element.url_720}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.url_480 ? `<span style="color: green;" title="${element.url_480}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.url_360 ? `<span style="color: green;" title="${element.url_360}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.url_240 ? `<span style="color: green;" title="${element.url_240}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.thumbnail ? `<span style="color: green;" title="${element.thumbnail}">✔</span>` : '<span style="color: red;">✘</span>'}</td>
                        <td>${element.duration || 'N/A'}</td>
                        <td>
                            <button 
                                class="btn btn-success btn-sm" 
                                title="Add to Database" 
                                onclick="addToDatabase(${JSON.stringify(element).replace(/"/g, '&quot;')}, this)">
                                +
                            </button>
                        </td>
                    </tr>`;
            });

            // Complete the table
            table += `
                </tbody>
                </table>`;
            document.getElementById('videosTableContainer').innerHTML = table;

            // Show the container
            document.getElementById('videosTableWrapper').classList.remove('d-none');
        })
        .catch(error => {
            document.getElementById('videosTableContainer').innerHTML = '<p class="text-danger">Error loading videos.</p>';
            console.error('Error:', error);
        });
});


/**
 * Add a video to the database.
 * This function is called when the "Add to Database" button is clicked for a specific video
 * 
 * @param {*} video - The video object containing all necessary data to be added to the database.
 * @param {*} button - The button element that was clicked to trigger this function.
 */
function addToDatabase(video, button) {
    // API call to add video to the database
    fetch('/api/videos/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(video),
    })

    .then(response => {
        if (response.ok) {
            response.json().then(data => {
                alert(data.message || 'Video added to the database successfully!');
            });
            button.disabled = true;
            button.classList.remove('btn-success');
            button.classList.add('btn-secondary');
        } else {
            alert('Failed to add video to the database.');
        }
    })

    .catch(error => {
        console.error('Error adding video to the database:', error);
        alert('An error occurred while adding the video.');
    });
}
