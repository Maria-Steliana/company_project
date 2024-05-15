from flask import Flask, request

import company_func

config = company_func.initialize_config()
app = Flask(__name__)

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



if __name__ == '__main__':
    app.run()
