from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from dotenv import load_dotenv
from bson import ObjectId
import os
import datetime

# load in the variables in the .env file into our operating system environment
load_dotenv()

app = Flask(__name__)

# connect to mongo
MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

# define my db_name
DB_NAME = "expenselist"

# read in the SESSION_KEY variable from the operating system environment
SESSION_KEY = os.environ.get('SESSION_KEY')

# set the session key
app.secret_key = SESSION_KEY

# Display all expenses
# All routes by default is methods=GET


@app.route('/')
def home():
    # extract out the terms
    search_terms = request.args.get('search-terms')

    criteria = {}

    # if there are search terms, add it to the criteria object
    if search_terms != "" and search_terms is not None:
        criteria['expense_name'] = {
            "$regex": search_terms,
            "$options": "i"
        }

    # Filtering begins here
    search_for_done = request.args.get('is_done')
    if search_for_done is not None and search_for_done is not False:
        criteria['reconciled'] = True

    expenses = client[DB_NAME].expenses.find(criteria)
    return render_template('home.template.html', expenses=expenses)

    print(criteria)
# Show point of entry for expenses


@app.route('/create/expense')
def show_create_expense_form():
    return render_template('create_expense.template.html')

# Write expenses into mongodb


@app.route('/create/expense', methods=['POST'])
def create_expense():
    expense_name = request.form.get('expense-name')
    expense_date = request.form.get('expense-date')
    expense_type = request.form.get('expense-type')
    expense_memo = request.form.get('expense-memo')

    client[DB_NAME].expenses.insert_one({
        'expense_name': expense_name,
        'expense_date': datetime.datetime.strptime(expense_date, "%Y-%m-%d"),
        'expense_type': expense_type,
        'expense_memo': expense_memo,
        'reconciled': False
    })
    flash(f"New task '{expense_name}' has been created")
    return redirect(url_for('home'))

# Check reconcilation


@app.route('/check/expense', methods=['PATCH'])
def check_expense():

    expense_id = request.json.get('expense_id')

    expense = client[DB_NAME].expenses.find_one({
        "_id": ObjectId(expense_id)
    })
    print(expense)

    if expense.get('reconciled') is None:
        expense['reconciled'] = False
    client[DB_NAME].expenses.update({
        "_id": ObjectId(expense_id)
    }, {
        '$set': {
            'reconciled': not expense['reconciled']
        }
    })

    return {
        "status": "OK"
    }


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
