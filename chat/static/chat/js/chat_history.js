function resizeChatHistory() {
    document.getElementById('chat-log').style.height = (window.innerHeight - 250).toString() + 'px';
}

// toBottom() when: 1.send msg 2.todo: received msg when the scroll is at the bottom 3.todo: click 'newmsg' button
function toBottom() {
    var container = document.querySelector('#chat-log');
    container.scrollTop = container.scrollHeight;
}