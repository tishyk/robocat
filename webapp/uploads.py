import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt','py', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_files(app, request):
        # check if the post request has the files part
	if 'files[]' not in request.files:
		return False
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return True
