from flask import Flask, jsonify, request, render_template,session
from werkzeug.utils import secure_filename
import os
from pymongo import  errors
from werkzeug .security import generate_password_hash


from db import create_parent, update_parent,get_parents,get_parent_by_password_and_useridname,get_parent
# ,get_student_data_by_parent_useridname

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = "Technologies"

@app.route('/')
def home():
    return render_template('index.html')

# #get profile by userid
@app.route('/get_parent_data/<string:search_value>', methods=['GET'])
def fetch_parent_data(search_value):
    parent = get_parent(search_value)

    if parent:
        # Modify this part to select the specific fields you want to return
        parent_info = {
            "parent_name": parent.get("parent_name", ""),
            "parent_age": parent.get("parent_age", ""),
            "parent_gender": parent.get("parent_gender", ""),
            "parent_designation": parent.get("parent_designation", ""),
            "parent_description": parent.get("parent_description", ""),
            "parent_email": parent.get("personal_info", {}).get("contact", {}).get("parent_email", "")
        }
        return jsonify(parent_info)
    else:
        return jsonify({'error': 'User does not exist'}), 404





#get_parent_profile
@app.route('/get_parent_profile', methods=['GET','POST'])
def get_parent_profile():
    if request.method == 'GET':
        # Render the 'fetch.html' template when it's a GET request
        return render_template("fetch.html")
    

    parent_useridname = request.form.get("parent_useridname", '')
    parent_password = request.form.get("parent_password", '')
    print(parent_useridname,parent_password)

    session['parent_useridname'] = parent_useridname
    session_parent_useridname = session.get('parent_useridname', '')

    parent = get_parent_by_password_and_useridname(parent_password, parent_useridname)
    print(parent)

    #fetch child data
    # child_data=get_student_data_by_parent_useridname(parent_useridname)

    if parent:
        parent_info = {
            "parent_useridname": parent["parent_useridname"],
        "parent_hashed_password": parent["parent_hashed_password"],
        "parent_name": parent["parent_name"],
        "parent_age": parent["parent_age"],
        "parent_gender": parent["parent_gender"],
        "parent_image": parent["parent_image"],
        "parent_designation": parent["parent_designation"],
        "parent_description": parent["parent_description"],
        "parent_about": parent["personal_info"]["parent_about"],
        "parent_phone": parent["personal_info"]["contact"]["parent_phone"],
        "parent_email": parent["personal_info"]["contact"]["parent_email"],
        "parent_address": parent["personal_info"]["contact"]["parent_address"],
        # "child_name":child_data['student_name'],
        # "child_image":child_data["student_image"]
        }
        return jsonify(parent_info)
    else:
        return jsonify({'error': 'User does not exist'}), 404


