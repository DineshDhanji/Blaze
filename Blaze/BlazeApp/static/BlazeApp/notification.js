document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".notification-item").forEach((item) => {
        item.addEventListener("click", (event) => {
            read_noti(event.currentTarget);
        });
    });
});


function read_noti(element) {
    const nid = element.dataset.nid
    console.log(nid)
    fetch(`/read/${nid}/`, {
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
                
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            // Handle the error here
            console.error('Fetch error:', error);
        });
}