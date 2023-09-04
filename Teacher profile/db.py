from bson import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
profile_db = client.get_database('ProfileApp')

teacher_profile_collection = profile_db.get_collection('teacherProfile')

def create_teacher(user_data):
    teacher_profile_collection.create_index([('profile.useridname_password.userid_name', 1)], unique=True)
    teacher_profile_collection.create_index([('profile.contact.phone', 1)], unique=True)
    teacher_profile_collection.create_index([('profile.contact.email', 1)], unique=True)

    hashed_password = generate_password_hash(user_data['profile']['useridname_password']['password'])
    # print("Hashed pass:",hashed_password)

    teacher_profile_collection.insert_one({
        'username': user_data['username'],
        'languages': user_data['languages'],
        'user_image': user_data['user_image'],

        'profile': {
            'status': {
                'user_designation': user_data['profile']['status']['user_designation'],
                'user_description': user_data['profile']['status']['user_description']
            },
            'about': user_data['profile']['about'],
            'useridname_password': {
                'userid_name': user_data['profile']['useridname_password']['userid_name'],
                'password': hashed_password
            },
            'contact': {
                'phone': user_data['profile']['contact']['phone'],
                'email': user_data['profile']['contact']['email'],
                'address': {
                    'house_no': user_data['profile']['contact']['address']['house_no'],
                    'street': user_data['profile']['contact']['address']['street'],
                    'postal_code': user_data['profile']['contact']['address']['postal_code'],
                    'city': user_data['profile']['contact']['address']['city'],
                    'state': user_data['profile']['contact']['address']['state']
                }
            }
        }
    })

def get_teachers():
    return list(teacher_profile_collection.find({}))

def get_teacher(user_id):
    # user = teacher_profile_collection.find_one({'_id': ObjectId(user_id)})
    user = teacher_profile_collection.find_one({'_id': ObjectId(user_id)})
    return user if user else None

def update_teacher(user_id, user_data):

    hashed_password = generate_password_hash(user_data['profile']['useridname_password']['password'])

    teacher_profile_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'username': user_data['username'],
            'languages': user_data['languages'],
            'user_image': user_data['user_image'],

            'profile': {
                'status': {
                    'user_designation': user_data['profile']['status']['user_designation'],
                    'user_description': user_data['profile']['status']['user_description']
                },
                'about': user_data['profile']['about'],
                'useridname_password': {
                    'userid_name': user_data['profile']['useridname_password']['userid_name'],
                    'password': hashed_password
                },
                'contact': {
                    'phone': user_data['profile']['contact']['phone'],
                    'email': user_data['profile']['contact']['email'],
                    'address': {
                        'house_no': user_data['profile']['contact']['address']['house_no'],
                        'street': user_data['profile']['contact']['address']['street'],
                        'postal_code': user_data['profile']['contact']['address']['postal_code'],
                        'city': user_data['profile']['contact']['address']['city'],
                        'state': user_data['profile']['contact']['address']['state']
                    }
                }
            }
        }}
    )
