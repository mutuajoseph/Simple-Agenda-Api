from main import db, ma


class AgendaModel(db.Model):
    __tablename = 'agendas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    agenda = db.Column(db.String(), nullable=False)
    # created_at = db.Column(db.Datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # create record 
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch records
    @classmethod
    def fetch_records(cls):
        agenda = cls.query.all()
        return agenda
    
    # fetch by id 
    @classmethod
    def fetch_by_id(cls, id):
        agenda = cls.query.filter_by(id=id).first()
        return agenda
    
     # delete record 
    @classmethod
    def delete_by_id(cls, id):
        agenda = cls.query.filter_by(id=id)
        if agenda.first():
            agenda.delete()
            db.session.commit()
            return True
        else:
            return False

    # update by id 
    @classmethod 
    def update_by_id(cls, id, title=None, agenda=None):
        task = cls.query.filter_by(id=id).first()
        if task:
            if title:
                task.title = title
            if agenda:
                task.agenda = agenda

            db.session.commit()

        return cls.query.filter_by(id=id).first()

class AgendaSchema(ma.Schema):
    class Meta:
        fields =('id','title','agenda')
        