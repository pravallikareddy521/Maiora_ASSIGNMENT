from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob_day = db.Column(db.Integer)
    dob_month = db.Column(db.Integer)
    dob_year = db.Column(db.Integer)
    age = db.Column(db.Integer)


db.create_all()

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(
        name=data['name'],
        dob_day=data['dob_day'],
        dob_month=data['dob_month'],
        dob_year=data['dob_year'],
        age=calculate_age(data['dob_day'], data['dob_month'], data['dob_year'])
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created'}), 201



@app.route('/students/age_range', methods=['GET'])
def get_students_in_age_range():
    students = Student.query.filter(Student.age.between(18, 25)).all()
    result = []
    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'dob': f'{student.dob_day}/{student.dob_month}/{student.dob_year}',
            'age': student.age
        }
        result.append(student_data)
    return jsonify(result)

def calculate_age(day, month, year):
    today = date.today()
    birth_date = date(year, month, day)
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

if __name__ == '__main__':
    app.run(debug=True)
