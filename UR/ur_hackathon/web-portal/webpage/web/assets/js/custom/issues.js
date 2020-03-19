$("#jsGrid").jsGrid({
    width: "100%",
    height: "600px",
    noDataContent: "No han habido incidencias",
    loadMessage: "Recopilando listado...",
    updateOnResize: true,
    loadIndication: true,
    editing: false,
    sorting: true,
    paging: true,
    autoload: true,
    pagePrevText: "Anterior",
    pageNextText: "Siguiente",
    pageFirstText: "Primera",
    pageLastText: "Ultima",

    controller: {
        loadData: function () {
            var d = $.Deferred();
            firebase.database().ref('/notifications/read').once('value').then(function (snapshot) {
                notifications = snapshot.val()
                var data = []
                if (notifications !== null) {
                    Object.keys(notifications).forEach(function (key) {
                        value = notifications[key]
                        var row = {}
                        row['Identificacion'] = key
                        row['Tipo'] = value.type
                        row['Robot'] = value.robot
                        row['Mensaje'] = value.message
                        row['Supervisor'] = value.supervisor
                        var date = new Date(value.date);
                        var seconds = date.getSeconds();
                        var minutes = date.getMinutes();
                        var hour = date.getHours();

                        var year = date.getFullYear();
                        var month = date.getMonth(); // beware: January = 0; February = 1, etc.
                        var day = date.getDate();
                        row['epoch'] = value.date
                        row['Hora'] = (hour < 10 ? ('0' + hour) : hour) + ':' + (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds)
                        row['Fecha'] = (day < 10 ? '0' + day : day) + '/' + (month < 10 ? '0' + month : month) + '/' + year
                        data.push(row)
                    });
                    data.sort(function (a, b) {
                        return b['epoch'] - a['epoch']
                    })
                }
                d.resolve(data);
            });
            return d.promise();
        }
    },
    fields: [
        {name: "Identificacion", type: "text"},
        {name: "Tipo", type: "text", itemTemplate: function(value, item) {
                switch (value) {
                    case 1216:
                    case 1536:
                        return $('<div style="text-align: center"><span class="label label-danger">Critico</span></div>');
                    case 1028:
                        return $('<div style="text-align: center"><span class="label label-warning">Advertencia</span></div>');
                    case 1:
                        return $('<div style="text-align: center"><span class="label label-success">Éxito</span></div>');
                    default:
                        return $('<div style="text-align: center"><span class="label label-info">Informativo</span></div>');
                }
            },
        },
        {name: "Robot", type: "text"},
        {name: "Mensaje", type: "text"},
        {name: "Supervisor", type: "text"},
        {name: "Hora", type: "text"},
        {name: "Fecha", type: "text"}
    ]
});



