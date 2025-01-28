from db import db
from flask import session
import secrets
import os
from PIL import Image

def check_user_in_data(username : str , password : str) :
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute("SELECT username , password FROM users WHERE username = %s AND password = %s" , (username , password))
        data = cursor.fetchone()
        if data :
            return True
        else:
            return False



def check_in_data(username: str, password: str):
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = %s OR password = %s', (username, password))
        data = cursor.fetchone()

        return True if data else False


def check_in_articles(article_name: str, article_content: str):
    user_data = get_user_Data(session['name'], session['password'])
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT * FROM articles WHERE (article_name = %s OR article_content = %s) AND id = %s', (article_name, article_content, user_data['user_id']))
        data = cursor.fetchone()

        return True if data else False


def check_in_likes(user_id: int, article_id: int):
    with db.get_connection() as cnx:
        cursor = cnx.cursor()

        cursor.execute(
            'SELECT * FROM likes WHERE user_id = %s AND article_id = %s', (
                user_id, article_id)
        )
        data = cursor.fetchone()

    return True if data else False


def add_user_to_database(username: str, password: str):
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute(
            'INSERT INTO users (username , password , joined_at) VALUES(%s , %s , CURRENT_TIMESTAMP())',
            (username, password)
        )
        cnx.commit()


def addArticleToDatabase(article_name, article_content, article_image_name):
    user_Data = get_user_Data(session['name'], session['password'])
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO articles (id , article_name , created_at , article_content , article_image) VALUES(%s , %s , CURRENT_TIMESTAMP() , %s , %s)",
            (user_Data['user_id'], article_name, article_content,
             'imgs/article_imgs/' + article_image_name)
        )
        cnx.commit()


def add_like(user_id: int, article_id: int):
    with db.get_connection() as cnx:
        try :

            cursor = cnx.cursor(dictionary=True)
            cursor.execute(
                'INSERT INTO likes (user_id, article_id) VALUES (%s, %s)', (user_id, article_id))

            cursor.execute(
                'UPDATE articles SET likes = likes + 1 WHERE article_id = %s', (article_id,))
            cnx.commit()
        except:
            raise PermissionError('this article might be not found')
    return


def remove_like(user_id: int, article_id: int):
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            'DELETE FROM likes WHERE user_id = %s AND article_id = %s', (user_id, article_id))
        cursor.execute(
            'UPDATE articles SET likes = likes - 1 WHERE article_id = %s', (article_id,))
        cnx.commit()
    return


def get_user_Data(username: str, password: str) -> tuple:
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM users WHERE username = %s AND password = %s',
            (username, password)
        )
        data = cursor.fetchone()

    return data


def get_article_by_id(article_id: int):
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM articles WHERE article_id = %s', (article_id,))
        data = cursor.fetchone()
    return data


def get_user_likes(user_id: int):
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM likes WHERE user_id = %s',
            (user_id,)
        )
        data = cursor.fetchall()

    return data


def saveImage(formImage):
    randomName = secrets.token_hex(8)
    _, file_extension = os.path.splitext(formImage.filename)
    pictureName = randomName + file_extension
    output_size = (500, 300)
    i = Image.open(formImage)
    i.thumbnail(output_size)
    picturePath = os.path.join(
        os.getcwd(), 'static/imgs/article_imgs', pictureName)
    i.save(picturePath)
    return pictureName


def getArticlesData(limit: int = None):
    myDataLimited = None

    if limit != None:
        myDataLimited = limit

    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        if myDataLimited is None:

            cursor.execute(
                "SELECT article_id , id , article_name , created_at  , likes , article_content , article_image FROM articles"
            )

        else:
            cursor.execute(
                f"SELECT article_id , id , article_name , created_at  , likes , article_content , article_image FROM articles LIMIT %s",
                (myDataLimited,)
            )

        data = cursor.fetchall()

    return data


def filter_articles_by_name(searchVal: str):
    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM articles WHERE article_name LIKE %s', (f'%{searchVal}%',))
        data = cursor.fetchall()
    return data

def update_Account(username : str , password : str  , user_profile_image = None):
    user_Data = get_user_Data(session['name'] , session['password'])

    with db.get_connection() as cnx:
        cursor = cnx.cursor(dictionary = True)
        if user_profile_image == None:
            cursor.execute('UPDATE users SET username = %s , password = %s WHERE user_id = %s',(username, password, user_Data['user_id']))

        else:
            cursor.execute('UPDATE users SET username = %s , password = %s , user_profile_image = %s WHERE user_id = %s',(username, password, user_profile_image, user_Data['user_id']))

        cnx.commit()
    
    return

def check_unique_name(username : str):
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        data = cursor.fetchone()

        return False if data else True


def saveUserProfile(formImage):
    randomName = secrets.token_hex(8)
    _, file_extension = os.path.splitext(formImage.filename)
    pictureName = randomName + file_extension
    output_size = (200, 200)
    i = Image.open(formImage)
    i.thumbnail(output_size)
    picturePath = os.path.join(
        os.getcwd(), 'static/imgs/account_imgs', pictureName)
    i.save(picturePath)
    return pictureName



def get_user_articles(user_id : int) -> list:
    with db.get_connection() as cnx:
        cursor  = cnx.cursor(dictionary = True)
        cursor.execute('SELECT * FROM articles WHERE id = %s' , (user_id,))
        data = cursor.fetchall()
    
    return data
        

def remove_article_by_id(article_id : int , user_id : int) -> None:
    with db.get_connection() as cnx:
        cursor  = cnx.cursor(dictionary = True)
        cursor.execute('DELETE FROM articles WHERE article_id = %s AND id = %s' , (article_id , user_id))
        cnx.commit()
    return

def update_article_by_id(article_id : int, user_id : int , article_content : str , article_name : str ) -> None:
    with db.get_connection() as cnx:
        cursor = cnx.cursor()
        cursor.execute("UPDATE articles SET article_content = %s , article_name = %s WHERE id = %s AND article_id = %s" , (article_content , article_name , user_id , article_id))
        cnx.commit()
    return