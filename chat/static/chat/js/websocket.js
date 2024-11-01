const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

var toBottomFlag = false;

chatSocket.onmessage = function(e) {
    
    const data = JSON.parse(e.data);

    if (data.type === 'user_list') {
        updateOnlineUserList(data.users);
        return ;
    }
    // var container = document.querySelector('#chat-log');
    // console.log(container.scrollTop);
    // console.log(container.scrollHeight);
    // console.log(container.clientHeight);
    // if (container.scrollTop + container.clientHeight == container.scrollHeight) toBottomFlag = true;

    const chatLog = document.getElementById('chat-log');
    var HTMLdisplay = `
    <p class="message" style="display: flex; flex-direction: row;">
        <span class="time-container">
            <small class="local-time"> ${data.time_short} </small>
            <span class="tooltip">
                ${data.time_local} <br>
                ${data.time_UTC}
            </span>
        </span>
        &nbsp;
        <script type="text/template" style="display: block;">
            ${data.username} : ${data.message}
        </script>
    </p>
    `
    chatLog.innerHTML += HTMLdisplay;
    // chatLog.innerHTML += '<p class="message">\n'
    // + '<span class="time-container">\n'
    // + '<small class="local-time">' + data.time_short + '</small>\n'
    // + '<span class="tooltip">\n'
    // + data.time_local + ' <br>\n'
    // + data.time_UTC + '\n'
    // + '</span>\n' + '</span>\n'
    // + '<pre>'
    // + data.username + ': ' + data.message
    // + '</pre>'
    // + '</p>'
    
    updTimeTooltip();
    if (toBottomFlag) toBottom(), toBottomFlag = false;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.getElementById('chat-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInputDom = document.getElementById('message-input');
    var message = messageInputDom.value;
    message = message.replace('\n', ' ');
    if (message.replace(' ', '') == '') return ;
    const username = document.getElementById('username').value;
    chatSocket.send(JSON.stringify({
        'type': 'msg',
        'message': message,
        'username': username
    }));
    messageInputDom.value = '';
    toBottomFlag = true;
};

// document.getElementById('cd_button').onclick = function(e) {
//     e.preventDefault();
//     const username = document.getElementById('username').value;
//     chatSocket.send(JSON.stringify({
//         'type': 'countdown',
//         'username': username
//     }));
// };

function updateOnlineUserList(users) {
    const userListElement = document.getElementById('online-users');
    user_count = users.length;
    userListElement.innerHTML = `<small>在线用户 (${user_count}): </small>`; // 清空现有列表
    users.forEach(user => {
        const li = document.createElement('small');
        li.textContent = user + ' ';
        userListElement.appendChild(li);
    });
}