from flask import Flask, request, jsonify, session
from flask_restx import Api, Resource,fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from config.pygconfig import DevelopmentConfig
from werkzeug.security import generate_password_hash


from config.pygconfig import DevelopmentConfig

app = Flask(__name__)


app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app, version="1.0",title="Agendas Api", description="An API to manage agendas ")

# Namespacing
ns_users = api.namespace('user', description='Perform user operations')
ns_agenda = api.namespace('agenda', description='Perform agenda operations')
ns_login = api.namespace('login', description = 'Perform login operations')

# Api models 
user = api.model('users',{
                    "username": fields.String(required=True, description='The users username'),
                    "email": fields.String(required=True, description='The users email'),
                    "password": fields.String(required=True, description='The users password')
                    })

agenda = api.model('agendas',{
                    "title":fields.String(required=True, description='The title'),
                    "agenda":fields.String(required=True, description='The description'),
                    })

login = api.model('login',{
                    "email":fields.String(required=True, description='The email'),
                    "password":fields.String(required=True, description='The password')
                    })


# Import the models to be used 
from models.agenda import AgendaModel,AgendaSchema
from models.users import UserModel,UserSchema

# serialize the data 
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

agenda_schema = AgendaSchema(strict=True)
agendas_schema = AgendaSchema(many=True,strict=True)

# create the tables before any request is handled
@app.before_first_request
def create_tables():
    db.create_all()


@ns_login.route('')
class Login(Resource):

    @api.doc('post a users login credentials', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    @api.expect(login)
    def post(self):
        # post a user using valid credentials
        try:
            data = api.payload

            email = data['email']
            password = data['password']

            # checks if the email exists
            if UserModel.check_email_exist(email):
                # checks if the password is valid 
                if UserModel.check_password(email,password):
                    return {'status':'User successfully logged in'}, 200
                else:
                    return {'status':'Wrong login credentials!'}, 401
            else:
                return {'status':'Email does not exist!'}, 401
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")

@ns_users.route('')
# @protected
class User(Resource):

    @api.doc('post a user', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    @api.expect(user)
    def post(self):
        try:
            data = api.payload

            username = data['username']
            email = data['email']
            password = data['password']

            if UserModel.check_email_exist(email):
                return {"status":"Email already exists"}, 400
            else:

                hashed_password = generate_password_hash(password)

                user = UserModel(username=username, email=email, password=hashed_password)
                user.create_record()

                return {"status":"User added successfully"}, 201
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
    
    @api.doc('get all users', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def get(self):
        try:
            users = UserModel.fetch_records()
            return users_schema.dump(users)
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
        

@ns_agenda.route('')
class Agenda(Resource):

    # post an agenda
    @api.doc('post an agenda', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    @api.expect(agenda)
    def post(self):
        try:

            data = api.payload 

            title = data['title']
            agenda = data['agenda']

            agenda = AgendaModel(title=title, agenda=agenda)
            agenda.create_record()

            return {"status":"Agenda Added Successfully"}, 201
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")

    # get all agendas 
    @api.doc('get all agendas', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def get (self):
        try:
            agendas = AgendaModel.fetch_records()
            return agendas_schema.dump(agendas)
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
    
    
@ns_users.route('/<int:id>')
class User(Resource):

    # get a specific user 
    @api.doc('get a user by id', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def get(self, id):
        try:
            user = UserModel.fetch_by_id(id)
            return user_schema.dump(user), 200
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
    
        
    
    # delete a user 
    @api.doc('delete a specific user', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def delete(self, id):
        try:
            user = UserModel.delete_by_id(id)
            return {"status":"User successfully deleted"}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
        
    
    # edit a user 
    @api.doc('edit a  specific user', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    @api.expect(user)
    def put(self, id):
        try:
            data = api.payload

            username = email = None

            username = data['username']
            email = data['email']
            
            update_record = UserModel.update_by_id(id=id, username=username, email=email)
            return {'status':'User updatedd successfully'}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")

@ns_agenda.route('/<int:id>')
class Agenda(Resource):

    # get a specific agenda
    @api.doc('get a specific agenda', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def get(self, id):
        try:
            agenda = AgendaModel.fetch_by_id(id)
            return agenda_schema.dump(agenda)
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")

     
    # delete a specific agenda
    @api.doc('delete a specific agenda', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    def delete(self, id):
        try:
            agenda = AgendaModel.delete_by_id(id)
            return {"status":"Agenda successfully deleted"}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")


    # edit an agenda
    @api.doc('update a specific agenda', response={ 200: 'OK', 400: 'Invalid Argument', 404: 'Not Found', 500: 'Mapping Key Error'})
    @api.expect(agenda)
    def put(self, id):
        try:
            data = api.payload

            title = agenda = None

            title = data['title']
            agenda = data['agenda']
            
            update_record = AgendaModel.update_by_id(id=id, title=title, agenda=agenda)
            return {'status':'Agenda updated successfully'}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status = "Could not perform this action", statusCode = "500")
        except KeyError as e:
            api.abort(400, e.__doc__, status = "Could not perform this action", statusCode = "400")
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)