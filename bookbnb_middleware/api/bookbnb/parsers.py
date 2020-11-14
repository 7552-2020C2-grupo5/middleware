from flask_restx import reqparse

user_post_arguments = reqparse.RequestParser()
user_post_arguments.add_argument('name', type=str, required=True, help='user first name')
user_post_arguments.add_argument('last_name', type=str, required=True, help='user last name')
user_post_arguments.add_argument('mail', type=str, required=True)
