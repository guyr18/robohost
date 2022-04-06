import firebase_admin
from firebase_admin import credentials, firestore;

from flask import Flask, jsonify, request, render_template
from flask_mail import Mail, Message
import os

# Initialize Flask
app = Flask(__name__, template_folder="public/Main/")

# Initialize Firebase / Firestore
cred = credentials.Certificate("firebase_private_key.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
objData = {} # This is the object to send back to JS.

# Flask email configuration details
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'robohostnoreply@gmail.com'
app.config['MAIL_PASSWORD'] = 'Csci4230!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/data_handler', methods=['POST'])
def data_handler():

    if request.method == 'POST':
        data = request.get_json()

        # Here we can check for some type of parameter like type and determine what kind of data
        # we need to return; table information etc; using firebase API.

        # Load tables
        if data['intType'] == 0:

            return load_table()

        # intType = 1; update state
        elif data['intType'] == 1:

            return update_state(data['tableId'], data['newState'])

        # intType = 2; send confirmation email message
        else:
            
            return confirm_email(data['name'], data['email'])

        return jsonify(objData)

def confirm_email(name, email):
 
    msg = Message('Robohost - Table Confirmation', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = "Hey, " + name + ". Thanks for checking in! Your estimated wait time is <x> minutes and <y> seconds."
    mail.send(msg)
    return jsonify({"resp": "success"})
 
def update_state(tableId, newState):

    tableRef = firestore_db.collection("tables")
    idQuery = tableRef.document(tableId)
    idQuery.update({"strState": newState})
    return jsonify({"resp": "success", "newState": newState})

def load_table():

    tableRef = firestore_db.collection("tables").get()
    objData['src'] = []

    for table in tableRef:

        tableId = table.id
        numSeats = table.get('numSeats')
        sectionUid = table.get('sectionUid')
        strState = table.get('strState')

        objData['src'].append({

            "tableId": tableId,
            "numSeats": numSeats,
            "sectionUid": sectionUid,
            "strState": strState,

        })

    return jsonify(objData)

@app.route('/add_table', methods=['POST'])
def add_table():

    if request.method == 'POST':

        data = request.get_json()
        tableId = data['tableId']
        numSeats = data['numSeats']
        sectionUid = data['sectionUid']
        strState = data['strState']
        colTables = firestore_db.collection("tables")
        colTables.document(tableId).set({

            "numSeats": numSeats,
            "sectionUid": sectionUid,
            "strState": strState,
        })

        objData['resp'] = 'Table added successfully.'
        return jsonify(objData)

@app.route('/remove_table', methods=['POST'])
def remove_table():

    if request.method == 'POST':

        data = request.get_json()
        tableId = data['tableId']
        print("tableId: " + str(tableId))
        colTables = firestore_db.collection("tables")
        docRef = colTables.document(tableId)
        docSnapShot = docRef.get()

        if docSnapShot.exists:

            colTables.document(tableId).delete()
            objData['code'] = 1
        else:
            objData['code'] = 0

        return jsonify(objData)

@app.route('/auth_login', methods=['POST'])
def auth_login():

    if request.method == 'POST':

        # Extract deserialized payload data from JavaScript.
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Get CollectionReference instance for users table.
        colUsers = firestore_db.collection("users")

        # Get DocumentReference instance from collection.
        # Database is setup such that usernames are the primary key
        # for each document.
        docRef = colUsers.document(username)

        # Obtain DocumentSnapshot instance; this is needed to access
        # individual fields for a document.
        docSnapShot = docRef.get()

        # Is their a document in our database for the provided username or
        # does the document exist, but the password is invalid?
        if docSnapShot == None or docSnapShot.get("password") != password:

            objData['msg'] = "Invalid username/password entered!"
            objData['success'] = 0

        # Second case would be that this is a valid login request. For both cases,
        # we will need to send something back to JavaScript to notify the user
        # about what has happened.
        else:

            objData['strName'] = username
            objData['msg'] = "Login successful!"
            objData['success'] = 1
            objData['accessLevel'] = docSnapShot.get("accessLevel")
        
        return jsonify(objData)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def render_index():
    return render_template('index.html')
    
@app.route('/employeeLogin', methods=['GET'])
def render_login():
    return render_template('employeeLogin.html')

@app.route('/howTo', methods=['GET', 'POST'])
def render_how():
    return render_template('howTo.html')

@app.route('/yourTables', methods=['GET', 'POST'])
def render_tables():
    return render_template('yourTables.html')

@app.route('/cview', methods=['GET', 'POST'])
def render_customer_view():
    return render_template('custView.html')

@app.route('/eview', methods=['GET', 'POST'])
def render_employee_view():
    return render_template('employeeView.html')

@app.route('/mview', methods=['GET', 'POST'])
def render_manager_view():
    return render_template('managerView.html')

@app.route('/custInfo', methods=['GET', 'POST'])
def render_cust_info():
    return render_template('custInfo.html')
    
@app.route('/custConfirm', methods=['GET', 'POST'])
def render_cust_confirm():
    return render_template('custConfirm.html')
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))