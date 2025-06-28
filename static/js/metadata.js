/**
 * metadata.js
 * 
 * Adds metadata to videos
 * Converts names to IDs (eg, video names to video IDs)
 */


// Listen for form submission on the add metadata form
document.getElementById('addMetadataForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevent default form submission

    // Get values from form fields
    const video_name = document.getElementById('videoName').value;
    const description = document.getElementById('description').value;
    const url = document.getElementById('url').value;
    const tag_name = document.getElementById('tagName').value;
    const speaker_name = document.getElementById('speakerName').value;
    const character_name = document.getElementById('characterName').value;
    const scripture_name = document.getElementById('scriptureName').value;
    const date_added = document.getElementById('dateAdded').value;


    // Create payload object to send to the server
    const payload = {
        video_name: video_name,
        description: description,
        url: url,
        tag_name: tag_name,
        speaker_name: speaker_name,
        character_name: character_name,
        scripture_name: scripture_name,
        date_added: date_added ? new Date(date_added).toISOString() : null
    };

    try {
        // Send POST request to add metadata
        const response = await fetch('/api/video/metadata', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        // Show success or error message based on response
        if (result.success) {
            alert('Metadata added successfully!');
        } else {
            alert('Failed to add metadata: ' + (result.error || 'Unknown error'));
        }

    } catch (err) {
        // Handle network or other errors
        alert('Error: ' + err);
    }
});
