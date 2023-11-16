document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".post-like-btn").forEach((element) => {
        element.addEventListener("click", (event) => {
            like_or_unlike(event.currentTarget);
        })
    });
    document.querySelectorAll(".post-save-btn").forEach((element) => {
        element.addEventListener("click", (event) => {
            save_or_unsave(event.currentTarget);
        })
    });

    // Update the content on the page
    update_likes();
    update_saves();
})


// Like Post Functionalities
function like_or_unlike(element) {
    // Getting post id of the post
    let pid = element.parentNode.parentNode.parentNode.dataset.pid;
    // Getting like icon from post div
    fetch(`/like_or_unlike/${pid}/`, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error === null) {
                if (data.like_status) {
                    // user has liked the post
                    element.innerHTML = `<i class="text-danger fs-5 m-1 bi bi-heart-fill"></i>
                    <div class="d-none d-md-block ms-3 fs-6">Likes</div>`
                } else {
                    // user has unliked the post
                    element.innerHTML = `<i class="fs-5 m-1 bi bi-heart"></i>
                                        <div class="d-none d-md-block ms-3 fs-6">Likes</div>`
                }
                update_like_count(element, data.like_status);
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });

}

function update_like_count(element, like_status) {
    let like_count = parseInt(element.parentNode.parentNode.childNodes[1].querySelector("#postLikedNum").innerHTML);

    if (like_status == true) {
        like_count += 1;
    }
    else {
        like_count -= 1;
    }

    // Update the like count in the HTML
    element.parentNode.parentNode.childNodes[1].querySelector("#postLikedNum").innerHTML = like_count;
}

function update_likes() {
    document.querySelectorAll(".post-like-btn").forEach((element) => {
        let pid = element.parentNode.parentNode.parentNode.dataset.pid;
        fetch(`/check_like_or_unlike/${pid}/`, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error === undefined) {
                    if (data.like_status) {
                        // user has liked the post
                        element.innerHTML = `<i class="text-danger fs-5 m-1 bi bi-heart-fill"></i>
                        <div class="d-none d-md-block ms-3 fs-6">Likes</div>`
                    } else {
                        // user has unliked the post
                        element.innerHTML = `<i class="fs-5 m-1 bi bi-heart"></i>
                                            <div class="d-none d-md-block ms-3 fs-6">Likes</div>`
                    }
                }
            })
            .catch(error => {
                // Handle the error here
                console.error('Fetch error:', error);
            });
    });
}


// Saved Post Functionalities
function save_or_unsave(element) {
    // Getting post id of the post
    let pid = element.parentNode.parentNode.parentNode.dataset.pid;
    // Getting like icon from post div
    fetch(`/save_or_unsave/${pid}/`, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error === null) {
                if (data.saved_status) {
                    // user has saved the post
                    element.innerHTML = `<i class="text-night fs-5 m-1 bi bi-bookmark-fill"></i>
                <div class="d-none d-md-block ms-3 fs-6">Saved</div>`
                } else {
                    // user has not saved the post
                    element.innerHTML = `<i class="fs-5 m-1 bi bi-bookmark"></i>
                <div class="d-none d-md-block ms-3 fs-6">Saved</div>`
                }
                update_saved_count(element, data.saved_status);
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}

function update_saved_count(element, saved_status) {
    let saved_count = parseInt(element.parentNode.parentNode.childNodes[1].querySelector("#postSavedNum").innerHTML);
    if (saved_status == true) {
        saved_count += 1;
    }
    else {
        saved_count -= 1;
    }

    // Update the like count in the HTML
    element.parentNode.parentNode.childNodes[1].querySelector("#postSavedNum").innerHTML = saved_count;
}

function update_saves() {
    document.querySelectorAll(".post-save-btn").forEach((element) => {
        let pid = element.parentNode.parentNode.parentNode.dataset.pid;
        fetch(`/check_save_or_unsave/${pid}/`, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error === undefined) {
                    if (data.saved_status) {
                        // user has saved the post
                        element.innerHTML = `<i class="text-night fs-5 m-1 bi bi-bookmark-fill"></i>
                    <div class="d-none d-md-block ms-3 fs-6">Saved</div>`
                    } else {
                        // user has not saved the post
                        element.innerHTML = `<i class="fs-5 m-1 bi bi-bookmark"></i>
                    <div class="d-none d-md-block ms-3 fs-6">Saved</div>`
                    }
                }
            })
            .catch(error => {
                // Handle the error here
                console.error('Fetch error:', error);
            });
    });
}