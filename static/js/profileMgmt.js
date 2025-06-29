/**
 * profileMgmt.js
 * 
 * Handles API calls to manage user profiles
 *  - Get a list of profiles (for the profile selection page)
 *  - Create a new profile
 */


/**
 * An event listener to create a new profile when the form is submitted.
 * This prevents the default form submission and sends a POST request to the server.
 * On success, it redirects the user to the profile selection page.
 */
// Only attach to the profile creation form
const profileForm = document.getElementById('profile-create-form');

// Continue if this is right
if (profileForm) {
    profileForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission

        const name = document.getElementById('name').value;
        const image = document.getElementById('profile_pic').value;

        fetch('/api/profile/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                { 
                    name: name,
                    image: image 
                }
            )
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            window.location.href = '/select_profile';   // Redirect
        });
    });
}

// Fetch the currently active profile from the server
fetch('/api/profile/get_active')
    .then(res => res.json())
    .then(profile => {
        console.log('Active profile:', profile.active_profile.name);
        // Update the profile name in the DOM, defaulting to 'Guest' if not set
        document.getElementById('profile-name').textContent = profile.active_profile.name || 'Guest';
        // Update the profile image in the DOM, defaulting to 'guest.png' if not set
        document.getElementById('profile-img').src = '/static/img/profiles/' + (profile.active_profile.image || 'guest.png');
        document.getElementById('profile-img').alt = profile.active_profile.name || 'Guest';
    });


// Add click event listeners to all profile list items to set the active profile
document.querySelectorAll('.list-group-item[data-profile-id]').forEach(function(item) {
    item.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default link behavior
        const profileId = this.getAttribute('data-profile-id');
        // Send a POST request to set the selected profile as active
        fetch('/api/profile/set_active', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ profile_id: profileId })
        })
        .then(res => res.json())
        .then(data => {
            // If successful, redirect to the home page
            if (data.success) {
                window.location.href = '/';
            }
        });
    });
});
