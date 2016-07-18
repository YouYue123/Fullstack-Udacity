"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
# import enchant
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb
# d = enchant.Dict("en_US")

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()

class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(required=True)
    miss = ndb.StringProperty(default='')
    current = ndb.StringProperty(default='')
    attempts_remaining = ndb.IntegerProperty(required=True, default=7)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    canceled = ndb.BooleanProperty(default=False)

    @classmethod
    def new_game(cls, user, word):
        """Creates and returns a new game"""
        # if d.check(word) is False:
        #     raise ValueError('Invalid Word in U.S English')
        current = []
        for t in list(word):
            current.append('_')

        game = Game(user=user,target=word,current=''.join(current))
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.current = self.current
        form.miss = self.miss
        form.canceled = self.canceled
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses= 7 - self.attempts_remaining)
        score.put()

    def cancel_game(self):
        self.game_over = True
        self.canceled = True
        self.put()


class History(ndb.Model):
    hitStatus = ndb.BooleanProperty(required=True)
    guesses = ndb.StringProperty(required=True)
    def to_form(self):
        return HistoryForm(guess=self.guesses,hitStatus=self.hitStatus)

class GameHistory(ndb.Model):
    game = ndb.KeyProperty(required=True,kind='Game')
    histories = ndb.StructuredProperty(History,repeated=True)
    @classmethod
    def new_game_history(cls,game):
        new_game_history = GameHistory(game=game,histories=[])
        new_game_history.put()

    def addHistory(self,hitStatus,guesses):
        history = History(hitStatus = hitStatus,guesses = guesses)
        self.histories.append(history)
        self.put()

class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)

class UserRankInfo():
    name = ""
    winTime = 0
    winRate = 0.0
    totalGuesses = 0
    def __init__(self,name,winTime,winRate,totalGussess):
        self.name = name
        self.winTime = winTime
        self.winRate = winRate
        self.totalGuesses = totalGussess
    def to_form(self):
        return UserRankForm(name=self.name,
                            win_time =self.winTime,
                            win_rate = self.winRate,
                            total_guesses=self.totalGuesses)

class HistoryForm(messages.Message):
    guess = messages.StringField(1,required=True)
    hitStatus = messages.BooleanField(2,required=True)

class HistoryForms(messages.Message):
    items = messages.MessageField(HistoryForm,1,repeated=True)

class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    miss = messages.StringField(6,required=True)
    current = messages.StringField(7,required= True)
    canceled = messages.BooleanField(8,required = True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    word = messages.StringField(2,required=True)

class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""

    guess = messages.StringField(1,required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)
    
class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm,1,repeated=True)

class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)
class UserRankForm(messages.Message):
    """Return user rank info with their winning time and average winning attempts"""
    name = messages.StringField(1,required=True)
    win_time = messages.IntegerField(2,required=True)
    win_rate = messages.FloatField(3,required=True)
    total_guesses = messages.IntegerField(4,required=True)

class UserRankForms(messages.Message):
    """Return multiple user rank info with their winning time and average winning attempts"""
    items = messages.MessageField(UserRankForm,1,repeated=True)
class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
