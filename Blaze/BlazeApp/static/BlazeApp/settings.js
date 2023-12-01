document.addEventListener("DOMContentLoaded", () => {
    // Working for dark mode
    let dark_mode_switch = document.getElementById("SwitchDarkMode");
    if (dark_mode_switch !== undefined) {
        dark_mode_switch.addEventListener("click", () => { toogleDarkMode() })
        setDarkModeToggle();
    }

    // Working for Profile picture cropper
    // Initialize Cropper.js
    const image = document.getElementById('cropper-image');
    const cropper = new Cropper(image, {
        aspectRatio: 1,  // Set the aspect ratio as needed
        viewMode: 1,     // Set the view mode as needed
    });

    // Handle file selection and show preview
    const input = document.getElementById('new_pfp');
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = (event) => {
                cropper.replace(event.target.result);
                document.getElementById('cropper-container').classList.remove('d-none');
            };

            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    const form = document.getElementById('profile-picture-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const croppedData = cropper.getData();

        // Get the cropped data and set it to the hidden field
        document.getElementById('pfp_x').value = croppedData["x"];
        document.getElementById('pfp_y').value = croppedData["y"];
        document.getElementById('pfp_width').value = croppedData["width"];
        document.getElementById('pfp_height').value = croppedData["height"];
        // Submit the form
        form.submit();
    });
})


function toogleDarkMode() {
    const current_theme = localStorage.getItem('theme')
    if (current_theme == 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'light')
        localStorage.setItem('theme', "light")
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        localStorage.setItem('theme', "dark")
    }
}

function setDarkModeToggle() {
    let dark_mode_switch = document.getElementById("SwitchDarkMode");
    if (dark_mode_switch !== undefined) {
        if (localStorage.getItem("theme") === "light" || localStorage.getItem("theme") === null) {
            dark_mode_switch.checked = false
        }
        else {
            dark_mode_switch.checked = true
        }
    }
    else
    {
        console.error("No switch found at the moment.")
    }
}