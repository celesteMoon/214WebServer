const statusElement = document.getElementById('status');
const choicesElement = document.getElementById('choices_div');
const timerElement = document.getElementById('timer');
const scoreElement = document.getElementById('score');
const selfChoiceElement = document.getElementById('emoji_left');
const oppenentChoiceElement = document.getElementById('emoji_right');
const opponentNameElement = document.getElementById('name_right');
let gameId = JSON.parse(document.getElementById('game-id').textContent);
console.log('gameId: ' + gameId.toString())

const socket = new WebSocket('ws://' + window.location.host + '/ws/game/' + gameId + '/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("status:"+data.status);
    if (data.status === 'waiting') {
        statusElement.textContent = '状态：' + data.status;
    }
    else if (data.status === 'game_start') {
        opponentNameElement.textContent = data.opponent_name;
        gameId = data.game_id.toString();
        console.log("gameid: "+gameId);
    }
    else if (data.status === 'round_start') {
        oppenentChoiceElement.textContent = "❔";
        selfChoiceElement.textContent = "❔";
        var countdown = 3;
        function updTimer() {
            timerElement.textContent = `${countdown}`;
            countdown -= 1;
            if (countdown < 0) {
                clearInterval(interval); // 停止倒计时
                timerElement.textContent = "";
            }
            return updTimer;
        }
        var interval = setInterval(updTimer(), 1000); // 每秒更新一次

        var timeout = setTimeout(function(){
            choicesElement.style.display = 'flex'; // 显示选项
            scoreElement.textContent = data.self_score + ':' + data.opponent_score;
        }, 3000);
    }
    else if (data.status === 'round_end') {
        if (data.opponent_choice == "rock") oppenentChoiceElement.textContent = "🪨";
        else if (data.opponent_choice == "scissors") oppenentChoiceElement.textContent = "✂️";
        else if (data.opponent_choice == "paper") oppenentChoiceElement.textContent = "📃";
        scoreElement.textContent = data.self_score + ':' + data.opponent_score;
        statusElement.textContent = '你的选择：' + data.your_choice + '，对手选择：' + data.opponent_choice + '，结果：' + data.result;
        choicesElement.style.display = 'none'; // 隐藏选项

        let countdown = 3;
        function updTimer() {
            timerElement.textContent = `${countdown}`;
            countdown -= 1;
            if (countdown < 0) {
                clearInterval(interval); // 停止倒计时
                timerElement.textContent = "";
                // window.location.reload(); // 刷新页面
            }
            return updTimer;
        }
        const interval = setInterval(updTimer(), 1000); // 每秒更新一次
    }
};

function makeChoice(choice) {
    if (choice == "rock") selfChoiceElement.textContent = "🪨";
    else if (choice == "scissors") selfChoiceElement.textContent = "✂️";
    else if (choice == "paper") selfChoiceElement.textContent = "📃";
    socket.send(JSON.stringify({
        'status': 'choice',
        'game_id': gameId,
        'choice': choice
    }));
}