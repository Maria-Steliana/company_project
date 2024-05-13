import json
import psycopg2 as ps

with open("config.json", 'r') as f:
    config = json.loads(f.read())

with ps.connect(**config) as conn:
    with conn.cursor() as cursor:
        sql_query = "select * from company.employees"
        cursor.execute(sql_query)
        response = cursor.fetchall()
        print(response)

