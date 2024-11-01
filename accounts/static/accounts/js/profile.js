const joinDateElement = document.getElementById("join_date")
const rpsWinLoseElement = document.getElementById("rps_win_lose");

let username = JSON.parse(document.getElementById("username").textContent);
console.log("username: " + username.toString())

const socket = new WebSocket("ws://" + window.location.host + "/ws/profile/" + username + "/");

// socket.onmessage() = function(event)
socket.addEventListener("message", function (event)
{
    const data = JSON.parse(event.data);
    console.log(data);
    if (data.error == 'error')
    {
        alert("该用户不存在")
        return ;
    }
    joinDateElement.textContent = `${data.join_date} 加入`
    rpsWinLoseElement.textContent = `胜/负: ${data.rps_win}/${data.rps_lose}`
})