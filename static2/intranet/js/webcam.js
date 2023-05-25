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


function getDateTime() {
    let now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');
    const second = String(now.getSeconds()).padStart(2, '0');
    let dateTime = `${day}.${month}.${year} ${hour}:${minute}:${second}`;
    return dateTime
}

function take_snapshot() {
    let user_val = $('#user_select').val();
    let comment = $('#comment').val();
    if (user_val === '-1')
        Swal.fire(
            'Foydalanuvchi tanlanmadi',
            'Iltimos foydalanuvchini tanlang',
            'error'
        )
    else {
        Webcam.snap(function (data_uri) {
            Webcam.snap((data_uri) => {
                const canvas = document.getElementById('canvas');
                const context = canvas.getContext('2d');
                const image = new Image();
                let dateTime = getDateTime()
                image.onload = () => {
                    context.drawImage(image, 0, 0, 810, 520);
                    context.font = "20px Arial"

                    context.fillText(dateTime, 10, 30);
                    context.fillText(user, 10, 60);
                    context.fillText(user_val, 10, 90);
                    const imageData = canvas.toDataURL('image/png');
                    fetch('/api/save-image/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        body: JSON.stringify({
                            imageData: imageData,
                            worker: user_val,
                            comment: comment,
                        })
                    })
                        .then((response) => response.json())
                        .then((data) => {
                            if (data.status === 'success') {
                                Swal.fire({
                                    position: 'top-end',
                                    icon: 'success',
                                    title: data.message,
                                    showConfirmButton: false,
                                    timer: 2000,
                                    width: 400,
                                })
                            } else {
                                Swal.fire({
                                    position: 'top-end',
                                    icon: 'error',
                                    title: data.message,
                                    showConfirmButton: false,
                                    timer: 2000,
                                    width: 400,
                                })
                            }

                            console.log(data);
                        });
                };
                image.src = data_uri;
            });
        });


        $('#user_select').val('-1')
        $('#comment').val('')

    }
}