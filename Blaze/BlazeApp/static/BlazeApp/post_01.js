document.addEventListener("DOMContentLoaded", function() {
    var fileInput = document.getElementById('picture-upload');
    // console.log(fileInput)
    fileInput.addEventListener('change', function() {
        previewImage(fileInput);
    });

});

function previewImage(fileInput) {
    var preview = document.getElementById('image-preview');

    while (preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }

    var file = fileInput.files[0];
    var imageType = /^image\//;

    if (imageType.test(file.type)) {
        var img = document.createElement('img');
        img.classList.add('img-thumbnail');
        img.file = file;
        preview.appendChild(img);

        var reader = new FileReader();
        reader.onload = (function(aImg) {
            return function(e) {
                aImg.src = e.target.result;
            };
        })(img);

        reader.readAsDataURL(file);
    } else {
        alert('Please select a valid image file.');
        fileInput.value = ''; // Clear the input field if an invalid file is selected
    }
}

function autoResize(textarea) {
    textarea.style.height = 'auto'; // Reset the height to auto to calculate the new height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set the height to the calculated scroll height
}
