# A very simple Flask Hello World app for you to get started with...

import datetime
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

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

@app.route('/')
def hello_world():
    return 'Hello from RoboCat app!'

@app.route('/memo/api/v1.0/records', methods=['GET'])
def get_records():
    # Test it with "curl -i https://robotcat.pythonanywhere.com/memo/api/v1.0/records"
    return jsonify({'records': records})


@app.route('/memo/api/v1.0/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = [record for record in records if record['id'] == record_id]
    if not any(record):
        abort(404)
    return jsonify({'record': record[0]})


@app.route('/memo/api/v1.0/records/', methods=['POST'])
def create_record():
    if not request.json or not 'date' in request.json:
        abort(400)
    record = request.json
    record['id'] = max(records, key=lambda rec: rec.get('id')) + 1
    for default_key in records[0]:
        record.setdefault(default_key, records[0][default_key])
    return jsonify({'record': record}), 201



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def request_validation(error):
    return make_response(jsonify({'error': 'JSON validation failed! {}'.format(error)}), 400)

if __name__ == "__main__":
    app.run(debug=True)
