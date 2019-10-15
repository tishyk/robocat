# A very simple Flask Hello World app for you to get started with...

import os
import datetime
from flask import Flask, jsonify, abort, make_response, request, url_for, redirect, render_template, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/home/robotcat/webapp/uploads"

auth = HTTPBasicAuth()
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


records = [
    {
        'id': 1,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'color': u'red',
        'flag': False,
        'reminder': datetime.datetime.now(),
        'version': 1,
        'sync': True,
        'title': u'Robocat task #1. Avocato',
        'description': u"""Robocat, by Andrew Clements
	This seven page activity works with the story Robocat, by Andrew Clements.
	The story is also included. The focus still for this activity is reality vs. realism.
	Vocabulary questions and general comprehension questions are also included.
	https://final-space.fandom.com/wiki/Avocato""",

    },
    {
        'id': 2,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'color': u'green',
        'flag': False,
        'reminder': datetime.datetime.now(),
        'version': 2,
        'sync': False,
        'title': u'Robocat task #2. The Dragon of Krakow',
        'description': u"""This 7 page activity corresponds with the story, The Dragon of Krakow.
	 The skill asking questions is explored as well as comprehension questions.
	 https://www.teacherspayteachers.com/Product/The-Dragon-of-Krakow-431206""",
    },
    {
        'id': 3,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'color': u'blue',
        'flag': True,
        'reminder': datetime.datetime.now(),
        'version': 2,
        'sync': True,
        'title': u'Robocat task #3. The Dragon of Krakow',
        'description': u"""This beautifuuly illustrated story is based on a real family of cats. 
	 These real life silver tabby & silver spotted characters are now portrayed in a fully illustrated book
	 suitable for all age groups. There's laughter, danger and romance that will keep you gripped until the very end.
	 https://www.robocats.co.uk/robocats-book-1.html""",
    }
]


@auth.get_password
def get_password(username):
    if username == 'robocat':
        return 'robocat_password'
    return None


def make_public_record(record):
    uri_record = copy(record)
    uri_record['uri'] = url_for('get_record', record_id=record.get('id', 0), _external=True)
    uri_records.pop('id')
    return uri_record


@app.route('/')
def home():
    return render_template('index.html')

ALLOWED_EXTENSIONS = set(['txt','py', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def home_post():
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	flash('File(s) successfully uploaded')
	return redirect('/')



# @app.route('/memo/api/v1.0/records', methods=['GET'])
# def get_records():
#     # Test it with "curl -i https://robotcat.pythonanywhere.com/memo/api/v1.0/records"
#     return jsonify({'records': records})

@app.route('/memo/api/v1.0/records', methods=['GET'])
@auth.login_required    #curl -u robocat:robocat_password -i https://robotcat.pythonanywhere.com/memo/api/v1.0/records
def get_records():
    # Test it with "curl -i https://robotcat.pythonanywhere.com/memo/api/v1.0/records"
    return jsonify({'records': [make_public_record(record) for record in records]})


@app.route('/memo/api/v1.0/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = [record for record in records if record['id'] == record_id]
    if not any(record):
        abort(404)
    return jsonify({'record': record[0]})


@app.route('/memo/api/v1.0/records', methods=['POST'])
def create_record():
    # Testing curl -i -H "Content-Type: application/json" -X POST -d '{"date":"2019-08-09"}' \
    #  http://robotcat.pythonanywhere.com/memo/api/v1.0/records
    if not request.json or not request.json.get('date'):
        abort(400)
    record_id = max(records, key=lambda rec: rec.get('id')).get('id', 0) + 1
    record = {'id': record_id,
              'date': request.json['date'],
              'time': datetime.datetime.now().strftime('%H:%M:%S'),  # Server creation time
              'color': u'red',
              'flag': False,
              'reminder': datetime.datetime.now(),
              'version': 1,
              'sync': True,
              'title': u'Robocat task #{}'.format(record_id),
              'description': u"""Robocat Description"""
              }
    records.append(record)
    return jsonify({'record': record}), 201


@app.route('/memo/api/v1.0/records/<int:record_id>', methods=['PUT'])
def update_task(record_id):
    record = [rec for rec in records if rec['id'] == record_id]
    if not any(record):
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json and isinstance(request.json['description'], str):
        abort(400)
    # Add verification for incoming json data
    for rec in record[0]:
        rec_value = request.json.setdefault(rec, record[0][rec])
        record[0][rec] = rec_value
    return jsonify({'record': record[0]})


@app.route('/memo/api/v1.0/records/<int:record_id>', methods=['DELETE'])
def delete_task(record_id):
    task = [rec for rec in records if rec['id'] == record_id]
    if not any(task):
        abort(404)
    records.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(400)
def request_validation(error):
    return make_response(jsonify({'error': 'JSON validation failed! {}'.format(error)}), 400)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

    if __name__ == "__main__":
        app.run(debug=True)
