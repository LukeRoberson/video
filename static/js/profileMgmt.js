/**
 * profileMgmt.js
 * 
 * Handles API calls to manage user profiles
 *  - Get a list of profiles (for the profile selection page)
 *  - Create a new profile
 */


/**
 * An event listener to create a new profile when the form is submitted.
 */
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent default form submission

    const name = document.getElementById('name').value;
    const image = document.getElementById('profile_pic').value;

    fetch('/api/profile/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, image: image })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        // Redirect to select_profile page after creation
        window.location.href = '/select_profile';
    });
});
