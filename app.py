import flask, zipfile
import os, random
from shutil import rmtree
from io import StringIO

app = flask.Flask(__name__)

storage = "./storage/"


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def uploading():
    if flask.request.method == 'POST':
        print("=====INCOMING UPLOAD=====")
        files = flask.request.files.getlist('file[]')

        if not files:
            return "선택되지 않음"
        else:
            code = padding(6, str(hex(random.randint(0, 16 ** 6 - 1)))[2:]).upper()
            if not os.isdir(storage):
                os.mkdir(storage)
            os.mkdir(storage + code)

            for file in files:
                file.save(storage + code + '/' + file.filename)

            ziped = zipfile.ZipFile(storage + code + '.zip', 'w')
            zipdir(storage + code, ziped)
            ziped.close()

            rmtree(storage + code)

            return code


@app.route('/download', methods=['GET', 'POST'])
def downloading():
    if flask.request.method == 'POST':
        print("=====INCOMING DOWNLOAD=====")

        code = flask.request.form['code'].upper()
        file = storage + code + '.zip'
        print(file)

        return flask.send_from_directory(storage, code + '.zip', as_attachment=True)


def padding(size, value):
    diff = size - len(str(value))
    if diff > 0:
        value = diff * "0" + value

    return value


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    app.run()
    # real zz
