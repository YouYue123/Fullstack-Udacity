#Full Stack Nanodegree Project Design A Game

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 
 
 
##Game Description:
Guess a number is a simple guessing game. Each game begins with a random 'target'
number between the minimum and maximum values provided, and a maximum number of
'attempts'. 'Guesses' are sent to the `make_move` endpoint which will reply
with either: 'too low', 'too high', 'you win', or 'game over' (if the maximum
number of attempts is reached).
Many different Guess a Number games can be played by many different Users at any
given time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, word
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Also adds a task to a task queue to update the average moves remaining for active games.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
 
 - **get_user_games**
    - Path: 'games/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms. 
    - Description: Returns all active Games recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.
- **get_high_scores**
    - Path: 'high_scores'
    - Method: GET
    - Parameters: None
    - Returns: Ordered ScoreForms
    - Description: Return Ordered Score List. Higher Ranking is based on 1st factor(more winning times) and 2nd factor(less guesses number)

- **get_user_rankings**
    - Path: 'user_rankings'
    - Method: GET
    - Parameter: None
    - Return: UserRankForms
    - Description: Return Ordered user ranking list. Higher Ranking is based on 1st factor(more winning time) and 2nd factor(more winning rate) and 3rd factor(less total guesses)

- **get_game_history**
    - Path: 'games/{urlsafe_game_key}/get_user_rankings'
    - Method : GET
    - Parameter: urlsafe_game_key
    - Return : HistoryForms
    - Description: Return ordered game history based on moving step for a specific game.

##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.

 - **GameHistory**
    - Records game history data. Associated with Game model via KeyProperty.

 - **History**
    - Intermediate structure for history data used by GameHistory model

-  **UserRankInfo**
    - Information representation class for gathering information to ouput as user ranking information

##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name,miss,current).
 - **GameForms**
    - Multiple GameForm container
 - **NewGameForm**
    - Used to create a new game (user_name,word)
 - **MakeMoveForm**
    - Inbound make move form (guess).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.

 - **HistoryForm**
    - Used to create a new history step(guess,hitStatus)
 - **HistoryForms**
    - Multitple HistoryForm container
 - **UserRankForm**
    - Used to create a user rank information form(name,win_time,win_rate,total_guesses)
 - **UserRankForms**
    - Multiple UserRankForm container
