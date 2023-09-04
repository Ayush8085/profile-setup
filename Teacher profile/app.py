from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import os

from db import create_teacher, get_teacher, get_teachers, update_teacher

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_teachers', methods=['GET'])
def get_users():
    teachers = get_teachers()

    for teacher in teachers:
        teacher['_id'] = str(teacher['_id'])
        
    return jsonify(teachers)

@app.route('/get_teacher/<string:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = get_teacher(user_id)
    if user:
        user['_id'] = str(user['_id'])
    else:
        return jsonify({'error': 'User does not exists!!'})
    return jsonify(user)


@app.route('/create_teacher', methods=['GET', 'POST'])
def create_profile():
    username = request.form.get('username', '')
    languages = request.form.get('languages', '')

    user_image = request.files['file']
    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)

    user_designation = request.form.get('user_designation', '')
    user_description = request.form.get('user_description', '')

    about = request.form.get('user_about', '')

    userid_name = request.form.get('userid_name', '')
    password = request.form.get('password', '')
    if len(password) < 8:
        return jsonify({'error': 'Password must be from 8 characters!!'}), 404

    phone = request.form.get('phone', '')
    email = request.form.get('email', '')

    house_no = request.form.get('house_no', '')
    street = request.form.get('street', '')
    postal_code = request.form.get('postal_code', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')

    status = {
        'user_designation': user_designation,
        'user_description': user_description
    }

    useridname_password = {
        'userid_name': userid_name,
        'password': password
    }

    address = {
        'house_no': house_no,
        'street': street,
        'postal_code': postal_code,
        'city': city,
        'state': state
    }

    contact = {
        'phone': phone,
        'email': email,
        'address': address
    }

    profile = {
        'status': status,
        'about': about,
        'useridname_password': useridname_password,
        'contact': contact
    }

    user_data = {
        'username': username,
        'languages': languages,
        'user_image': filename,

        'profile': profile
    }

    create_teacher(user_data)

    return jsonify(user_data)


@app.route('/update_teacher/<string:user_id>', methods=['PUT', 'POST'])
def update_user_profile(user_id):
    user_data = get_teacher(user_id)

    if not user_data:
        return jsonify({"error": "User not found"}), 404


    username = request.form.get('username', user_data['username'])
    languages = request.form.get('languages', user_data['languages'])

    user_designation = request.form.get('user_designation', user_data['profile']['status']['user_designation'])
    user_description = request.form.get('user_description', user_data['profile']['status']['user_description'])

    about = request.form.get('user_about', user_data['profile']['about'])

    userid_name = request.form.get('userid_name',  user_data['profile']['useridname_password']['userid_name'])
    password = request.form.get('password',  user_data['profile']['useridname_password']['password'])

    phone = request.form.get('phone', user_data['profile']['contact']['phone'])
    email = request.form.get('email', user_data['profile']['contact']['email'])

    # address = request.form.get('address', user_data['personal_info']['contact']['address'])

    house_no = request.form.get('house_no', user_data['profile']['contact']['address']['house_no'])
    street = request.form.get('street', user_data['profile']['contact']['address']['street'])
    postal_code = request.form.get('postal_code', user_data['profile']['contact']['address']['postal_code'])
    city = request.form.get('city', user_data['profile']['contact']['address']['city'])
    state = request.form.get('state', user_data['profile']['contact']['address']['state'])

    address = {
        'house_no': house_no,
        'street': street,
        'postal_code': postal_code,
        'city': city,
        'state': state
    }

    user_image = request.files.get('file')
    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)

    status = {
        'user_designation': user_designation,
        'user_description': user_description
    }

    useridname_password = {
        'userid_name': userid_name,
        'password': password
    }

    address = {
        'house_no': house_no,
        'street': street,
        'postal_code': postal_code,
        'city': city,
        'state': state
    }

    contact = {
        'phone': phone,
        'email': email,
        'address': address
    }

    profile = {
        'status': status,
        'about': about,
        'useridname_password': useridname_password,
        'contact': contact
    }

    new_user_data = {
        'username': username,
        'languages': languages,
        'user_image': filename,

        'profile': profile
    }


    # update_teacher(user_id, username, filename, user_designation, user_description, about, phone, email, address, department, experience, specialization)
    update_teacher(user_id, new_user_data)

    updated_user = get_teacher(user_id)
    updated_user['_id'] = str(updated_user['_id'])

    return jsonify(updated_user)

if __name__ == '__main__':
    app.run(debug=True)