from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

import company_func
budget_gap = 0.8

config = company_func.initialize_config()
app = Flask(__name__)
users = {
    "user1": "parola1",
    "user2": "parola2"
}

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in users.keys():
        if password == users[username]:
            return True
    return False


@app.route("/")
def first_func():
    return {"message": "Hello world!"}


@app.route("/home", methods=['PUT', 'POST'])
def second_func():
    print(request.method)
    data = request.data
    data = data.decode()
    print(data)
    return {"message": "Post or put request"}


@app.route("/emps/<emp_id>")
def get_employees(emp_id):
    if emp_id:
        sql_query = f"select * from company.employees where emp_id = {emp_id}"
        return company_func.read_from_database(sql_query, config)


@app.route("/emps/<emp_id>", methods=["DELETE"])
@auth.login_required
def fire_employees(emp_id):
    sql_query = f"DELETE from company.employees where emp_id = {emp_id}"
    response = company_func.execute_query(sql_query, config)
    if "DELETE 0" == response:
        return {"error": "Employee not in database"}
    return {"message": "Successfully removed employee from database"}


@app.route("/emps/<emp_id>/update_salary", methods=["PUT"])
@auth.login_required
def update_salary():
    data = request.json
    if ("name" in data or "emp_id" in data) and 'percentage' in data:
        emps_query = f"select emp_id, name, salary from company.employees where name = '{data['name']}'"
        emp = company_func.read_from_database(emps_query, config)[0]
        available_budget_query = f"""select sum(p.budget) from company.projects p 
                                                    join company.contracts c on c.project_id = p.proj_id
                                                    join company.employees e on e.emp_id = c.emp_id
                                                    where e.emp_id = {emp['emp_id']};"""
        budget = company_func.read_from_database(available_budget_query, config)
        new_salary = emp['salary'] + emp['salary'] * float(data["percentage"])/ 100
        if new_salary < budget[0]['sum'] * company_func.budget_gap:
            response = company_func.execute_query(f"UPDATE company.employees set salary = {new_salary} "
                                                  f"where emp_id = {emp_pick}", config)
            print(response)
            return print("Employee's salary was updated")
        else:
            print("Not enough money for the raise.")
            return {"error": "Not enough money"}
    else:
        return {"error": "Mandatory variables were not provided. Please provide name or id."}



if __name__ == '__main__':
    app.run()
