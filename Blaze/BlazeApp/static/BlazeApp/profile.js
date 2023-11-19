document.addEventListener("DOMContentLoaded", () => {
    check_follow_or_unfollow();

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