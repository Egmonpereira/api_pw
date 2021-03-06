#import das libs
from os import name
from flask import Flask, json, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

from sqlalchemy.engine import result

#recupera o arquivo do banco e utiliza o flask
db_connect = create_engine('sqlite://exemplo.db')
app = Flask(__name__)
api = Api(app)

#cria os endpoints de User, GET, POST E PUT
class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from user")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
    def post(self):
        conn = db_connect.connect()
        name = request.json['name']
        email = request.json['email']
        
        conn.execute(
            "insert into user values(null, '{0}','{1}')".format(name,email)
        )
        
        query = conn.execute('select * from user order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
        
    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']
        
        conn.execute("update user set name ='" + str(name) +
                     "', email='" + str(email) + "' where id = %d " % int(id))
        
        query = conn.execute("select * from user where id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
#cria os endpoints de envio da ID - metodos GET e DELETE

class UserById(Resource):
    def delete(self, id):
        conn = db_connect.connect()
        conn.execute("delete from user where id=%d " % int(id))
        return {"status": "sucess"}
    
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from user")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from user where id = %d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
#mapea os endponts criados e finaliza o arquivo
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')

if __name__ ++ '__main__':
    app.run()