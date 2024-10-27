const statusElement = document.getElementById('status');
const choicesElement = document.getElementById('choices_div');
const timerElement = document.getElementById('timer');
const scoreElement = document.getElementById('score');
const selfChoiceElement = document.getElementById('emoji_left');
const opponentChoiceElement = document.getElementById('emoji_right');
const selfNameElement = document.getElementById('name_left');
const opponentNameElement = document.getElementById('name_right');
var isPlayer = false;
let gameId = JSON.parse(document.getElementById('game-id').textContent);
console.log('gameId: ' + gameId.toString())

const socket = new WebSocket('ws://' + window.location.host + '/ws/game/' + gameId + '/');

socket.onmessage = function(event)
{
    const data = JSON.parse(event.data);
    console.log(data);
    if (data.status === 'waiting')
    {
        statusElement.textContent = '状态：' + data.status;
    }
    else if (data.status === 'game_start')
    {
        opponentNameElement.textContent = data.opponent_name;
        gameId = data.game_id.toString();
        console.log("gameid: "+gameId);
        isPlayer = true;
    }
    else if (data.status === 'round_start')
    {
        countdown(3);
        delay(function(){
            choicesElement.style.display = 'flex'; // 显示选项
            scoreElement.textContent = data.self_score + ':' + data.opponent_score;
            opponentChoiceElement.textContent = "❔";
            selfChoiceElement.textContent = "❔";
        }, 3)
    }
    else if (data.status === 'round_end')
    {
        if (data.opponent_choice == "rock") opponentChoiceElement.textContent = "🪨";
        else if (data.opponent_choice == "scissors") opponentChoiceElement.textContent = "✂️";
        else if (data.opponent_choice == "paper") opponentChoiceElement.textContent = "📃";
        scoreElement.textContent = data.self_score + ':' + data.opponent_score;
        statusElement.textContent = '你的选择：' + data.your_choice + '，对手选择：' + data.opponent_choice + '，结果：' + data.result;
        choicesElement.style.display = 'none'; // 隐藏选项

        if (Math.max(data.self_score, data.opponent_score) == 3)
        {
            if (data.self_score == 3) selfNameElement.textContent += '👑';
            if (data.opponent_score == 3) opponentNameElement.textContent += '👑';
        }
    }
    else if (data.status === 'spectate_start')
    {
        if (isPlayer) return ;
        statusElement.textContent = '这里满员了, 你现在是旁观者模式!';
        selfNameElement.textContent = data.p1_name;
        opponentNameElement.textContent = data.p2_name;
        selfChoiceElement.textContent = "❔";
        opponentChoiceElement.textContent = "❔";
        scoreElement.textContent = data.p1_score + ':' + data.p2_score;
    }
    else if (data.status === 'spectate_update')
    {
        if (isPlayer) return ;
        selfNameElement.textContent = data.p1_name;
        opponentNameElement.textContent = data.p2_name;
        if (data.p1_choice == "rock") selfChoiceElement.textContent = "🪨";
        else if (data.p1_choice == "scissors") selfChoiceElement.textContent = "✂️";
        else if (data.p1_choice == "paper") selfChoiceElement.textContent = "📃";
        if (data.p2_choice == "rock") opponentChoiceElement.textContent = "🪨";
        else if (data.p2_choice == "scissors") opponentChoiceElement.textContent = "✂️";
        else if (data.p2_choice == "paper") opponentChoiceElement.textContent = "📃";
        scoreElement.textContent = data.p1_score + ':' + data.p2_score;

        if (Math.max(data.p1_score, data.p2_score) == 3)
        {
            if (data.p1_score == 3) selfNameElement.textContent += '👑';
            if (data.p2_score == 3) opponentNameElement.textContent += '👑';
        }
        else
        {
            countdown(3);
            delay(function(){
                opponentChoiceElement.textContent = "❔";
                selfChoiceElement.textContent = "❔";
            }, 3)
        }
    }
}

function makeChoice(choice)
{
    if (choice == "rock") selfChoiceElement.textContent = "🪨";
    else if (choice == "scissors") selfChoiceElement.textContent = "✂️";
    else if (choice == "paper") selfChoiceElement.textContent = "📃";
    socket.send(JSON.stringify({
        'status': 'choice',
        'game_id': gameId,
        'choice': choice
    }));
}

function countdown(cd)
{
    var countdownTimer = cd;
        function updTimer()
        {
            timerElement.textContent = `${countdownTimer}`;
            countdownTimer -= 1;
            if (countdownTimer < 0)
            {
                clearInterval(interval); // 停止倒计时
                timerElement.textContent = "";
            }
            return updTimer;
        }
        var interval = setInterval(updTimer(), 1000); // 每秒更新一次
}

function delay(Func, delayTime)
{
    var timeout = setTimeout(function(){Func(); }, delayTime * 1000);
}