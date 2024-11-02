from channels.generic.websocket import AsyncWebsocketConsumer
import json, logging

from channels.db import database_sync_to_async

logger = logging.getLogger('rps/consumers.py')

class RPSConsumer(AsyncWebsocketConsumer):
    games = {}  # 正在进行的游戏
    
    async def connect(self):
        self.username = self.scope["user"].username

        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_id_name = 'game_%s' % self.game_id

        # 将当前频道加入频道组
        await self.channel_layer.group_add(
            self.game_id_name,
            self.channel_name
        )
        await self.accept()

        if not self.game_id in RPSConsumer.games:
            RPSConsumer.games[self.game_id] = {
                'players': [self],
            }
            await self.send(text_data=json.dumps({
                'status': 'waiting'
            }))

        elif len(RPSConsumer.games[self.game_id]['players']) == 1:
            opponent = RPSConsumer.games[self.game_id]['players'][0]
            # game_id = str(uuid.uuid4())  # 创建唯一的游戏 ID
            game_id = self.game_id

            # 保存游戏状态
            RPSConsumer.games[game_id] = {
                'players': [self, opponent],
                'spectators': [],
                'choices': {},
                'scores': {self.username: 0, opponent.username: 0},
            }

            await self.status_game_start(self, opponent, game_id)
            await self.status_round_start(self, opponent, game_id)

        elif len(RPSConsumer.games[self.game_id]['players']) >= 2:
            RPSConsumer.games[self.game_id]['spectators'].append(self)
            # await self.status_update_spectator
            player1, player2 = RPSConsumer.games[self.game_id]['players']
            await self.send(text_data=json.dumps({
                'status': 'spectate_start',
                'p1_name': player1.username,
                'p1_score': RPSConsumer.games[self.game_id]['scores'][player1.username],
                'p2_name': player2.username,
                'p2_score': RPSConsumer.games[self.game_id]['scores'][player2.username],
                'game_id': self.game_id
            }))

    async def disconnect(self, close_code):
        if self.game_id in RPSConsumer.games:
            if 'spectators' in RPSConsumer.games[self.game_id]:
                if self in RPSConsumer.games[self.game_id]['spectators']:
                    RPSConsumer.games[self.game_id]['spectators'].remove(self)
            if 'players' in RPSConsumer.games[self.game_id]:
                if self in RPSConsumer.games[self.game_id]['players']:
                    del RPSConsumer.games[self.game_id]
        await self.channel_layer.group_discard(
            self.game_id_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        game_id = data.get('game_id')
        status = data.get('status')
        game = RPSConsumer.games[game_id]

        if status == 'choice':
            choice = data.get('choice')
            game['choices'][self.username] = choice
        
        if len(game['choices']) == 2:
            # 获取双方的选择
            player1, player2 = game['players']
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

            if RPSConsumer.games[game_id]['scores'][player1.username] == 3:
                # logger.info(player1.username + ' wins')
                player1.scope["user"].stats_rps_win += 1
                player2.scope["user"].stats_rps_lose += 1
                await self.db_save(player1, player2)
            if RPSConsumer.games[game_id]['scores'][player2.username] == 3:
                # logger.info(player2.username + ' wins')
                player1.scope["user"].stats_rps_lose += 1
                player2.scope["user"].stats_rps_win += 1
                await self.db_save(player1, player2)
            # 通知双方结果
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
            # broadcast to spectators
            await self.status_update_spectator(text_data=json.dumps({
                'status': 'spectate_update',
                'p1_name': player1.username,
                'p1_choice': choice1,
                'p1_score': RPSConsumer.games[self.game_id]['scores'][player1.username],
                'p2_name': player2.username,
                'p2_choice': choice2,
                'p2_score': RPSConsumer.games[self.game_id]['scores'][player2.username],
                'game_id': self.game_id,
                'p1_win': player1.scope["user"].stats_rps_win,
                'p1_lose': player1.scope["user"].stats_rps_lose,
                'p2_win': player2.scope["user"].stats_rps_win,
                'p2_lose': player2.scope["user"].stats_rps_lose,
            }))
            
            if max(RPSConsumer.games[game_id]['scores'][player1.username], RPSConsumer.games[game_id]['scores'][player2.username]) == 3:
                # logger.info(player1.username + str(player1.scope["user"].stats_rps_win) + '/' + str(player1.scope["user"].stats_rps_lose))
                # logger.info(player2.username + str(player2.scope["user"].stats_rps_win) + '/' + str(player2.scope["user"].stats_rps_lose))
                del RPSConsumer.games[game_id]
            else:
                game['choices'] = {}
                await self.status_round_start(player1, player2, game_id)

    #
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

    async def status_update_spectator(self, text_data):
        await self.channel_layer.group_send(
            self.game_id_name, 
            {
                'type': 'spectate_update',
                'text': text_data
            }
        )

    async def spectate_update(self, event):
        await self.send(text_data=event['text'])

    @database_sync_to_async
    def db_save(self, p1, p2):
        p1.scope["user"].save()
        p2.scope["user"].save()

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

    
