/**
 * profileMgmt.js
 * 
 * Handles API calls to manage user profiles
 *  - Create a new profile
 *  - Get a list of profiles (for the profile selection page)
 *  - Set an active profile
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
        console.log('Profile creation form submitted');
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


/**
 * Fetches the list of profiles from the server and populates the profile selection list.
 * Each profile is displayed as a list item with a link.
 * The list items have a data attribute `data-profile-id` to identify the profile.
 * Clicking on a profile sets it as the active profile and redirects to the home page.
*/
fetch('/api/profile/get_active')
    .then(res => res.json())
    .then(profile => {
        console.log('Active profile:', profile.data.active_profile.name);

        // Update the profile name in the DOM, defaulting to 'Guest' if not set
        document.getElementById('profile-name').textContent = profile.data.active_profile.name || 'Guest';
        
        // Update the profile image in the DOM, defaulting to 'guest.png' if not set
        document.getElementById('profile-img').src = '/static/img/profiles/' + (profile.data.active_profile.image || 'guest.png');
        document.getElementById('profile-img').alt = profile.data.active_profile.name || 'Guest';       
    });




/**
 * Attaches click event listeners to each profile list item.
 * When a profile is clicked, it sends a POST request to set that profile as the active one.
 * On success, it redirects the user to the home page.
 */
document.querySelectorAll('.list-group-item[data-profile-id]').forEach(function(item) {
    item.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default link behavior
        const profileId = this.getAttribute('data-profile-id');
        const profileAdmin = this.getAttribute('data-profile-admin');
        console.log('Setting admin status:', profileAdmin);

        // Send a POST request to set the selected profile as active
        fetch('/api/profile/set_active', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    profile_id: profileId,
                    profile_admin: profileAdmin
                }
        )
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
