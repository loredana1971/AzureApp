import json

def create_table(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute(
        'create table Animals(idAnimal int NOT NULL AUTO_INCREMENT, '
        'name varchar(255) NOT NULL, species VARCHAR(100) NOT NULL, '
        'gender VARCHAR (20) NOT NULL, age int, pictureURL VARCHAR(255) NOT  NULL, '
        'adopted bit, PRIMARY KEY(idAnimal))')

def see_all_animals(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from animals')
    data = cursor.fetchall()
    animals_list = []
    for item in data:
        animals_dict = dict()
        animals_dict["id"] = item[0]
        animals_dict["name"] = item[1]
        animals_dict["species"] = item[2]
        animals_dict["gender"] = item[3]
        animals_dict["age"] = item[4]
        animals_dict["picture"] = item[5]
        animals_dict["adopted"] = item[6].decode("utf-8")
        animals_list.append(animals_dict)
    return animals_list

def see_all_species_animals(mysql, species):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from animals where species = %s", [species])
    data = cursor.fetchall()
    animals_list = []
    for item in data:
        animals_dict = dict()
        animals_dict["id"] = item[0]
        animals_dict["name"] = item[1]
        animals_dict["species"] = item[2]
        animals_dict["gender"] = item[3]
        animals_dict["age"] = item[4]
        animals_dict["picture"] = item[5]
        animals_dict["adopted"] = item[6].decode("utf-8")
        animals_list.append(animals_dict)
    return animals_list

def see_one_animal(animal_id, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from animals where idAnimal = %s", [animal_id])
    data = cursor.fetchall()
    animals_dict = dict()
    if data != ():
        animals_dict["id"] = data[0][0]
        animals_dict["name"] = data[0][1]
        animals_dict["species"] = data[0][2]
        animals_dict["gender"] = data[0][3]
        animals_dict["age"] = data[0][4]
        animals_dict["picture"] = data[0][5]
        animals_dict["adopted"] = data[0][6].decode("utf-8")
    return animals_dict

def insert_animal(animal_dict, mysql):
    cursor = mysql.connection.cursor()
    nume = animal_dict.get("name")
    specie = animal_dict.get("species")
    gen = animal_dict.get("gender")
    age = animal_dict.get("age")
    pictureURL = animal_dict.get('picture')
    adopted = 0
    cursor.execute("insert into Animals values(%s, %s, %s, %s, %s, %s, %s)", (id, nume, specie, gen, age, pictureURL, adopted))
    mysql.connection.commit()

def is_not_adopted(animal_id, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("select adopted from animals where idAnimal = %s", [animal_id])
    data = cursor.fetchall()
    adopt_string = data[0][0].decode("utf-8")
    if adopt_string == "\u0001":
        return False
    else:
        return True

def update_adopted_animal(animal_id, mysql):
    cursor = mysql.connection.cursor()
    adopted = 1
    cursor.execute('update Animals set adopted = %s where idAnimal = %s', (adopted, animal_id))
    mysql.connection.commit()

def delete_all_animals(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from Animals")
    mysql.connection.commit()

def delete_one_animal(id_animal, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from Animals where idAnimal = %s", [id_animal])
    mysql.connection.commit()
