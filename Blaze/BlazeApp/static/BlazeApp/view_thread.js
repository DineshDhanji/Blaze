document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".reply-d").forEach(e => {
        e.addEventListener("click", (event) => {
            // unload_reply_from_container();
            load_reply_in_container(event.currentTarget);
        });
    })
})


function load_reply_in_container(element) {
    aid = element.parentNode.parentNode.dataset.aid;
    unload_reply_from_container();
    fetch(`/get_answer/${aid}/`, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(answer_instance => {
            if (answer_instance.error === null) {
                // Filling header
                const header = document.querySelector("#reply-header");
                header.innerHTML = `
                   <div class="d-flex" data-aid='${answer_instance.data.id}'>
                            <a href="/profile/129s36dpv=k35${answer_instance.data.poster.id}313d60c3a9pvmq5c3vjg">
                              <div class="ms-2 me-3 my-1" style="border: 2px solid black; border-radius: 50%; padding: 2px; border-color:${answer_instance.data.poster.ring_color}!important;">
                                <div class="post-d-profile-pic">
                                  <img src="${answer_instance.data.poster.profile_picture}" alt="poster profile picture" style="width: inherit;" />
                                </div>
                              </div>
                            </a>
                            <div class="d-flex flex-column justify-content-center text-truncate">
                            <a href="/profile/129s36dpv=k35${answer_instance.data.poster.id}313d60c3a9pvmq5c3vjg">
                                <div class="text-body-emphasis">${answer_instance.data.poster.first_name} ${answer_instance.data.poster.last_name}</div>
                            </a>
                              <div class="post-d-timestamp text-secondary">${Date(answer_instance.data.timestamp).toString()}</div>
                            </div>
                          </div>
                          <div class="mx-2 mt-3 text-break text-body-emphasis">${answer_instance.data.content}</div>
                          `;
                // Filling input div 
                const content = document.querySelector("#reply-content");
                content.innerHTML = `
                          <form id="reply_form" class="d-flex flex-wrap" accept="#">
                          <input type="text" class="py-2 px-3 col-12 border rounded-5" style="outline: none;" name="reply" maxlength="500" required placeholder="Write your reply here"/>
                          <input type="submit" class="btn btn-dark border my-2" name="reply" value="Post" />
                          </form>
                          `;

                content.querySelector("form").addEventListener("submit", (e) => {
                    do_reply(e, answer_instance.data.id, element);
                })
                // Filling all replies
                const footer = document.querySelector("#reply-footer");
                answer_instance.data.replies.forEach((re_instance) => {
                    let new_reply_item = document.createElement("div");
                    new_reply_item.classList.add("post-all-comments-item", "col-12", "my-3");
                    new_reply_item.innerHTML = `
                            <div class="ms-2 me-3 my-1" style="width: max-content; height: max-content;border: 2px solid black; border-radius: 50%; padding: 2px; border-color: ${re_instance.uid.ring_color}!important;">
                            <a href="/profile/129s36dpv=k35${re_instance.uid.id}313d60c3a9pvmq5c3vjg">    
                            <div class="post-d-profile-pic">
                                    <img src="${re_instance.uid.profile_picture}" alt="poster profile picture" style="width: inherit;" />
                                </div>
                                </a>
                            </div>
                            <div class="post-comment-d p-2 border rounded bg-body-tertiary col-9">
                                <div class="d-flex justify-content-between" id="reply-dh">
                                    <div style="width:-webkit-fill-available;">
                                    <a href="/profile/129s36dpv=k35${re_instance.uid.id}313d60c3a9pvmq5c3vjg">    
                                        <div class="fw-semibold text-truncate text-break text-body-emphasis">${re_instance.uid.first_name} ${re_instance.uid.last_name}</div>
                                    </a>    
                                    <div class="fw-normal mb-2 text-secondary" style="font-size: 0.7rem;">${re_instance.timestamp}</div>
                                    </div>
                                </div>
                                <div class="text-break text-body-emphasis">${re_instance.content}</div>
                            </div>
                    `;

                    let uid = document.querySelector("#replyContainer").dataset.uid;
                    if (uid == re_instance.uid.id) {

                        let btn_div = document.createElement("div");
                        btn_div.classList.add("btn-group", "dropstart", "post-delete-d");
                        btn_div.innerHTML = `
                                    <button type="button" class="btn text-night dropdown-toggle" style="height: 2rem; width: 2rem; padding: 0rem;" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-three-dots-vertical"></i></button>
                                          <ul class="dropdown-menu">
                                            <li class="fs-6">
                                            <form action="/delete_reply/${re_instance.id}/">
                                                <input type="hidden" name="reply_id" value="${re_instance.id}" />
                                                <button type="submit" class="dropdown-item text-danger">Delete your reply</button>
                                            </form>
                                            </li>
                                            </ul>
                                            `;
                        new_reply_item.querySelector("#reply-dh").append(btn_div);
                    }
                    footer.append(new_reply_item);
                })
            } else {
                console.error(answer_instance.error);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}
function unload_reply_from_container() {
    // header
    document.querySelector("#reply-header").innerText = ``;
    // content
    document.querySelector("#reply-content").innerHTML = `
    <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    `;
    // footer
    document.querySelector("#reply-footer").innerHTML = "";
}

function do_reply(e, answer_id, element) {
    e.preventDefault();
    const form = document.querySelector("#reply_form");
    const new_reply = form.querySelector("input").value;

    if (new_reply.length === 0) {
        return;
    }

    fetch(`/create_reply/${answer_id}/${new_reply}/`, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(reply_instance => {
            if (reply_instance.error === null) {
                let new_reply_item = document.createElement("div");
                new_reply_item.classList.add("post-all-comments-item", "col-12", "my-3");
                new_reply_item.innerHTML = `
            <div class="ms-2 me-3 my-1" style="width: max-content; height: max-content;border: 2px solid black; border-radius: 50%; padding: 2px; border-color: ${reply_instance.data.uid.ring_color}!important;">
                <div class="post-d-profile-pic">
                    <img src="${reply_instance.data.uid.profile_picture}" alt="poster profile picture" style="width: inherit;" />
                </div>
            </div>
            <div class="post-comment-d p-2 border rounded bg-body-tertiary col-9">
                <div class="d-flex justify-content-between" id="reply-dh">
                    <div style="width:-webkit-fill-available;">
                        <div class="fw-semibold text-truncate text-break text-body-emphasis">${reply_instance.data.uid.first_name} ${reply_instance.data.uid.last_name}</div>
                        <div class="fw-normal mb-2 text-secondary" style="font-size: 0.7rem;">${reply_instance.data.timestamp}</div>
                    </div>
                </div>
                <div class="text-break text-body-emphasis">${reply_instance.data.content}</div>
            </div>
    `;

                let uid = document.querySelector("#replyContainer").dataset.uid;
                if (uid == reply_instance.data.uid.id) {

                    let btn_div = document.createElement("div");
                    btn_div.classList.add("btn-group", "dropstart", "post-delete-d");
                    btn_div.innerHTML = `
                    <button type="button" class="btn text-night dropdown-toggle" style="height: 2rem; width: 2rem; padding: 0rem;" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-three-dots-vertical"></i></button>
                          <ul class="dropdown-menu">
                            <li class="fs-6">
                            <form action="delete_answer/${reply_instance.data.id}/" method="post">
                                <input type="hidden" name="reply_id" value="${reply_instance.data.id}" />
                                <button type="submit" class="dropdown-item text-danger">Delete your reply</button>
                                </form>
                            </li>
                            </ul>
                            `;
                    new_reply_item.querySelector("#reply-dh").append(btn_div);
                }
                const footer = document.querySelector("#reply-footer");
                footer.append(new_reply_item);
                element.querySelectorAll('span')[0].innerText = parseInt(element.querySelectorAll('span')[0].innerText) + 1;
            } else {
                console.error(reply_instance.error);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });





    // Clear the reply
    form.querySelector("input").value = '';
}