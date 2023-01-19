import os
import psycopg2
from dotenv import load_dotenv

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

def create():
    '''
    Function to insert data to database
    '''

    database = dbConnect()
    db_cursor = database.cursor()

    nama = input('Masukkan nama: ')
    jenis_kelamin = input('Masukkan jenis kelamin (f\m): ').lower()
    id_orangtua = getParentsId(input('Masukkan nama orang tua: '))

    if jenis_kelamin not in ['m', 'f']:
        print('-'*30)
        print('gender value is not valid')
        print('-'*30)
    else:
        db_cursor.execute(
            'insert into person values (%s, %s, %s, %s)',
            (generateID(), nama, jenis_kelamin, id_orangtua)
        )
        database.commit()
        print('-'*30)
        print(db_cursor.rowcount, 'record(s) affected')
        print('-'*30)

def read(nama: str):
    '''
    Function to get data with nama as parameter
    '''

    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute(f'select * from person where nama = \'{nama}\'')
    return db_cursor.fetchall()

def update():
    '''
    Function to update existing data in database
    '''

    database = dbConnect()
    db_cursor = database.cursor()

    id = input('Enter id: ')
    name = input('Enter name: ')
    jenis_kelamin = input('Enter gender: ')
    id_orangtua = getParentsId(input('Masukkan nama orang tua: '))

    if jenis_kelamin not in ['m', 'f']:
        print('-'*30)
        print('gender value is not valid')
        print('-'*30)
    else:
        db_cursor.execute('update person set nama = %s, jenis_kelamin = %s, id_orangtua = %s where id = %s', (name, jenis_kelamin, id_orangtua, id))
        database.commit()
        print('-'*30)
        print(db_cursor.rowcount, 'record(s) affected')
        print('-'*30)

def delete():
    '''
    Function to delete data from database
    '''

    database = dbConnect()
    db_cursor = database.cursor()

    id = input('Enter id: ')

    db_cursor.execute('delete from person where id = %s', (id,))
    database.commit()
    print('-'*30)
    print(db_cursor.rowcount, 'record(s) deleted')
    print('-'*30)

def readAll():
    '''
    Function to get all data in database
    '''

    database = dbConnect()
    db_cursor = database.cursor()
    db_cursor.execute(f'select * from person')
    return db_cursor.fetchall()

def showData(data: list):
    '''
    Function to formatting the output data from database and print it on console
    '''

    print('-'*30)
    print("id, nama, jenis_kelamin, id_orangtua")
    for i in data:
        print(i)

def main():
    createDatabase()

    while True:
        print('#'*30)
        print('1. View data\n2. Add data\n3. Update data\n4. Delete data\n5. Exit')
        print('#'*30)
        choice = input('Enter your choice: ')

        if choice == '1':
            showData(readAll())
        elif choice == '2':
            create()
        elif choice == '3':
            update()
        elif choice == '4':
            delete()
        elif choice == '5':
            break
        else:
            print(f'\n{choice} is invalid choice\n')

if __name__ == '__main__':
    main()

