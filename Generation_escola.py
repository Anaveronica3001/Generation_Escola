
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CRUD App"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    semester1 = db.Column(db.Float)
    semester2 = db.Column(db.Float)
    professor = db.Column(db.String(50))
    room_number = db.Column(db.Integer)

    def __init__(self, name, age, semester1, semester2, professor, room_number):
        self.name = name
        self.age = age
        self.semester1 = semester1
        self.semester2 = semester2
        self.professor = professor
        self.room_number = room_number

# Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'semester1', 'semester2', 'professor', 'room_number')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Routes
@app.route('/students', methods=['POST'])
def add_student():
    name = request.json['name']
    age = request.json['age']
    semester1 = request.json['semester1']
    semester2 = request.json['semester2']
    professor = request.json['professor']
    room_number = request.json['room_number']

    new_student = Student(name, age, semester1, semester2, professor, room_number)

    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)

@app.route('/students', methods=['GET'])
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)

@app.route('/students/', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    return student_schema.jsonify(student)

@app.route('/students/', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)

    name = request.json['name']
    age = request.json['age']
    semester1 = request.json['semester1']
    semester2 = request.json['semester2']
    professor = request.json['professor']
    room_number = request.json['room_number']

    student.name = name
    student.age = age
    student.semester1 = semester1
    student.semester2 = semester2
    student.professor = professor
    student.room_number = room_number

    db.session.commit()

    return student_schema.jsonify(student)

@app.route('/students/', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return student_schema.jsonify(student)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


'''To run this code, you'll need to install the required packages using pip:

bash'''
'''pip install Flask flask_sqlalchemy flask_marshmallow flask_swagger_ui'''


'''Remember to replace the `mysql://username:password@localhost/db_name` in the database URI with your actual MySQL connection details. Also, don't forget to create the corresponding MySQL database before running the application.

You can access the Swagger documentation and test the endpoints by visiting `http://localhost:5000/swagger` in your browser (assuming you're running the app locally).
