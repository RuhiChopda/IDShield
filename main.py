from flask import Flask, render_template, flash, request, session
import mysql.connector
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import secrets

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# ================= DATABASE CONFIG =================
DB_HOST = "YOUR_HOST"
DB_USER = "YOUR_USERNAME"
DB_PASSWORD = "YOUR_PASSWORD"
DB_NAME = "YOUR_DATABASE"
DB_PORT = 3306

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

# ================= FUNCTIONS =================

def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
    image = cv2.imread(image_name)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8

    if len(secret_data) > n_bytes:
        raise ValueError("Insufficient bytes")

    secret_data += "====="
    data_index = 0
    binary_secret_data = to_bin(secret_data)
    data_len = len(binary_secret_data)

    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)

            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1

            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1

            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1

            if data_index >= data_len:
                break

    return image

def decode(image_name):
    image = cv2.imread(image_name)
    binary_data = ""

    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    decoded_data = ""

    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))

        if decoded_data[-5:] == "=====":
            break

    return decoded_data[:-5]

def string_to_binary(input_string):
    return ''.join(format(ord(char), '08b') for char in input_string)

def binary_to_string(binary_string):
    n = 8
    return ''.join(chr(int(binary_string[i:i + n], 2)) for i in range(0, len(binary_string), n))

def calculate_parity_bits(data_bits):
    if len(data_bits) < 7:
        binary_list = [0] * (7 - len(data_bits)) + data_bits

    binary_list[0] = (binary_list[2] + binary_list[4] + binary_list[6]) % 2
    binary_list[1] = (binary_list[2] + binary_list[5] + binary_list[6]) % 2
    binary_list[2] = (binary_list[4] + binary_list[5] + binary_list[6]) % 2

    return binary_list

def detect_and_correct_error(codeword):
    code = [int(bit) for bit in codeword]

    p1 = (code[2] + code[4] + code[6]) % 2
    p2 = (code[2] + code[5] + code[6]) % 2
    p3 = (code[4] + code[5] + code[6]) % 2

    error_position = p1 * 1 + p2 * 2 + p3 * 4

    if error_position != 0:
        code[error_position - 1] = 1 - code[error_position - 1]
        return ''.join(str(bit) for bit in code)

    else:
        return codeword

def detect_and_crop_head(input_image_path, output_image_path, factor=1.7):
    from PIL import Image

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    image = Image.open(input_image_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(20, 20)
    )

    if len(faces) > 0:
        faces = sorted(faces, key=lambda f: f[2] * f[3])

        x, y, w, h = faces[0]

        center_x = x + w // 2
        center_y = y + h // 2

        size = int(max(w, h) * factor)

        x_new = max(0, center_x - size // 2)
        y_new = max(0, center_y - size // 2)

        cropped_head = cv_image[y_new:y_new + size, x_new:x_new + size]

        cropped_head_pil = Image.fromarray(
            cv2.cvtColor(cropped_head, cv2.COLOR_BGR2RGB)
        )

        cropped_head_pil.save(output_image_path)

def encode_text_to_image(text, image_path, output_image_path):
    from PIL import Image

    binary_text = ''.join(format(ord(char), '08b') for char in text)

    img = Image.open(image_path)
    img = img.convert('RGB')

    pixels = img.load()

    width, height = img.size

    idx = 0

    for y in range(height):
        for x in range(width):
            if idx < len(binary_text):
                pixel = list(pixels[x, y])

                for i in range(3):
                    if idx < len(binary_text):
                        pixel[i] = pixel[i] & ~1 | int(binary_text[idx])
                        idx += 1

                pixels[x, y] = tuple(pixel)

    img.save(output_image_path)

def decode_text_from_image(image_path):
    from PIL import Image

    img = Image.open(image_path)
    img = img.convert('RGB')

    pixels = img.load()

    binary_text = ''

    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            for i in range(3):
                binary_text += str(pixel[i] & 1)

    decoded_text = ''

    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i + 8]

        decoded_text += chr(int(byte, 2))

        if decoded_text[-1] == '\x00':
            break

    return decoded_text

# ================= ROUTES =================

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/adminhome")
def adminhome():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select * from user")
    data = cursor.fetchall()
    return render_template("adminhome.html", data=data)

@app.route("/userhome")
def userhome():
    uname = session['uname']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select * from user where uname='" + uname + "'")

    data = cursor.fetchall()

    return render_template("userhome.html", data=data)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/number")
def number():
    return render_template('number.html')

@app.route("/view1")
def view1():
    uname = session['uname']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select * from filetrans where uname='" + uname + "'")

    data = cursor.fetchall()

    return render_template('view1.html', data=data)

@app.route("/imgview")
def imgview():
    uname = session['uname']
    id = request.args.get('id')

    session['did'] = id

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select * from filetrans where uname='" + uname + "'")

    data = cursor.fetchall()

    return render_template('imgview.html', data=data)

@app.route("/admin")
def admin():
    return render_template('AdminLogin.html')

@app.route("/user")
def user():
    return render_template('UserLogin.html')

@app.route("/newregister", methods=['GET', 'POST'])
def newregister():
    if request.method == 'POST':

        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        pnumber = request.form['pnumber']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "insert into user values('','" +
            name + "','" +
            gender + "','" +
            address + "','" +
            email + "','" +
            pnumber + "','" +
            uname + "','" +
            password + "')"
        )

        conn.commit()
        conn.close()

        return render_template("UserLogin.html")

