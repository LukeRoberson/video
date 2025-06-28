/**
 * metadata.js
 * 
 * Adds metadata to videos
 * Converts names to IDs (eg, video names to video IDs)
 */

document.getElementById('addMetadataForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const video_id = document.getElementById('videoId').value;
    const url = document.getElementById('url').value;
    const tag_id = document.getElementById('tagId').value;
    const speaker_id = document.getElementById('speakerId').value;
    const character_id = document.getElementById('characterId').value;
    const scripture_id = document.getElementById('scriptureId').value;

    const payload = {
        video_id: video_id,
        url: url,
        tag_id: tag_id,
        speaker_id: speaker_id,
        character_id: character_id,
        scripture_id: scripture_id
    };

    try {
        const response = await fetch('/api/video/metadata', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (result.success) {
            alert('Metadata added successfully!');
        } else {
            alert('Failed to add metadata: ' + (result.error || 'Unknown error'));
        }
    } catch (err) {
        alert('Error: ' + err);
    }
});

async function resolveNameToId(type, name, idInputId) {
    if (!name) {
        document.getElementById(idInputId).value = '';
        return;
    }
    let param = '';
    if (type === 'video') param = 'video_name';
    if (type === 'tag') param = 'tag_name';
    if (type === 'speaker') param = 'speaker_name';
    if (type === 'character') param = 'character_name';
    const url = `/api/video/metadata?${param}=${encodeURIComponent(name)}`;
    try {
        const response = await fetch(url);
        const result = await response.json();
        let idValue = '';
        if (type === 'video') idValue = result.video_id ?? '';
        if (type === 'tag') idValue = result.tag_id ?? '';
        if (type === 'speaker') idValue = result.speaker_id ?? '';
        if (type === 'character') idValue = result.character_id ?? '';
        document.getElementById(idInputId).value = idValue;
    } catch (err) {
        document.getElementById(idInputId).value = '';
        alert('Error resolving ID: ' + err);
    }
}

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
