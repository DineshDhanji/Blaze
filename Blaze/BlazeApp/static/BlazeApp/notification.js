document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#nbtn").addEventListener("click", () => {
        update_notifications();
    })

    // Call the function to start checking for new notifications
    check_indicator();
    check_for_new_notifications();
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


function check_for_new_notifications() {
    // You need to adjust this URL to match your backend endpoint for fetching notifications
    const apiUrl = '/notification_heart_beat/';

    // Keep track of the last notification ID to avoid duplicates
    let lastNotificationId = localStorage.getItem("lastNotificationId");
    // Function to fetch new notifications
    function fetchNotifications() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => handleNotifications(data.data))
            .catch(error => console.error('Error fetching notifications:', error));
    }
    // Function to handle new notifications
    function handleNotifications(notifications) {
        notifications.forEach(notification => {
            // Check if the notification is new
            if (notification.id > lastNotificationId) {
                // Play notification sound

                playNotificationSound();
                check_indicator();
                update_notifications();
                // Update lastNotificationId
                lastNotificationId = notification.id;
                localStorage.setItem("lastNotificationId", notification.id)
                // You can also display the notification in the UI or perform other actions
                console.log('New Notification:', notification);
            }
        });
    }

    // Function to play notification sound
    function playNotificationSound() {
        const notificationSound = new Audio('/static/BlazeApp/sounds/notification_sound.mp3'); // Adjust the path to your notification sound file
        notificationSound.play();
    }

    // Fetch notifications every 30 seconds (adjust as needed)
    setInterval(fetchNotifications, 1000);
}

function update_notifications() {
    // You need to adjust this URL to match your backend endpoint for fetching notifications
    const apiUrl = '/notification_heart_beat/';
    function fetchNotifications() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => handleNotifications(data.data))
            .catch(error => console.error('Error fetching notifications:', error));
    }
    function generate_url(notification) {
        // {% url 'BlazeApp:view_post' notification.object_id %}
        if (notification.object_type == "post") {
            return `/view_post/xy9i3ao40yr6zp${notification.object_id}ssd&2um[a/`
        }
        else if (notification.object_type == "event") {
            return `/view_event/pqmpevna5fjc0yr6zp${notification.object_id}sdhfd[m[a/`
        }
        else if (notification.object_type == "question") {
            return `/view_thread/cs2vmfps0sfd5ad${notification.object_id}sdhfd[mlca73vps[a/`
        }
    }
    const nul = document.querySelector("#nul");
    nul.innerHTML = `
        <div class="d-flex flex-column justify-content-center align-items-center" style="height:20rem">
            <div class="spinner-grow text-body-emphasis" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="my-3 text-secondary">Waiting</div> 
        </div>`;

    fetchNotifications()
    // Function to handle new notifications
    function handleNotifications(notifications) {
        nul.innerHTML = "";
        notifications.forEach(notification => {
            const li_element = document.createElement("li");
            if (notification.is_read) {
                li_element.classList.add("list-group-item", "bg-body-tertiary", "notification-item", "rounded", "border", "noti-read");
            }
            else {
                li_element.classList.add("list-group-item", "bg-body-secondary", "notification-item", "rounded", "border", "noti-read");
            }
            li_element.dataset.nid = notification.id;
            let notification_url = generate_url(notification);
            li_element.innerHTML = `
            <a href="${notification_url}">
                <div class="mt-1 text-body-emphasis">
                    ${notification.content}
                </div>
                <div class="mt-2 text-secondary"style="font-size: 0.7rem;">
                    ${notification.timestamp}
                </div>
            </a> 
            `;
            li_element.addEventListener("click", (event) => {
                read_noti(event.currentTarget);
            })
            nul.append(li_element);
        });
    }
}

function check_indicator() {
    const apiUrl = '/notification_heart_beat/';

    // Function to fetch new notifications
    function fetchNotifications() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => handleNotifications(data.data))
            .catch(error => console.error('Error fetching notifications:', error));
    }
    // Function to handle new notifications
    function handleNotifications(notifications) {
        for (let i = 0; i < notifications.length; i++) {
            if (!notifications[i].is_read) {

                let indicator = document.createElement("div");
                indicator.setAttribute("id", "noti-indicator");
                document.querySelector("#nbtn").append(indicator)
                return;
            }
        }
        document.querySelector("#nbtn").innerHTML = `<i class="bi bi-bell"></i>`;
        return;
    }
    fetchNotifications();
}