import math
import time
import certifi

from datetime import datetime
from pprint import PrettyPrinter
from flask import Flask, request, jsonify, make_response, render_template
from pymongo import MongoClient
from sympy import solveset

from helper_function import find_number
from edge_cases import side_cases

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('localhost', 27017)

solveapi_db = client.SolveAPI

printer = PrettyPrinter()

collection = solveapi_db.equationSolver
logs = solveapi_db.equationLogs

# INDEXING ON THE 'NAME' PROPERTY
collection.create_index("number")


@app.route('/', methods=["POST", "GET"])
def solve_equation():

    if request.method == 'POST':
        equation = request.form.get('equation')
        equation_copy = equation
        equation = equation.replace(" ", "")

        # INSERT INTO LOGS
        inserted_log = {
            'equation': equation_copy,
            'formatedEquation': equation,
            'timeOfLog': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        logs.insert_one(inserted_log)

        # FOR EDGE CASES
        flag, number_left, var, variable = side_cases(equation)

        if flag is False:
            return make_response(jsonify(
                Message="NO OUTPUT EXISTS, PLEASE RETRY WITH POWER 2 VALUES"
            ), 200)

        number = find_number(equation)
        temp_number = number
        number = number/number_left

        if number is False:
            return make_response(jsonify(
                Message="NO OUTPUT EXISTS, PLEASE RETRY WITH POWER 2 VALUES"
            ), 200)

        # NUMBER PRESENT IN DB
        numberUsed = collection.find_one({"number": number})
        if numberUsed is not None:
            return make_response(jsonify(
                Message="It was previously solved",
                Equation=equation,
                TimeTaken=numberUsed['timeTaken'],
                Steps=numberUsed['steps'],
                Result=str(numberUsed['result'])
            ), 200)

        begin = time.time()
        # SYMPY SOLVER
        sol = solveset(var**2 - float(number), var)
        end = time.time()

        # TIME TAKEN
        time_taken = end-begin

        # FOR STEP 3
        if number < 0:
            sqrt_part = str(sol)
        else:
            sqrt_part = math.sqrt(number)

        steps = {
            'Step 1': f'Constant value : {temp_number}, Coeff value : {number_left}',
            'Step 2': f'By Refactoring => sqrt({number})',
            'Step 3': f'+ve value = {sqrt_part}, -ve value = -{sqrt_part}'
        }

        final_answer = {
            variable: str(sol)
        }

        # INSERT NEW DOCUMENT
        inserted_number = {
            'number': number,
            'result': str(sol),
            'timeTaken': str(time_taken),
            'steps': steps
        }

        inserted_id = collection.insert_one(inserted_number).inserted_id

        return make_response(jsonify(
            Equation=equation,
            final_answer=final_answer,
            Steps=steps
        ), 200)

    else:
        return render_template('input.html')


if __name__ == "__main__":
    app.run(port=3003, debug=True)
