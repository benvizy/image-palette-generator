from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from matplotlib.image import imread
import matplotlib
from statistics import mode
from werkzeug.utils import secure_filename
import os

# Initialize App and Flask and Friends
app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = '/FILEPATH ;)'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to find the top ten most recurring values in a list
def top_boys(list):
    top_ten = []
    for i in range(80):
        most_common = mode(list)
        top_ten.append(most_common)
        list = [value for value in list if value != most_common]

    return top_ten


# Numpy Function to return Hex Values


def readPhoto(pic):
    img = imread(pic)

    hex_array = []

    for r in img:
        for s in r:
            new_array = s.tolist()
            int_array = []
            for i in new_array:
                int_array.append(int(i) / 255)
            try:
                hex_color = matplotlib.colors.to_hex(int_array)
                hex_array.append(hex_color)
            except:
                pass

    return hex_array


# Back End Server

@app.route('/', methods=['GET', 'POST'])
def home():
    # This post method creates the top hexagrams to pass to the colors template.  I started with ten, but I ended up
    # expanding to 50 because it was just so cool.  The print statements were for testing purposes, but I thought it
    # would be fun to leave them in.
    if request.method == 'POST':
        f = request.files['file']
        print(f'The File is {f}')
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f'The File Name is {filename}')
        hex_array = readPhoto(filename)
        print(f'A bit of our hex Array is {hex_array[0:10]}')
        top = top_boys(hex_array)
        print(f'Most recurring: {top}')

        return render_template('colors.html', colors=top)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
