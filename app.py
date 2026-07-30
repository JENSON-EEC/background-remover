from flask import Flask, render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

from modules.background import remove_background

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    original = None
    result = None

    if request.method == "POST":

        file = request.files["image"]

        if file:

            filename = secure_filename(file.filename)

            input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            output_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)

            file.save(input_path)

            remove_background(input_path, output_path)

            original = input_path
            result = output_path

    return render_template(
        "index.html",
        original=original,
        result=result
    )

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory("uploads", filename)


@app.route("/outputs/<filename>")
def outputs(filename):
    return send_from_directory("outputs", filename)
if __name__ == "__main__":
    app.run(debug=True)