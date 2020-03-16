
var first_read = true
var read_status = 1
var unread_notifications = null

function updateNotifications(notificationList) {
    unread_notifications = notificationList
    $('#notification-center').empty()
    values = 0
    heartbit = 0
    received_notifications = []
    if (notificationList !== null) {
        Object.keys(notificationList).forEach(function (key) {
            received_notifications.push(notificationList[key])
        });
        received_notifications.sort(function (a, b) {
            return b.date - a.date
        })
        for (let i = 0; i < received_notifications.length && i < 5; i++) {
            var added = ""
            switch (received_notifications[i].type) {
                case 1216:
                case 1536:
                    added = '/assets/images/error.png'
                    break;
                case 1028:
                    added = '/assets/images/warning.png'
                    break;
                case 1:
                    added = '/assets/images/success.png'
                    break;
                default:
                    added = '/assets/images/info.png'
                    break;
            }
            var date = new Date(received_notifications[i].date)
            $('#notification-center').append('<a href="#">\n' +
                '<div class="user-img"> <img src=" ' + added + ' " alt="user" class="img-circle"> </div>' +
                '<div class="mail-contnet">' +
                '<h5> Robot ' + received_notifications[i].robot + '</h5>' +
                '<span class="mail-desc">' + received_notifications[i].message + '</span> <span class="time"> ' + date.getHours() + ':' + date.getMinutes() + ' </span>\n' +
                '</div>' +
                '</a>')
            if (received_notifications.length > 3) {

                Push.create('Multiples incidencias',{
                    body: 'Se han detectado ' + received_notifications.length + ' incidencias' ,
                    icon: '/assets/images/warning.png',
                    onClick: function () {
                        window.focus();
                        this.close();
                    }
                });
            } else {
                Push.create('Incidencia con robot ' + received_notifications[i].robot,{
                    body: received_notifications[i].message ,
                    icon: added,
                    onClick: function () {
                        window.focus();
                        this.close();
                    }
                });
            }
        }
        $('#number-notifications').empty()
        if (received_notifications.length == 1) {
            $('#number-notifications').append('Tienes 1 aviso')
        } else {
            $('#number-notifications').append('Tienes ' + received_notifications.length + ' avisos')
        }
        $('#heartbitDiv').empty()
        $('#heartbitDiv').append('<span class="heartbit"></span><span class="point"></span>')
    } else {
        $('#number-notifications').empty()
        $('#number-notifications').append('Tienes 0 avisos')
    }
}

var starCountRef = firebase.database().ref('notifications/read_status');
starCountRef.on('value', function (snapshot) {
    if (snapshot.val() !== 1) {
        firebase.database().ref('/notifications/unread').once('value').then(function (snapshot) {
            updateNotifications(snapshot.val())
        });
        read_status = 0
    }
});

$("#notify-bubble").on("click", function () {
    if (read_status !== 1) {
        firebase.database().ref('/notifications/read_status').set(1);
        $('#heartbitDiv').empty()
        read_status = 1
        if (unread_notifications !== null) {
            Object.keys(unread_notifications).forEach(function (key) {
                value = unread_notifications[key]
                firebase.database().ref('/notifications/unread/' + key).remove();
                firebase.database().ref('notifications/read').push({
                    date: value.date,
                    message: value.message,
                    robot: value.robot,
                    supervisor: value.supervisor,
                    type: value.type
                });
            });
            unread_notifications = null
        }
    }
})
