# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from models import User, Game, Score
from models import (StringMessage, 
                    NewGameForm, 
                    GameForm, 
                    MakeMoveForm,
                    ScoreForms,
                    GameForms,
                    UserRankForms,
                    UserRankInfo,
                    GameHistory,
                    History,
                    HistoryForms)
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
HIGH_SCORE_REQUEST = endpoints.ResourceContainer(limitation=messages.IntegerField(1))
MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'

@endpoints.api(name='hangman', version='v1')
class HangmanApi(remote.Service):
    """Hangman Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            game = Game.new_game(user.key, request.word)
            GameHistory.new_game_history(game.key)
        except ValueError:
            raise endpoints.BadRequestException('Invalid word')

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Hangman!')
    @endpoints.method(request_message = GET_GAME_REQUEST,
                      response_message = GameForm,
                      path='cancel_game/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='POST')
    def cancel_game(self,request):
      """Cancel a game"""
      game = get_by_urlsafe(request.urlsafe_game_key, Game)
      print(game)
      if game.game_over:
        return game.to_form('Game already over!')

      if game:
        game.cancel_game()
        return game.to_form('Cancel game successfully')
      else:
        raise endpoints.NotFoundException('Game not found!')
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='games/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Return all avtive games under one specific user"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        games = Game.query(Game.user == user.key).filter(Game.game_over == False)
        return GameForms(items=[game.to_form('') for game in games])


    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')
        
        """Hangman Game Logic"""
        
        word = list(request.guess)[0]
        target = list(game.target)
        miss = list(game.miss)
        current = list(game.current)
        valid = False
        inMissList = False
        message = ''
        game_history = GameHistory.query(GameHistory.game == game.key).get()

        """Check whether the input word is in miss list"""
        for index,t in enumerate(miss):
            if t == word:
                inMissList = True
                game.attempts_remaining -= 1
                message = 'You already guessed that letter and it is not right! Try again, but a new one this time.'
                break
        

        """Check whether the input word is in target list"""
        for index,t in enumerate(target):
            if word == t:
                valid = True
                message = 'Correct!'
                current[index] = word
                break

        game.current = ''.join(current)

        """Update miss list"""
        if valid == False and inMissList == False:
            game.attempts_remaining -= 1
            miss.append(word)
            game.miss =''.join(miss)
            game.put()
            message = 'Nice try! But it is not a valid word'

        """Compare between current and target"""

        if game.attempts_remaining < 1:
            game_history.addHistory(valid,word,'lose')
            game.end_game(False)
            message = 'Game over!'
        else:
            if target == current:
                game.end_game(True)
                game_history.addHistory(valid,word,'win')
                message = 'You Win!'
            else:
                game_history.addHistory(valid,word,'pending') 
            game.put()

        return game.to_form(message)
    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])


    @endpoints.method(request_message = HIGH_SCORE_REQUEST,
                      response_message=ScoreForms,
                      path='high_scores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Return ordered high scores based on 1.more won 2.less guesses number"""
        qo = ndb.QueryOptions(limit=request.limitation)
        scoreQuery = Score.query().order(-Score.won,Score.guesses)
        scoreList = scoreQuery.fetch(10,options=qo)

        return ScoreForms(items=[score.to_form() for score in scoreList])

    @endpoints.method(response_message=UserRankForms,
                      path='user_rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self,request):
        """Return user rankings"""
        users = User.query()
        userRankInfoList = []
        if users == None:
            raise endpoints.NotFoundException(
                    'No existing users now')
        for user in users:
            winTime = 0
            totalTime = 0
            winRate = 0.0
            totalGuesses = 0
            scores = Score.query(Score.user == user.key)
            if scores != None:
                for score in scores:
                    totalTime = totalTime + 1
                    if score.won == True:
                        winTime = winTime + 1
                    totalGuesses += score.guesses
                if totalTime != 0:
                    winRate = winTime / float(totalTime)
                userRankInfo = UserRankInfo(user.name,
                                            winTime,
                                            winRate,
                                            totalGuesses)
                userRankInfoList.append(userRankInfo)
        userRankInfoList = sorted(userRankInfoList, key=lambda user: (user.winTime,user.winRate,-user.totalGuesses),reverse=True) 
        return UserRankForms(items=[userRank.to_form() for userRank in userRankInfoList])



    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=HistoryForms,
                      path='games/{urlsafe_game_key}/get_user_rankings',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self,request):
        """Return game history for a specific game"""
        game = get_by_urlsafe(request.urlsafe_game_key,Game)
        if not game:
            raise endpoints.NotFoundException('Game not found!')
        gameHistory = GameHistory.query(GameHistory.game == game.key).get()
        return HistoryForms(items=[history.to_form() for history in gameHistory.histories])

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                        for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([HangmanApi])
