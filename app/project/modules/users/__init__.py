import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource

from project.extensions import db

from project.modules.utils import authenticate_restful, is_admin

from .models import Users as UsersModel

log = logging.getLogger(__name__)

users_blueprint = Blueprint('users', __name__)
users_api = Api(users_blueprint)


class Users(Resource):

    @authenticate_restful
    def get(self, token: str):
        """Get single user details"""
        response_object = {'status': 'fail', 'message': 'User does not exist'}
        log.debug(token)
        try:
            user = UsersModel.query.filter_by(id=token).first()
            log.debug(user)
            if not user:
                return response_object, HTTPStatus.NOT_FOUND
            else:
                response_object = {'status': 'success', 'data': user.to_json()}
                return response_object, HTTPStatus.OK
        except ValueError:
            return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object[
                'message'] = "There's an error while fetch user detail"
            log.error(e)
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR


class UsersList(Resource):

    @authenticate_restful
    def get(self, resp):
        """Get all users"""
        response_object = {
            'status': 'success',
            'users': [user.to_json() for user in UsersModel.query.all()]
        }
        return response_object, HTTPStatus.OK

    @authenticate_restful
    def post(self, resp):
        post_data = request.get_json()
        response_object = {'status': 'fail', 'message': 'Invalid payload'}
        if not is_admin(resp.id):
            response_object['message'] = \
                "You do not have permission to do that."
            return response_object, HTTPStatus.UNAUTHORIZED
        if not post_data:
            return response_object, HTTPStatus.BAD_REQUEST

        try:
            username = post_data.get('username')
            email = post_data.get('email')
            password = post_data.get('password')        

            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            log.error(e)

    # @authenticate_restful
    # def put(self, user):
    #     post_data = request.get_json()
    #     response_object = {'status': 'fail', 'message': 'Invalid payload'}
    #     if not is_admin(resp):
    #         response_object['message'] = \
    #             "You do not have permission to do that."
    #         return response_object, HTTPStatus.UNAUTHORIZED
    #     if not post_data:
    #         return response_object, HTTPStatus.BAD_REQUEST

    #     username = post_data.get('username')
    #     email = post_data.get('email')
    #     try:
    #         response_object = {
    #             'status': 'success',
    #             'message': f'{email} was added!'
    #         }
    #         return response_object, HTTPStatus.CREATED
    #     except Exception as e:
    #         log.error(e)


users_api.add_resource(Users, '/app/v1/users/<token>')
users_api.add_resource(UsersList, '/app/v1/users')
