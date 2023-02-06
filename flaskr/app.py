import os
import uuid
from .main_app import main

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = "{}/uploads/".format(
    PROJECT_HOME
)  # Path where uploaded files are stored
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx", "json"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Function to check if a file extension is valid
    :param filename: The file we want to upload
    :return: True if valid else False
    """
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            # function to secure a filename before storing it
            filename = secure_filename(file.filename)
            destination = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(destination)
            _path = os.path.abspath("<FILE PATH>")
            uf = str(uuid.uuid4())
            # process file
            analysis = main(destination)
            # split by '\n' so the list can be iterated over in html template
            analysis = analysis.split("\n")
            # Return the template filled with the analysis
            return render_template("analysis.html", text=analysis)
    return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new dataset file to analyze it</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        <p>%s</p>
        """ % "<br>".join(
        os.listdir(
            app.config["UPLOAD_FOLDER"],
        )
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