@app.route("/userlog", methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        uname = request.form['uname']
        password = request.form['password']

        session['uname'] = uname

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "select * from user where uname='" +
            uname +
            "' and password='" +
            password +
            "'"
        )

        data = cursor.fetchone()

        if data is None:
            return "user name and password incorrect"

        else:
            return render_template("userhome.html", data=[data])

@app.route("/fileupload", methods=['GET', 'POST'])
def fileupload():
    if request.method == 'POST':

        name = request.form['name']
        army_text = request.form['message']

        f = request.files['file']

        f.save("static/uploads/" + secure_filename(f.filename))

        key1 = secrets.token_hex(4)

        input_image_path = "static/uploads/" + secure_filename(f.filename)

        output_image_path = "static/uploads/" + str(key1) + "face.jpg"

        detect_and_crop_head(input_image_path, output_image_path)

        res = ''.join(format(ord(i), '08b') for i in army_text)

        decoded_text = decode_text_from_image(input_image_path)

        if len(decoded_text) > 1:

            res2 = ""

            encode_text_to_image(
                str(res2),
                input_image_path,
                "static/uploads/" + str(key1) + "encoded_image.png"
            )

            res1 = ''.join(format(ord(i), '08b') for i in army_text)

            encode_text_to_image(
                str(res1),
                input_image_path,
                "static/uploads/" + str(key1) + "encoded_image.png"
            )

        else:

            encode_text_to_image(
                str(res),
                input_image_path,
                "static/uploads/" + str(key1) + "encoded_image.png"
            )

        conn = get_db_connection()

        cursor = conn.cursor()

        key2 = secrets.token_hex(4)

        cursor.execute(
            "insert into filetrans(uname,image,message,key1,key2,fimage,bstr) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (
                name,
                secure_filename(f.filename),
                army_text,
                key1,
                key2,
                output_image_path,
                str(res)
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            "result1.html",
            data1=res,
            data2=army_text,
            data3=input_image_path,
            data4=output_image_path
        )

@app.route("/verimg", methods=['GET', 'POST'])
def verimg():
    if request.method == 'POST':

        f = request.files['file']

        filename = secure_filename(f.filename)

        f.save("static/uploads/" + filename)

        input_image_path = "static/uploads/" + filename

        output_image_path = "static/uploads/cropped_" + filename

        detect_and_crop_head(input_image_path, output_image_path)

        decoded_text = decode_text_from_image(input_image_path)

        txt = decoded_text

        x = txt.split(',')

        def is_binary_string(s):
            unique_chars = {c for c in s}
            return unique_chars.issubset({'0', '1'})

        s = is_binary_string(x[0])

        if s == True:

            b = x[0]

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM filetrans where bstr='" + str(x[0]) + "'"
            )

            data = cur.fetchall()

            if not data:
                status = "Fake"

            else:
                status = "Real"

            return render_template(
                "result.html",
                data1=status,
                data2='',
                data3=input_image_path,
                data4=output_image_path
            )

        else:

            status = "Fake Image No Binary code Detected"

            return render_template(
                "result.html",
                data1=status,
                data2=decoded_text,
                data3=input_image_path,
                data4=output_image_path
            )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
