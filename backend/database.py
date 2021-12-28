import sqlite3
import os
import time
from typing import Tuple, Dict, List

database_path = "db/data.db"

class DB:
    def __init__(self, root_path) -> None:
        self.root_path = root_path

    def get_connection(self):
        return sqlite3.connect(os.path.join(self.root_path, database_path))

    def start_game(self, user):
        if not self.get_user(user):
            return (409, "User does not exist")
        
        con = self.get_connection()
        with con:
            try:
                c = con.execute("INSERT INTO game VALUES (?)", (int(time.time()*1000),))
                return (200, c.lastrowid)
            except sqlite3.Error as e:
                return (500,e.args[0])

    def join_game(self, user, game):
        if not self.get_user(user)[1]:
            return (409, "User does not exist")
        if not self.get_game(game)[1]:
            return (409, "Game does not exist")
        if user in self.get_game(game)[1]["players"]:
            return (409, "Player already in game")

        con = self.get_connection()
        with con:
            try:
                con.execute("INSERT INTO game_user VALUES (?,?)", (game, user))
                return (200,"")
            except sqlite3.Error as e:
                return (500,e.args[0])


    def get_game(self, game) -> Tuple[int, str | object]:
        con = self.get_connection()
        with con:
            cur = con.cursor()
            r = None
            try:
                if game:
                    r = cur.execute("SELECT date FROM game WHERE rowid=?", (game,))
                    g = r.fetchone()
                    if not g:
                        return (200, "")
                    r = cur.execute("SELECT user_id FROM game_user WHERE game_id=?", (game,))
                    o = {"time":g[0], "players":list(map(lambda x: x[0], r))}
                    return (200, o)
                else:
                    r = cur.execute("SELECT rowid, date FROM game")
                    return (200, {x[0]:x[1] for x in r})
            except sqlite3.Error as e:
                return (500,e.args[0])


    def add_user(self, name, password, pretty_name) -> tuple[int,str]:

        if self.get_user(name):
            return (409, "User already exists.")

        con = self.get_connection()
        with con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO users VALUES (?, ?, ?)", (name, password, pretty_name))
                return (200,"")
            except sqlite3.Error as e:
                return (500,e.args[0])

    def get_user(self, name : str=None) -> Dict[int, str | Dict[str, List]]:
        con = self.get_connection()
        with con:
            cur = con.cursor()
            r = []
            try:
                if not name:
                    r = cur.execute("SELECT name, rowid, pretty_name FROM users")
                else:
                    r = cur.execute("SELECT name, rowid, pretty_name FROM users WHERE rowid=?", (name,))
                out = {x[0]:[x[1], x[2]] for x in r}
                return (200,out)
            except sqlite3.Error as e:
                return (500,e.args[0])


    def create_tables(self) -> None:
        con = self.get_connection()
        with con:
            TABLES = [
                "CREATE TABLE users (name text, password text, pretty_name text)",
                "CREATE TABLE contracts (name text, content text)",
                "CREATE TABLE contract_rel (contract_id integer, user_id integer)",
                "CREATE TABLE game (date NUMERIC)",
                "CREATE TABLE game_user (game_id integer, user_id integer)"
                ]
            error = False
            for t in TABLES:
                print(t)
                try:
                    con.execute(t)
                except sqlite3.Error as e:
                    print("An error occurred:\n\t", e.args[0])
                    error = True
            if error:
                print("One or more errors occurred, not committing!")
                con.rollback()
                return "One or more errors occurred, not committing!"
            else:
                con.commit()
                return "Committed, hope it went well..."