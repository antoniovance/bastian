$(document).ready(
    function () {
        if (!window.console) window.console = {};
        if (!window.console.log) window.console.log = function () {};

        //redefine submit event of message form
        //$("#messageform").live("submit", function () {
        //    newMessage($(this));
        //    return false;
        //});
        console.log('fuck');

        $("#messageform").submit(function () {
            console.log("jooooo");
            newMessage($(this));
            return false;
        });

        //redefine keypress event of message form
        $("#messageform").on("keypress", function (e) {
            if (e.keyCode==13){
                newMessage($(this));
                return false;
            }
        });

        $("#message").select();
        updater.start();
    }
);

function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function () {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++){
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json
};

var updater = {
    socket: null,
    start: function () {
        var url = "ws://" + location.host + "/chatsocket";
        updater.socket = new WebSocket(url);

        updater.socket.onmessage = function (event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },
    showMessage: function (message) {
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};