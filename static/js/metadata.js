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

    // Create payload object to send to the server
    const payload = {
        video_name: video_name,
        description: description,
        url: url,
        tag_name: tag_name,
        speaker_name: speaker_name,
        character_name: character_name,
        scripture_name: scripture_name
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


// Resolves a name (video, tag, speaker, character) to its corresponding ID using the API
async function resolveNameToId(type, name, idInputId) {
    if (!name) {
        // If no name is provided, clear the ID input field
        document.getElementById(idInputId).value = '';
        return;
    }
    // Determine the query parameter based on the type
    let param = '';
    if (type === 'video') param = 'video_name';
    if (type === 'tag') param = 'tag_name';
    if (type === 'speaker') param = 'speaker_name';
    if (type === 'character') param = 'character_name';
    const url = `/api/video/metadata?${param}=${encodeURIComponent(name)}`;
    try {
        // Fetch the ID from the server
        const response = await fetch(url);
        const result = await response.json();
        let idValue = '';
        // Extract the correct ID from the response based on type
        if (type === 'video') idValue = result.video_id ?? '';
        if (type === 'tag') idValue = result.tag_id ?? '';
        if (type === 'speaker') idValue = result.speaker_id ?? '';
        if (type === 'character') idValue = result.character_id ?? '';
        // Set the resolved ID in the corresponding input field
        document.getElementById(idInputId).value = idValue;
    } catch (err) {
        // On error, clear the ID field and alert the user
        document.getElementById(idInputId).value = '';
        alert('Error resolving ID: ' + err);
    }
}

// Add event listeners to resolve buttons for each type
document.getElementById('resolveVideoBtn').addEventListener('click', function() {
    const name = document.getElementById('videoName').value;
    resolveNameToId('video', name, 'videoId');
});
document.getElementById('resolveTagBtn').addEventListener('click', function() {
    const name = document.getElementById('tagName').value;
    resolveNameToId('tag', name, 'tagId');
});
document.getElementById('resolveSpeakerBtn').addEventListener('click', function() {
    const name = document.getElementById('speakerName').value;
    resolveNameToId('speaker', name, 'speakerId');
});
document.getElementById('resolveCharacterBtn').addEventListener('click', function() {
    const name = document.getElementById('characterName').value;
    resolveNameToId('character', name, 'characterId');
});
