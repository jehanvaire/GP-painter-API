import re
from flask import Flask, request
from flask_cors import cross_origin
import os
import subprocess
from PIL import Image
from io import BytesIO
import base64



app = Flask(__name__)


# INITIALISATION VARIABLES #
adresse = '0.0.0.0'
port = '5000'
debug = True
# FIN INITIALISATION VARIABLES #


app = Flask(__name__)


@app.route('/images', methods=['POST'])
@cross_origin()
def upload():
    # get image data
    image_data = request.form.get('image')

    # convert base64 to image
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image = base64.b64decode(image_data)

    # create PIL image
    image = Image.open(BytesIO(image))
    

    image.save(os.path.join("./images/image.png"))

    x1 = request.form.get('x1')
    y1 = request.form.get('y1')
    x2 = request.form.get('x2')
    y2 = request.form.get('y2')

    # start painter.py with the image file
    subprocess.check_call([f"python3", "painter.py", "image.png", x1, y1, x2, y2])


    # start GP-lines.exe with the image file
    # subprocess.check_call([f"GP-lines.exe", "image.png", x1, y1, x2, y2])

    response = {
        'status': 'success',
        'message': 'Peinture en cours...',
    }

    return response


if __name__ == '__main__':
    app.run(host=adresse, port=port, debug=debug, ssl_context='adhoc')
