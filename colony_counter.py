from IPython.display import Image
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os
from flask import Flask, request, redirect, url_for, render_template, flash, session
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from datetime import datetime
import string
import random


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENTIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.secret_key = "hogehoge"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS


@app.route("/", methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Not Found File")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Not Found ")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #remove unsupported letter
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)            
            
            Image(filename = filepath)
            
            img = cv2.imread(filepath)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            red = cv2.inRange(hsv, np.array([145, 70, 0]), np.array([180, 255, 255]))
            yellow = cv2.inRange(hsv, np.array([10, 80, 0]), np.array([50, 255, 255]))
            blue = cv2.inRange(hsv, np.array([108, 121, 0]), np.array([120, 255, 255]))

            #収縮演算
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            bin_imgs = {"red": red, "yellow": yellow, "blue": blue}

            fig, ax = plt.subplots(figsize=(12, 10))
            ax.axis("off")
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            answer_list = []
            for label, bin_img in bin_imgs.items():
                contours, _ = cv2.findContours(
                    bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = list(filter(lambda cnt: len(cnt) > 1, contours))
                count = len(contours)

                result = "color = {} count:{}".format(label, count)
                answer_list.append(result)
                
            return render_template("index.html", answer = answer_list)
    
    return render_template("index.html", answer = "")

if __name__=="__main__":
    app.run(debug=True)     
            
            
            
            