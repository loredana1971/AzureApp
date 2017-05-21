from flask import Flask, jsonify, request, make_response
from flask import abort
from flask_mysqldb import MySQL
import database as db

app = Flask(__name__)

app.config['MYSQL_USER'] = 'gabrielabarbieru@animale'
app.config['MYSQL_PASSWORD'] = 'database_pass1'
app.config['MYSQL_DB'] = 'animale'
app.config['MYSQL_HOST'] = 'animale.mysql.database.azure.com'
app.config['MY_SQL_PORT'] = 3306;
mysql = MySQL()
mysql.init_app(app)

def AllAnimalsFromBD():
    '''
    raspuns pentru select * from BD
    '''
    listOfAnimals=db.see_all_animals(mysql)
    return listOfAnimals

def AnimalsFromSpecies(speciesName):
    '''
    raspuns pentru select * from BD where species=speciesName
    '''
    listOfAnimals=db.see_all_species_animals(mysql, speciesName)
    return listOfAnimals

def OneAnimal(idAnimal):
    '''
    raspuns pentru select * from BD where idAnimal=idAnimal
    '''
    infoAnimal = db.see_one_animal(idAnimal, mysql)
    return infoAnimal

def isValid(idAnimal):
    '''
    verificare pentru select Adopted from BD where idAnimal=idAnimal
    '''
    valid = db.is_not_adopted(idAnimal, mysql)
    return valid

def adopt(idAnimal):
    '''
    update BD set Adopted=False where idAnimal=idAnimal
    '''
    db.update_adopted_animal(idAnimal, mysql)
    return "Successfully adopted"

def addAnimalBD(animal):
    '''
    insert animal
    campul id trebuie adaugat in json si pus max(id from bd)+1
    campul adopted este false by default
    '''
    db.insert_animal(animal, mysql)
    return "Successfully added"

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/animals/getAll', methods=['GET'])
def getAll():
    listOfAnimals=AllAnimalsFromBD()
    return jsonify({'animals': listOfAnimals})

@app.route('/animals/<string:speciesName>', methods=['GET'])
def getAnimalsFromSpecies(speciesName):
    listOfAnimals=AnimalsFromSpecies(speciesName)
    return jsonify({'animals': listOfAnimals})

@app.route('/animals/getOneAnimal/<int:idAnimal>', methods=['GET'])
def getOneAnimal(idAnimal):
    infoAnimal=OneAnimal(idAnimal)
    return jsonify(infoAnimal)

@app.route('/animals/adopt/<int:idAnimal>', methods=['GET'])
def adoptAnimal(idAnimal):
    if isValid(idAnimal)==True:
        response=adopt(idAnimal)
        return make_response(jsonify({'response': response}), 200)
    else:
        abort(404)

@app.route('/animals/add', methods=['POST'])
def doPost():
    animal = {
        'name': request.json['name'],
        'species': request.json['species'],
        'gender': request.json['gender'],
        'age': request.json['age'],
        'picture': request.json['urlPoza']
    }
    response=addAnimalBD(animal)
    return jsonify({'response': response}), 201

if __name__ == '__main__':
    app.run(debug=True,port=5000)
