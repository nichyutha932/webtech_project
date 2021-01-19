# Previous imports remain...
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


class PetModel(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    breed = db.Column(db.String(), default=False)
    description = db.Column(db.String())
    hobby = db.Column(db.String())
    vaccination = db.Column(db.String())

    def __init__(self, name, type, breed, description, hobby, vaccination):
        self.name = name
        self.type = type
        self.breed = breed
        self.description = description
        self.hobby = hobby
        self.vaccination = vaccination

    def __repr__(self):
        return f" {self.name}"

    def get_one(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'breed': self.breed,
            'description': self.description,
            'hobby': self.hobby,
            'vaccination': self.vaccination,
        }


@app.route('/api/pets', methods=['POST'])
def save_pets():
    temp = request.form['data']
    temp = json.loads(temp)
    pet = PetModel(temp['name'], temp['type'],
                   temp['breed'], temp['description'], temp['hobby'], temp['vaccination'])
    db.session.add(pet)
    db.session.commit()
    res = {}
    res['success'] = True
    return pet.get_one()


@app.route('/api/pets/<int:id>', methods=['PUT'])
def put_pets(id):
    temp = request.form['data']
    temp = json.loads(temp)
    db_pet = PetModel.query.filter_by(id=id).first()
    db_pet.name = temp['name']
    db_pet.type = temp['type']
    db_pet.breed = temp['breed']
    db_pet.description = temp['description']
    db_pet.hobby = temp['hobby']
    db_pet.vaccination = temp['vaccination']
    db.session.commit()
    return db_pet.get_one()


@app.route('/api/pets/<int:id>', methods=['GET'])
def get_pet_detail(id):
    db_pet = PetModel.query.filter_by(id=id).first()
    return render_template("pet_detail.html", pet_detail=db_pet.get_one())


@app.route('/api/pets/<int:id>/vaccination', methods=['GET'])
def get_pet_vaccination(id):
    db_pet = PetModel.query.filter_by(id=id).first()
    pet_detail = db_pet.get_one()
    return render_template("Vaccination_detail.html", pet_detail=db_pet.get_one())


@app.route('/api/pets/<int:id>', methods=["DELETE"])
def delete_pets(id):
    PetModel.query.filter_by(id=id).delete()
    db.session.commit()
    res = {}
    res['success'] = True
    return res


@app.route('/api/pet_one', methods=['POST'])
def pet_one():
    temp = request.form['data']
    temp = json.loads(temp)
    db_pet = PetModel.query.filter_by(id=int(temp['id'])).first()
    return db_pet.get_one()


@app.route('/api/pets', methods=['Get'])
def get_pets():
    pet_list = PetModel.query.all()
    return render_template("pet_list.html", pet_list=pet_list)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
