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
    sql = """
          DELETE FROM match;
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    # why does this version of psycopg2 not have context managers for
    # connections???


def deletePlayers():
    """Remove all the player records from the database."""
    sql = """
          DELETE FROM player;
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    sql = """
          SELECT COUNT(*)
          FROM player;
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    retval = cur.fetchall()
    cur.close()
    conn.close()
    if retval:
        return retval[0][0]
    else:
        return


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    sql = """
          INSERT INTO player (name) VALUES (%s);
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (name,))
    cur.close()
    conn.commit()
    conn.close()


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
    sql = """
          SELECT player.player_id, player.name,
                 player_wins.wins_cnt, player_matches.matches_cnt
          FROM player
          LEFT JOIN player_wins ON player.player_id = player_wins.player_id
          LEFT JOIN player_matches on player.player_id = player_matches.player_id
          ORDER BY player_wins.wins_cnt;
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    retval = cur.fetchall()
    print retval
    cur.close()
    conn.close()
    return retval


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql = """
          INSERT INTO match (winner_id, loser_id) VALUES (%s, %s);
          """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (winner, loser))
    cur.close()
    conn.commit()
    conn.close()


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
    standings = playerStandings()
    pairings = []

    if len(standings) % 2 == 1:
        raise ValueError("An uneven number of players are registered!")

    # Returns player pairing tuples based presorted results of sql query
    for i in xrange(0, len(standings), 2):
        pairings.append((standings[i][0], standings[i][1],
                         standings[i+1][0], standings[i][1]))

    return pairings
