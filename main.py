import base64
from io import BytesIO
import re
from flask import Flask, request
from flask_cors import CORS
import os
import subprocess
from PIL import Image


app = Flask(__name__)


# INITIALISATION VARIABLES #
adresse = '0.0.0.0'
port = 5000
debug = True

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'https://garticphone.com'}})


@app.route('/images', methods=['POST'])
def upload():
    # get image data
    image_data = request.form.get('image')

    # convert base64 to image
    image_data = re.sub('^data:image/.+;base64,', '',  # type: ignore
                        image_data)   # type: ignore
    image = base64.b64decode(image_data)

    # create PIL image
    image = Image.open(BytesIO(image))

    image.save(os.path.join("./images/image.png"))

    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')
    pas = "5"

    # start painter.py with the image file
    # subprocess.check_call([f"python3", "painter.py", "image.png", x1, y1, x2, y2])

    # start GP-lines.exe with the image file
    subprocess.check_call([f"GP-lines.exe", "image.png",
                          x1, y1, x2, y2, pas])  # type: ignore

    # start GP-lines.exe with the image file
    # subprocess.check_call([f"GP-lines.exe", "image.png", x1, y1, x2, y2])

    response = {
        'status': 'success',
        'message': 'Peinture en cours...',
    }

    return response


if __name__ == '__main__':
    app.run(host=adresse, port=port, debug=debug, ssl_context='adhoc')
