const socket = new WebSocket("ws://" + window.location.host + "/ws/setting/");

socket.addEventListener("message", function (event)
{

})

function saveChanges(value)
{
    socket.send(JSON.stringify({
        "background_color": value
    }));
    location.reload();
}