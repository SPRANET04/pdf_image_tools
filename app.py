from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resize", methods=["POST"])
def resize():

    if not os.path.exists("uploads"):
         os.makedirs("uploads")

    file = request.files["image"]
    width = request.form.get("width")
    height = request.form.get("height")
    size_kb = request.form.get("size_kb")
    size_unit = request.form.get("size_unit")

    if not width and not size_kb:
        return "Please enter width/height or size in KB ❌"

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    img = Image.open(filepath)

    if width and height:
        width = int(width)
        height = int(height)
        img = img.resize((width, height))

    output_path = os.path.join("uploads", "resized_" + file.filename)
    
    img.save(output_path) 

    if size_kb:
     size_kb = int(size_kb)

     if size_unit == "mb":
        size_kb = size_kb * 1024

     quality = 95

     while True:
         img.save(output_path, quality=quality)
         current_size = os.path.getsize(output_path) / 1024

         if current_size <= size_kb or quality <= 10:
            break

         quality -= 5
    app.config["OUTPUT"] = output_path
    return redirect(url_for("result"))

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/download")
def download():
    return send_file(app.config["OUTPUT"], as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
