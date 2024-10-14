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
    
    async def connect(self):
        # functions inside function
        async def ready():
            pass

        async def round_start():
            pass

        # main
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
            # game_id = 'truckduckpluck'  # 创建唯一的游戏 ID

            RPSConsumer.games[game_id] = {
                'players': [self, opponent],
                'choices': {},
                'scores': [0, 0],
            }

            # 保存游戏状态
            async with games_lock:
                RPSConsumer.games[game_id] = {
                    'players': [self, opponent],
                    'choices': {},
                    'scores': [0, 0],
                }
            
            # 通知两个玩家游戏开始
            await self.send(text_data=json.dumps({
                'status': 'ready',
                'self_name': self.username,
                'opponent_name': opponent.username,
                'game_id': game_id
            }))
            await opponent.send(text_data=json.dumps({
                'status': 'ready',
                'self_name': opponent.username,
                'opponent_name': self.username,
                'game_id': game_id
            }))

            await asyncio.sleep(3) # wait 3 seconds to start the game

            await self.send(text_data=json.dumps({
                'status': 'round_start',
                'self_name': self.username,
                'opponent_name': opponent.username,
                'game_id': game_id
            }))
            await opponent.send(text_data=json.dumps({
                'status': 'round_start',
                'self_name': opponent.username,
                'opponent_name': self.username,
                'game_id': game_id
            }))

        
    async def receive(self, text_data):
        data = json.loads(text_data)
        game_id = data.get('game_id')
        status = data.get('status')
        game = RPSConsumer.games[game_id]

        if status == 'choice':
            logger.info("gameid: "+str(game_id))
            choice = data.get('choice')
            game['choices'][self.username] = choice
        
        # 保存玩家选择
        # async with games_lock:
            # game = RPSConsumer.games[game_id]
            # game['choices'][self.username] = choice

        await asyncio.sleep(5) # wait 5 seconds to see the results for this round
        if True:
        # if len(game['choices']) == 2:
            

            # calc results for this round


            # async with games_lock:
            #     game = RPSConsumer.games[game_id]


            # 获取双方的选择
            player1, player2 = game['players']
            choice1 = 'rock'
            choice2 = 'paper'
            # async with games_lock:
            if game['choices'][player1.username] is None:
                choice1 = 'fuck'
            else:
                choice1 = game['choices'][player1.username]
            if game['choices'][player2.username] is None:
                choice2 = 'fuck'
            else:
                choice2 = game['choices'][player2.username]
            
            # scores
            self_score, opponent_score = game['scores']

            # 判断结果
            result = self.judge_winner(player1.username, choice1, player2.username, choice2)
            
            # 通知双方结果
            async with games_lock:
                await player1.send(text_data=json.dumps({
                    'status': 'round_end',
                    'your_choice': choice1,
                    # 'self_score': RPSConsumer.games[game_id]['scores'][0],
                    'opponent_choice': choice2,
                    # 'opponent_score': RPSConsumer.games[game_id]['scores'][1],
                    'result': result[player1.username]
                }))
                await player2.send(text_data=json.dumps({
                    'status': 'round_end',
                    'your_choice': choice2,
                    # 'self_score': RPSConsumer.games[game_id]['scores'][1],
                    'opponent_choice': choice1,
                    # 'opponent_score': RPSConsumer.games[game_id]['scores'][0],
                    'result': result[player2.username]
                }))
            
            # 删除游戏记录
            del RPSConsumer.games[game_id]
            # break

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
