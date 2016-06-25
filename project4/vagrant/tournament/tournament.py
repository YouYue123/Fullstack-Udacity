#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cmd = "UPDATE players SET wins=0,matches = 0"
    sql = "DELETE FROM matches"
    cursor.execute(cmd)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    sql = "DELETE FROM players"
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    sql = "SELECT count(*) as count FROM players"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    count = results[0][0]
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
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
    db = connect()
    cursor = db.cursor()
    cmd = "SELECT * FROM players order by wins"
    cursor.execute(cmd)
    results = cursor.fetchall()
    db.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cmd = "UPDATE players SET wins=wins+1,matches=matches+1 WHERE id = %s"
    cmd1 = "UPDATE players SET matches=matches+1 WHERE id = %s"
    cmd2 = "INSERT INTO matches(winner_id,loser_id) values(%s,%s)"
    cursor.execute(cmd,(winner,))
    cursor.execute(cmd1,(loser,))
    cursor.execute(cmd2,(winner,loser,))
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
    db = connect()
    cursor = db.cursor()
    cmd = "SELECT winner_id, loser_id FROM matches WHERE ((winner_id = %s AND loser_id = %s) OR (winner_id=%s AND loser_id = %s))"
    cursor.execute(cmd,(player1,player2,player2,player1,))
    results = cursor.rowcount
    db.close()
    if results > 0 :
        return False
    else:
        return True
