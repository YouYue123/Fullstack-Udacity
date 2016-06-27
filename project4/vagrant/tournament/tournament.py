#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:
    def __init__(self,db_con_str="dbname=tournament"):
        """
        Create a database connection
        :param str db_con_str: dataname
        """
        self.conn = psycopg2.connect(db_con_str)
    
    def cursor(self):
        """
        Return the current cursor of database
        """
        return self.conn.cursor()

    def execute(self,self_query_string,and_close=False):
        """
        Execute sql command
        :param str self_query_string: sql command
        :param bool and_close: if true,close database after executing and commiting
        """
        cursor = self.cursor()
        cursor.execute(self_query_string)
        if and_close:
            self.conn.commit()
            self.conn.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

def deleteMatches():
    """Remove all the match records from the database."""
    cmd = "DELETE FROM matches"
    DB().execute(cmd,True)
    return

def deletePlayers():
    """Remove all the player records from the database."""
    cmd = "DELETE FROM players"
    DB().execute(cmd,True)
    return

def countPlayers():
    """Returns the number of players currently registered."""
    cmd = "SELECT count(*) FROM players"
    conn = DB().execute(cmd,False)
    cursor = conn["cursor"].fetchone()
    conn['conn'].close()
    return cursor[0] 

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = DB().conn
    cursor = db.cursor()
    cmd = "INSERT INTO players(name) values(%s)"
    cursor.execute(cmd,(name,))
    db.commit()
    db.close()
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cmd = "SELECT * FROM v_matches order by wins"
    conn = DB().execute(cmd,False)
    results = conn["cursor"].fetchall()
    conn['conn'].close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = DB().conn
    cursor = db.cursor()
    cmd = "INSERT INTO matches(winner_id,loser_id) values(%s,%s)"
    cursor.execute(cmd,(winner,loser,))
    db.commit()
    db.close()
    return

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    
    players = playerStandings()
    ##at least two players
    while len(players) > 1 :
        validMatch = checkPairs(players)
        player1 = players.pop(0)
        player2 = players.pop(validMatch - 1)
        pairs.append((player1[0],player1[1],player2[0],player2[1]))
    return pairs

def checkPairs(players):
    """Return Valid Rival's position
    Args:
        players: players list

    Returns:
        the position of a valid rival 
    """
    result = 0
    standPlayer = players[0]
    for index,player in enumerate(players):
        if index == 0:
            continue
        if index >= len(players):
            return 1
        if player[2] == standPlayer[2]:
            if checkRematch(player[0],standPlayer[0]):
                result = index

    return result



def checkRematch(player1,player2):
    """Check whether two players has already been matched previously 
    Args:
        player1: id of player1
        player2: id of player2
    Returns:
        the rematch status of these two players
    """
    db = DB().conn
    cursor = db.cursor()
    cmd = "SELECT winner_id, loser_id FROM matches WHERE ((winner_id = %s AND loser_id = %s) OR (winner_id=%s AND loser_id = %s))"
    cursor.execute(cmd,(player1,player2,player2,player1,))
    results = cursor.rowcount
    db.close()
    if results > 0 :
        return False
    else:
        return True
