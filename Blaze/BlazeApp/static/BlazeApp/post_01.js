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

// function addNewComment(commentForm) {
//     // Get the comment text and post ID from the form
//     var commentText = commentForm.querySelector('#post-comment').value;
//     var commentContainer = commentForm.parentNode.nextElementSibling;
    

//     // Check if the comment is not empty
//     if (commentText.trim() !== '') {
//         // Fetch the user's profile picture URL here using AJAX or a static URL
//         var userProfilePictureSrc = commentForm.previousElementSibling.querySelector('img').src;

//         // Create a new comment div
//         var newCommentDiv = document.createElement('div');
//         newCommentDiv.classList.add("posted-comments-item", "my-2", "ps-1", "pe-3");
//         newCommentDiv.innerHTML = `
//              <div class="post-d-profile-pic ms-2 me-3 my-1">
//                  <img src="${userProfilePictureSrc}" alt="user profile picture" style="width: inherit;" />
//              </div>
//              <div class="posted-comment col py-1 px-2 bg-light border">${commentText}</div>`;


//         // Append the new comment div to the corresponding post's comments
//         commentContainer.appendChild(newCommentDiv);
//         // Clear the input field
//         commentForm.querySelector('#post-comment').value = '';
//     }

//     return false; // Prevent form submission
// }

