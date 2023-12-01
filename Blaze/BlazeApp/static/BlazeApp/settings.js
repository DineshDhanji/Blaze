document.addEventListener("DOMContentLoaded", () => {

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
                document.getElementById('cropper-container').classList.remove('hidden');
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