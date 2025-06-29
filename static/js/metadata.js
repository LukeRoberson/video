/**
 * metadata.js
 * 
 * Adds metadata to videos
 * Adds text to scriptures
 */


/**
 * Add metadata to a video
 * This function listens for the form submission event,
 * collects the form data, and sends it to the server via a POST request.
 */
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
            document.getElementById('addMetadataForm').reset();
        } else {
            alert('Failed to add metadata: ' + (result.error || 'Unknown error'));
        }

    } catch (err) {
        // Handle network or other errors
        alert('Error: ' + err);
    }
});



/**
 * Add text to a scripture
 * This function listens for the form submission event,
 * collects the form data, and sends it to the server via a POST request.
 */
document.getElementById('addScrForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevent default form submission

    // Get values from form fields
    const scr_name = document.getElementById('scrName').value;
    const scr_text = document.getElementById('scrText').value;

    // Create payload object to send to the server
    const payload = {
        scr_name: scr_name,
        scr_text: scr_text,
    };

    try {
        // Send POST request to add metadata
        const response = await fetch('/api/scripture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        // Show success or error message based on response
        if (result.success) {
            alert('Scripture text added successfully!');
            document.getElementById('scrText').value = '';
        } else {
            alert('Failed to add scripture text: ' + (result.error || 'Unknown error'));
        }

    } catch (err) {
        // Handle network or other errors
        alert('Error: ' + err);
    }
});
