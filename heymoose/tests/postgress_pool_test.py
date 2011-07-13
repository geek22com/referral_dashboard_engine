# -*- coding: utf-8 -*-
import sys

sys.path.append("/home/kshilov/Prg/tuta/apache_configuration/frontend")

from heymoose.db.connection import connection

def new_user(username, email, password):
        args = {'name' : username,
                        'email' : email,
                        'password' : password}
        query = "INSERT INTO users (name, email, password) VALUES(%(name)s, %(email)s, %(password)s)"
        connection.execute_query(query, args)


def get_user(username):
        args = {'name' : username}
        query = "SELECT * FROM users WHERE name = %(name)s"
        user = connection.select_query(query, args)
        return user if user else None

def check_user(email):
        args = {'email':email}
        query = "SELECT id FROM users WHERE email = %(email)s"
        res = connection.select_query(query, args)
        return res if res else None

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    args = {'name' : username}
    query = "SELECT id FROM users WHERE name = %(name)s"
    rv = connection.select_query(query, args)
    return rv if rv else None

def new_question(user_id, text):
        args = {'questioner_id' : user_id,
                        'body' : text}
        query = "INSERT INTO questions (questioner_id, body, pub_date) VALUES(%(questioner_id)s, %(body)s, NOW())"
        connection.execute_query(query, args)

def get_questions_answers(user_id):
        args = {'questioner_id': user_id}
        query = "SELECT * FROM questions q LEFT JOIN answers a ON a.question_id = q.id WHERE q.questioner_id = %(questioner_id)s"
        res = connection.select_query(query, args)
        return res

