from flask import Flask, request

app = Flask(__name__)

@app.get('/')
def homepage():
    return " Welcome to the homepage! "

@app.post('/login')
def login():
    userdata = request.json
    print(userdata)
    return " Hi {user} , your login request was successful! ".format(user=userdata.get('username').split()[-1])

@app.get('/leaderboard')
def leaderboard():
    students = [
        {'name': 'Halima', 'score': 90},
        {'name': 'Abubakar', 'score': 80},
        {'name': 'Abdulwahab', 'score': 70},
        {'name': 'Aisha', 'score': 60},
    ]
    return {'students': students}

@app.patch('/student/<int:student_index>')
def update_student(student_index):
    student = request.json
    students = [
        {'name': 'Halima', 'score': 90},
        {'name': 'Abubakar', 'score': 80},
        {'name': 'Abdulwahab', 'score': 70},
        {'name': 'Aisha', 'score': 60},
    ]
    students[student_index]['score'] = student['score']
    print(student)
    return {'students': students}

@app.delete('/student/<int:student_index>')
def delete_student(student_index):
    students = [
        {'name': 'Halima', 'score': 90},
        {'name': 'Abubakar', 'score': 80},
        {'name': 'Abdulwahab', 'score': 70},
        {'name': 'Aisha', 'score': 60},
    ]
    students.pop(student_index)
    return {'students': students}

@app.get('/student/<int:student_index>')
def get_student(student_index):
    students = [
        {'name': 'Halima', 'score': 90},
        {'name': 'Abubakar', 'score': 80},
        {'name': 'Abdulwahab', 'score': 70},
        {'name': 'Aisha', 'score': 60},
    ]
    return {'student': students[student_index]}

@app.post('/student')
def add_student():
    userdata = request.json
    students = [
        {'name': 'Halima', 'score': 90},
        {'name': 'Abubakar', 'score': 80},
        {'name': 'Abdulwahab', 'score': 70},
        {'name': 'Aisha', 'score': 60},
    ]
    students.append(userdata.get('student'))
    return {'student': students}

if __name__ == '__main__':
    app.run(debug=True)