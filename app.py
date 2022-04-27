import firebase_admin
from firebase_admin import credentials, firestore;
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Thread
import RoboQueue
import os

# Initialize Flask
app = Flask(__name__, template_folder="public/Main/")
socketIO_ = SocketIO(app, async_mode=None)
CORS(app)

# Initialize Firebase / Firestore
cred = credentials.Certificate("firebase_private_key.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
objData = {} # This is the object to send back to JS.

# SocketIO event handlers
@socketIO_.on('connect')
def connect_handler(auth):
    print("Client connected")

@socketIO_.on('disconnect')
def disconnect_handler():
    print("Client disconnected.")

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
        else:

            return update_state(data['tableId'], data['newState'])

        return jsonify(objData)
 
def update_state(tableId, newState):

    tableRef = firestore_db.collection("tables")
    idQuery = tableRef.document(tableId)
    idQuery.update({"strState": newState})
    socketIO_.emit('update_state_recv', {'tableId': tableId, 'strState': newState}, broadcast=True)
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
        socketIO_.emit('add_table_recv', {'tableId': tableId, 'numSeats': numSeats, 'sectionUid': sectionUid, 'strState': strState}, broadcast=True)
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
            socketIO_.emit('rem_table_recv', {'tableId': tableId}, broadcast=True)

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

@app.route('/404', methods=['GET', 'POST'])
@app.errorhandler(404)
def render_404(e):
    return render_template('404.html')

if __name__ == '__main__':
    # GCR Dockerfile will run "python app.py" - Therefore this section will be executed.
    robothread = Thread(target=RoboQueue.main, args=[socketIO_])
    robothread.daemon = True
    robothread.start()
    socketIO_.run(app, debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
else:
    # If local, this will be executed - assuming you use "flask run [params]"
    robothread = Thread(target=RoboQueue.main, args=[socketIO_])
    robothread.daemon = True
    robothread.start()