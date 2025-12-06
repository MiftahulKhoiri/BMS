import os
from werkzeug.utils import secure_filename

def save_file(file, upload_dir):
    filename = secure_filename(file.filename)
    path = os.path.join(upload_dir, filename)
    file.save(path)
    return filename