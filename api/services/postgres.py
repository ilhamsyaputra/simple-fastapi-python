import os
import psycopg2
from dotenv import load_dotenv
from services.exception import *

def dbConnect():
    load_dotenv()

    return psycopg2.connect(
        database = os.getenv('DATABASE'),
        host = os.getenv('HOST'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        port = os.getenv('PORT')
    )

def createDatabase():
    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute('create table if not exists person (id int not null primary key, nama varchar(100) not null, jenis_kelamin char(1) not null, id_orangtua int)')


def generateID():
    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute('select max(id) from person')
    return db_cursor.fetchone()[0] + 1

def addParent(nama: str):
    '''
    Function to add parents data to database if user's parent data is not in database
    '''

    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute(
        'insert into person values (%s, %s, %s, %s)',
        (generateID(), nama, 'm', None)
    )
    database.commit()

def getParentsId(nama: str):
    '''
    Function to get parentsID
    if no input ('') then will insert null value to database
    if parents name not in database, then add parents data to database
    '''
    
    database = dbConnect()
    db_cursor = database.cursor()

    nama = nama.capitalize()

    if nama == '':
        return None

    try:
        db_cursor.execute('select id from person where nama = %s', (nama,))
        return db_cursor.fetchone()[0]
    except TypeError:
        addParent(nama)

        db_cursor.execute('select id from person where nama = %s', (nama,))
        return db_cursor.fetchone()[0]

def create(nama: str, jenis_kelamin: str, id_orangtua: str):
    '''
    Function to insert data to database
    '''

    database = dbConnect()
    db_cursor = database.cursor()

    id_orangtua = getParentsId(id_orangtua)

    if nama == '':
        raise InvalidNameError

    if jenis_kelamin not in ['m', 'f'] or jenis_kelamin == '':
        raise InvalidGenderError


    db_cursor.execute(
        'insert into person values (%s, %s, %s, %s)',
        (generateID(), nama, jenis_kelamin, id_orangtua)
    )
    database.commit()

def read(nama: str):
    '''
    Function to get data with nama as parameter
    '''

    database = dbConnect()
    db_cursor = database.cursor()
    nama = nama.capitalize()

    db_cursor.execute(f'select * from person where nama = \'{nama}\'')
    return db_cursor.fetchall()

def update(id: int, nama: str, jenis_kelamin: str, id_orangtua: str):
    '''
    Function to update existing data in database
    '''

    database = dbConnect()
    db_cursor = database.cursor()

    id_orangtua = getParentsId(id_orangtua)

    if nama == '':
        raise InvalidNameError

    if jenis_kelamin not in ['m', 'f'] or jenis_kelamin == '':
        raise InvalidGenderError

    db_cursor.execute('update person set nama = %s, jenis_kelamin = %s, id_orangtua = %s where id = %s', (nama, jenis_kelamin, id_orangtua, id))
    database.commit()

def delete(id: int):
    database = dbConnect()
    db_cursor = database.cursor()

    db_cursor.execute('delete from person where id = %s', (id,))
    database.commit()

    if db_cursor.rowcount == 0:
        raise DeleteError

def readAll():
    '''
    Function to get all data in database
    '''

    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute(f'select * from person')
    return db_cursor.fetchall()