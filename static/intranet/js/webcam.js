let w_width = window.innerWidth
let w_height = window.innerHeight
let user = document.getElementById('user').innerText

window.onload = function () {
    open_webcam();
    getCSRFToken();
    getSessionId();


}

function getCSRFToken() {
    const cookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    if (cookie) {
        return cookie.split('=')[1];
    } else {
        return null;
    }
}

function getSessionId() {
    const sessionid = document.cookie.split(';').find(cookie => cookie.trim().startsWith('sessionid='));

    if (sessionid) {
        return sessionid.split('=')[1];
    } else {
        return null;
    }
}

// Configure a few settings and attach camera
function open_webcam() {
    Webcam.set({
        width: 410,
        height: 320,
        image_format: 'png',
        jpeg_quality: 100,
        force_flash: false,
        radius: 20,
        fps: 45,

    });
    Webcam.attach('#my_camera');
}


function take_snapshot() {

    // take snapshot and get image data
    Webcam.snap(function (data_uri) {

        Webcam.snap((data_uri) => {
            const canvas = document.getElementById('canvas');
            const context = canvas.getContext('2d');
            const image = new Image();
            let dateTime = getDateTime()
            image.onload = () => {
                // context.drawImage(image, 0, 0, 640, 480);
                context.drawImage(image, 0, 0, 810, 520);
                context.font = "20px Arial"

                context.fillText(dateTime, 10, 30);
                context.fillText(user, 10, 50);
                const imageData = canvas.toDataURL('image/png');
                fetch('/api/save-image/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        imageData: imageData
                        // imageData: "salom"
                    })
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log(data);
                    });
            };
            image.src = data_uri;
        });
    });
}


function getDateTime() {
    let now = new Date();
    let date = now.getDate() + '/' + (now.getMonth() + 1) + '/' + now.getFullYear();
    let time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    let dateTime = time + '  ' + date;
    return dateTime
}