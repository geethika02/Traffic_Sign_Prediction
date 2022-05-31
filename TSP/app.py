import os
import numpy as np
from flask import *
import tensorflow
from keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Classes of trafic signs
classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)',
            2:'Speed limit (50km/h)',
            3:'Speed limit (60km/h)',
            4:'Speed limit (70km/h)',
            5:'Speed limit (80km/h)',
            6:'End of speed limit (80km/h)',
            7:'Speed limit (100km/h)',
            8:'Speed limit (120km/h)',
            9:'No passing',
            10:'No passing veh over 3.5 tons',
            11:'Right-of-way at intersection',
            12:'Priority road',
            13:'Yield',
            14:'Stop',
            15:'No vehicles',
            16:'Vehicle > 3.5 tons prohibited',
            17:'No entry',
            18:'General caution',
            19:'Dangerous curve left',
            20:'Dangerous curve right',
            21:'Double curve',
            22:'Bumpy road',
            23:'Slippery road',
            24:'Road narrows on the right',
            25:'Road work',
            26:'Traffic signals',
            27:'Pedestrians',
            28:'Children crossing',
            29:'Bicycles crossing',
            30:'Beware of ice/snow',
            31:'Wild animals crossing',
            32:'End speed + passing limits',
            33:'Turn right ahead',
            34:'Turn left ahead',
            35:'Ahead only',
            36:'Go straight or right',
            37:'Go straight or left',
            38:'Keep right',
            39:'Keep left',
            40:'Roundabout mandatory',
            41:'End of no passing',
            42:'End no passing vehicle > 3.5 tons' }

def image_processing(img):
    model = load_model('./model/TSR.h5')
    data = []
    img = tensorflow.keras.utils.load_img(img,target_size = (30,30))
    img = tensorflow.keras.utils.img_to_array(img)
    data.append(img)
    X_test = np.array(data)
    Y_pred = model.predict(X_test)
    Y_pred = model.predict(X_test)
    a = np.argmax(Y_pred,axis=1)
    return a[0]

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        result = image_processing(file_path)
        result = classes[result]
        os.remove(file_path)
        return render_template('/result.html', result = result)
    return None

if __name__ == '__main__':
    app.run(debug=True)