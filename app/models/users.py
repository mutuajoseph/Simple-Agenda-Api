from main import db, ma
from werkzeug.security import check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    # agenda = db.relationship('AgendaModel', backref='agendaz', lazy=True )


    # create the record 
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    # fetch records
    @classmethod
    def fetch_records(cls):
        user = cls.query.all()
        return user
    
    # fetch user by id 
    @classmethod
    def fetch_by_id(cls,email):
        user = cls.query.filter_by(email=email).first()
        return user
    
    # check if email exists
    @classmethod
    def check_email_exist(cls,email):
        user = cls.query.filter_by(email=email).first()
        return user
    
    # check if password is valid
    @classmethod
    def check_password(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return True
        else:
            return False


    @classmethod
    def fetch_username(cls,username):
        user = UserModel.filter_by(username=username).first()
        return user
        
    # delete record 
    @classmethod
    def delete_by_id(cls, id):
        user = cls.query.filter_by(id=id)
        if user.first():
            user.delete()
            db.session.commit()
            return True
        else:
            return False
    
    # update by id 
    @classmethod 
    def update_by_id(cls, id, username=None, email=None):
        user = cls.query.filter_by(id=id).first()
        if user:
            if username:
                user.username = username
            if email:
                user.email = email

            db.session.commit()

        return cls.query.filter_by(id=id).first()


class UserSchema(ma.Schema):
    class Meta():
        # fields to expose
        fields= ('id','username','email')