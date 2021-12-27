import sqlite3
import os
from typing import Tuple

database_path = "db/data.db"

class DB:
    def __init__(self, root_path) -> None:
        self.root_path = root_path

    def get_connection(self):
        return sqlite3.connect(os.path.join(self.root_path, database_path))

    def add_user(self, name, password, pretty_name) -> Tuple[int,str]:

        if self.get_user(name):
            return (409, "User already exists.")

        con = self.get_connection()
        with con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO users VALUES (?, ?, ?)", (name, password, pretty_name))
                return (200,"")
            except sqlite3.Error as e:
                return (500,e.with_traceback())

    def get_user(self, name : str=None) -> list:
        con = self.get_connection()
        with con:
            cur = con.cursor()
            if not name:
                r = cur.execute("SELECT name, pretty_name FROM users")
                return list(r)
            else:
                r = cur.execute("SELECT name, pretty_name FROM users WHERE name=?", (name,))
                return list(r)


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
                return "One or more errors occurred, not committing!"
            else:
                con.commit()
                return "Committed, hope it went well..."