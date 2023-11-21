document.addEventListener("DOMContentLoaded", () => {
    check_follow_or_unfollow();

    // Render all posts
    show_posts();

})

function check_follow_or_unfollow() {
    const uid = document.querySelector('#user-name-d').dataset.uid;
    fetch(`/check_follow_or_unfollow/${uid}/`, {
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
                const fufd = document.querySelector("#fuf-d");

                if (data.follow_status) {
                    // user has followed the this user
                    fufd.innerHTML = `<button class="btn btn-outline-dark">Unfollow</button>`
                } else {
                    // user has not followed the this user
                    fufd.innerHTML = `<button class="btn btn-dark">Follow</button>`
                }
                const followButton = fufd.querySelector('button');
                followButton.addEventListener("click", () => { follow_or_unfollow() });
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}
function follow_or_unfollow() {
    const uid = document.querySelector('#user-name-d').dataset.uid;
    fetch(`/follow_or_unfollow/${uid}/`, {
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
                const fufd = document.querySelector("#fuf-d");

                if (data.follow_status) {
                    // user has followed the this user
                    fufd.innerHTML = `<button class="btn btn-outline-dark">Unfollow</button>`
                } else {
                    // user has not followed the this user
                    fufd.innerHTML = `<button class="btn btn-dark">Follow</button>`
                }
                const followButton = fufd.querySelector('button');
                followButton.addEventListener("click", () => { follow_or_unfollow() });
                update_follow_count(data.follow_status);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}
function update_follow_count(follow_status) {
    let follow_count = parseInt(document.querySelector("#follow-d").innerHTML)
    if (follow_status == true) {
        follow_count += 1;
    }
    else {
        follow_count -= 1;
    }

    // Update the like count in the HTML
    document.querySelector("#follow-d").innerHTML = follow_count;
}


function show_posts() {
    document.querySelector("#profile-posts-d").style.display = "flex";
    document.querySelector("#profile-saved-posts-d").style.display = "none";

    let x = document.querySelector("#ps-pb");
    let y = document.querySelector("#ps-sb");
    if (x !== null && y) {
        document.querySelector("#ps-pb").classList.add("show_status");
        document.querySelector("#ps-sb").classList.remove("show_status");
        x.innerHTML = `
            <i class="fs-5 bi bi-file-richtext-fill mx-2"></i><span class="mx-2" style="font-size: 0.9rem">Posts</span>
        `;
        y.innerHTML = `
            <i class="fs-5 bi bi-bookmark mx-2"></i><span class="mx-2" style="font-size: 0.9rem">Saved</span>
        `;
    }

}
function show_saved_posts() {
    document.querySelector("#profile-posts-d").style.display = "none";
    document.querySelector("#profile-saved-posts-d").style.display = "flex";
    let x = document.querySelector("#ps-pb");
    let y = document.querySelector("#ps-sb");
    if (x !== null && y) {
        document.querySelector("#ps-pb").classList.remove("show_status");
        document.querySelector("#ps-sb").classList.add("show_status");
        x.innerHTML = `
            <i class="fs-5 bi bi-file-richtext mx-2"></i><span class="mx-2" style="font-size: 0.9rem">Posts</span>
        `;
        y.innerHTML = `
            <i class="fs-5 bi bi-bookmark-fill mx-2"></i><span class="mx-2" style="font-size: 0.9rem">Saved</span>
            `;
    }
}

