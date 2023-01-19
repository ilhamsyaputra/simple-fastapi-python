from fastapi import FastAPI, Response, status
import services.postgres as service
from pydantic import BaseModel
from services.exception import *

class User(BaseModel):
    nama: str
    jenis_kelamin: str
    nama_orangtua: str

app = FastAPI()

# get users detail by name
@app.get('/users/{name}', status_code=200)
async def getUser(name: str, response: Response):
    try:
        data = service.read(name)[0]

        return {
            'success': 'true',
            'message': 'data found',
            'data': {
                'id': data[0],
                'name': data[1],
                'gender': data[2],
                'parentId': data[3]
            }
        }
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'success': 'false',
            'message': 'user not exist'
        }

# get list of all users
@app.get('/users/')
async def getAllUsers():

    data = service.readAll()

    dataa = []

    for i in data:
        dictData = {
            'id': i[0],
            'name': i[1],
            'gender': i[2],
            'parentId': i[3]
        }

        dataa.append(dictData)
    
    out = {
        'success': 'true',
        'message': 'data found',
        'data': dataa
    }

    return out

# add users
@app.post('/users/', status_code=200)
async def addUser(data: User, response: Response):
    
    nama = data.nama
    jenis_kelamin = data.jenis_kelamin
    orangtua = data.nama_orangtua

    try:
        service.create(nama, jenis_kelamin, orangtua)
        response.status_code = status.HTTP_201_CREATED
        return {
            'success': 'true',
            'message': 'user added to database',
            'data': data
        }
    except InvalidGenderError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': 'false',
            'message': 'error occurred: Gender is not valid'
        }
    except InvalidNameError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': 'false',
            'message': 'error occurred: Name is not valid'
        }


# update users
@app.put('/users/{id}', status_code=200)
async def updateUser(data: User, id: int, response: Response):
    
    nama = data.nama
    jenis_kelamin = data.jenis_kelamin
    orangtua = data.nama_orangtua

    try:
        service.update(id, nama, jenis_kelamin, orangtua)
        response.status_code = status.HTTP_202_ACCEPTED
        return {
            'success': 'true',
            'message': 'user detail updated',
            'data': data
        }
    except InvalidGenderError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': 'false',
            'message': 'error occurred: Gender is not valid'
        }
    except InvalidNameError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': 'false',
            'message': 'error occurred: Name is not valid'
        }

# delete users
@app.delete('/users/{id}', status_code=200)
async def deleteUser(id: int, response: Response):
    try:
        service.delete(id)
        response.status_code = status.HTTP_202_ACCEPTED
        return {
            'success': 'true',
            'message': 'users deleted'
        }
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': 'false',
            'message': 'error occurred'
        }