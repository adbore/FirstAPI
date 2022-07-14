from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# Create Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False

# sqlalchemy mapper
db = SQLAlchemy(app)


# Add a class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"


# For GET request to http://localhost:5000/
class GetEmployee(Resource):

    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {'Id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname, 'Gender': emp.gender,
                        'Salary': emp.salary}
            emp_list.append(emp_data)
        return {"Employees": emp_list}, 200


# For POST request to http://localhost:5000/employee
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstname=request.json['FirstName'], lastname=request.json['LastName'],
                           gender=request.json['Gender'], salary=request.json['Salary'])
            db.session.add(emp)
            db.session.commit()
            # Return the json response
            return make_response(jsonify({'Id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname,
                                          'Gender': emp.gender, 'Salary': emp.salary}), 201)
        else:
            return {'Error: Request Must Json'}, 400


# For PUT request to http://localhost:5000/update/?
class UpdateEmployee(Resource):

    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'Error': 'Not Found'}, 404
            else:
                emp.firstname = request.json['FirstName']
                emp.lastname = request.json['LastName']
                emp.gender = request.json['Gender']
                emp.salary = request.json['Salary']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'Error: Request Must Json'}, 400


# For DELETE request to http://localhost:5000/delete/?
class DeleteEmployee(Resource):

    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'Error': 'Not Found'}, 404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200


api.add_resource(GetEmployee, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(Debug=True)
