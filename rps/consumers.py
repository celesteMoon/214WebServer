from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import logging
import uuid

logger = logging.getLogger('django')

games_lock = asyncio.Lock() # lock

class RPSConsumer(AsyncWebsocketConsumer):
    waiting_players = []  # 等待匹配的玩家
    games = {}  # 正在进行的游戏
    
    async def status_game_start(self, p1, p2, game_id):
        await p1.send(text_data=json.dumps({
            'status': 'game_start',
            'self_name': p1.username,
            'self_score': RPSConsumer.games[game_id]['scores'][p1.username],
            'opponent_name': p2.username,
            'opponent_score': RPSConsumer.games[game_id]['scores'][p2.username],
            'game_id': game_id
        }))
        await p2.send(text_data=json.dumps({
            'status': 'game_start',
            'self_name': p2.username,
            'self_score': RPSConsumer.games[game_id]['scores'][p2.username],
            'opponent_name': p1.username,
            'opponent_score': RPSConsumer.games[game_id]['scores'][p1.username],
            'game_id': game_id
        }))

    async def status_round_start(self, p1, p2, game_id):
        await p1.send(text_data=json.dumps({
            'status': 'round_start',
            'self_name': p1.username,
            'self_score': RPSConsumer.games[game_id]['scores'][p1.username],
            'opponent_name': p2.username,
            'opponent_score': RPSConsumer.games[game_id]['scores'][p2.username],
            'game_id': game_id
        }))
        await p2.send(text_data=json.dumps({
            'status': 'round_start',
            'self_name': p2.username,
            'self_score': RPSConsumer.games[game_id]['scores'][p2.username],
            'opponent_name': p1.username,
            'opponent_score': RPSConsumer.games[game_id]['scores'][p1.username],
            'game_id': game_id
        }))

    async def connect(self):
        self.username = self.scope["user"].username
        await self.accept()
        
        if not RPSConsumer.waiting_players:
            # 没有等待的玩家，添加当前用户到等待列表
            RPSConsumer.waiting_players.append(self)
            await self.send(text_data=json.dumps({
                'status': 'waiting'
            }))
        else:
            # 匹配到另一个等待的玩家
            opponent = RPSConsumer.waiting_players.pop(0)
            game_id = str(uuid.uuid4())  # 创建唯一的游戏 ID

            # 保存游戏状态
            async with games_lock:
                RPSConsumer.games[game_id] = {
                    'players': [self, opponent],
                    'choices': {},
                    'scores': {self.username: 0, opponent.username: 0},
                }

            await self.status_game_start(self, opponent, game_id)
            await self.status_round_start(self, opponent, game_id)

        
    async def receive(self, text_data):
        data = json.loads(text_data)
        game_id = data.get('game_id')
        status = data.get('status')
        game = RPSConsumer.games[game_id]

        if status == 'choice':
            choice = data.get('choice')
            game['choices'][self.username] = choice
        
        # 保存玩家选择
        # async with games_lock:
            # game = RPSConsumer.games[game_id]
            # game['choices'][self.username] = choice

        # await asyncio.sleep(5) # wait 5 seconds to see the results for this round

        # if True:
        if len(game['choices']) == 2:
            # async with games_lock:
            #     game = RPSConsumer.games[game_id]

            # 获取双方的选择
            player1, player2 = game['players']
            # async with games_lock:
            if game['choices'][player1.username] is None:
                choice1 = 'fuck'
            else:
                choice1 = game['choices'][player1.username]
            if game['choices'][player2.username] is None:
                choice2 = 'fuck'
            else:
                choice2 = game['choices'][player2.username]

            # 判断结果
            result = self.judge_winner(player1.username, choice1, player2.username, choice2)
            if result[player1.username] == 'win':
                RPSConsumer.games[game_id]['scores'][player1.username] += 1
            if result[player2.username] == 'win':
                RPSConsumer.games[game_id]['scores'][player2.username] += 1
            # 通知双方结果
            async with games_lock:
                await player1.send(text_data=json.dumps({
                    'status': 'round_end',
                    'your_choice': choice1,
                    'self_score': RPSConsumer.games[game_id]['scores'][player1.username],
                    'opponent_choice': choice2,
                    'opponent_score': RPSConsumer.games[game_id]['scores'][player2.username],
                    'result': result[player1.username]
                }))
                await player2.send(text_data=json.dumps({
                    'status': 'round_end',
                    'your_choice': choice2,
                    'self_score': RPSConsumer.games[game_id]['scores'][player2.username],
                    'opponent_choice': choice1,
                    'opponent_score': RPSConsumer.games[game_id]['scores'][player1.username],
                    'result': result[player2.username]
                }))
            
            if max(RPSConsumer.games[game_id]['scores'][player1.username], RPSConsumer.games[game_id]['scores'][player2.username]) == 3:
                # 删除游戏记录
                del RPSConsumer.games[game_id]
            else:
                game['choices'] = {}
                await self.status_round_start(player1, player2, game_id)

    def judge_winner(self, player1, choice1, player2, choice2):
        outcomes = {
            ('rock', 'scissors'): 'win',
            ('scissors', 'paper'): 'win',
            ('paper', 'rock'): 'win',
        }

        if choice1 == choice2:
            return {player1: 'draw', player2: 'draw'}
        elif (choice1, choice2) in outcomes:
            return {player1: 'win', player2: 'lose'}
        else:
            return {player1: 'lose', player2: 'win'}

    async def disconnect(self, close_code):
        if self in RPSConsumer.waiting_players:
            RPSConsumer.waiting_players.remove(self)