#create parent profile
@app.route('/create_parent_profile', methods=['GET', 'POST'])
def create_parent_profile():
    try:
        parent_useridname=request.form.get("parent_useridname", '')
        parent_password=request.form.get("parent_password", '')
        parent_name = request.form.get('parent_name', '')
        parent_designation = request.form.get('parent_designation', '')
        parent_age = request.form.get('parent_age', '')
        parent_gender = request.form.get('parent_gender', '')
        
        parent_description = request.form.get('parent_description', '')
        parent_about = request.form.get('parent_about', '')
        parent_phone = request.form.get('parent_phone', '')
        parent_email = request.form.get('parent_email', '')
        parent_StreetAddress = request.form.get('parent_StreetAddress', '')
        parent_city=request.form.get('parent_city', '')
        parent_PostalCode=request.form.get('parent_PostalCode', '')
        parent_country=request.form.get('parent_country', '')
        parent_Apartment=request.form.get('parent_country', '')
        parent_state=request.form.get('parent_state', '')

    


        parent_image = request.files['file']
        data=get_parents()
        parent_hashed_password = generate_password_hash(parent_password)
        
        if parent_image:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(parent_image.filename))
            parent_image.save(filename)

        email_exists = any(item['personal_info']['contact']['parent_email'] == parent_email for item in data)
        phone_exists = any(item['personal_info']['contact']['parent_phone'] == parent_phone for item in data)
        useridname=any(item['parent_useridname'] == parent_useridname for item in data)

        if email_exists:
              return jsonify({"message": "This email is already exist"}), 400
        if phone_exists:
              return jsonify({"message": "This phone number is already exist"}), 400
        if useridname:
              return jsonify({"message": "This useridname is already exist"}), 400
        else:
            create_parent(parent_useridname,parent_hashed_password,parent_name, filename, parent_designation, parent_description, parent_about, parent_phone, parent_email, parent_StreetAddress,parent_age,parent_gender,parent_city,parent_PostalCode,parent_country,parent_Apartment,parent_state)

        return jsonify({"message": "Parent profile created successfully"}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500



#update parent info
@app.route('/update_parent/<string:useridname>', methods=['PUT', 'POST'])
def update_parent_profile(useridname):
    parent_data = get_parent(useridname)
    print(parent_data)
    if not parent_data:
        return jsonify({"error": "Parent not found"}), 404
    # Update parent information based on the received data

    # Example: Update the 'parent_name', 'parent_designation', and 'parent_description'
    parent_data['parent_useridname'] = request.form.get('parent_useridname', parent_data['parent_useridname'])
    parent_data['parent_name'] = request.form.get('parent_name', parent_data['parent_name'])
    parent_data['parent_designation'] = request.form.get('parent_designation', parent_data['parent_designation'])
    parent_data['parent_description'] = request.form.get('parent_description', parent_data['parent_description'])
    parent_data['parent_age'] = request.form.get('parent_age', parent_data['parent_age'])
    parent_data['parent_gender'] = request.form.get('parent_gender', parent_data['parent_gender'])
    # Example: Update the 'parent_about', 'parent_phone', 'parent_email', and 'parent_address' within 'personal_info'
    parent_data['personal_info']['parent_about'] = request.form.get('parent_about', parent_data['personal_info']['parent_about'])
    parent_data['personal_info']['contact']['parent_phone'] = request.form.get('parent_phone', parent_data['personal_info']['contact']['parent_phone'])
    parent_data['personal_info']['contact']['parent_email'] = request.form.get('parent_email', parent_data['personal_info']['contact']['parent_email'])


    parent_data['personal_info']['contact']['parent_address']['parent_country'] = request.form.get('parent_country', parent_data['personal_info']['contact']['parent_address']['parent_country'])

    parent_data['personal_info']['contact']['parent_address']['parent_state'] = request.form.get('parent_state', parent_data['personal_info']['contact']['parent_address']['parent_state'])

    parent_data['personal_info']['contact']['parent_address']['parent_city'] = request.form.get('parent_city', parent_data['personal_info']['contact']['parent_address']['parent_city'])

    parent_data['personal_info']['contact']['parent_address']['parent_StreetAddress'] = request.form.get('parent_StreetAddress', parent_data['personal_info']['contact']['parent_address']['parent_StreetAddress'])

    parent_data['personal_info']['contact']['parent_address']['parent_Apartment'] = request.form.get('parent_Apartment', parent_data['personal_info']['contact']['parent_address']['parent_Apartment'])

    parent_data['personal_info']['contact']['parent_address']['parent_PostalCode'] = request.form.get('parent_PostalCode', parent_data['personal_info']['contact']['parent_address']['parent_PostalCode'])

    # Example: Handle file uploads 
    parent_image = request.files['file']
    if parent_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(parent_image.filename))
        parent_image.save(filename)
        parent_data['parent_image'] = filename

     # Update password if provided
    new_password = request.form.get('new_password')
    if new_password:
        # You may want to add validation and hashing here
        parent_data['parent_hashed_password'] = generate_password_hash(new_password)

    # Save the updated parent data 
    update_parent(parent_data)

    return jsonify({"message": "Parent information updated successfully"}), 200



if __name__ == '__main__':
    app.run(debug=True)