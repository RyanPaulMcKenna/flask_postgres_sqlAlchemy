import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource

from project.modules.utils import authenticate_restful, is_admin
from project.extensions import db
from .models import Files as FileModel
from io import StringIO
log = logging.getLogger(__name__)

files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)

class Files(Resource):

    @authenticate_restful
    def get(self, token: str):
        """Get single user details"""
        response_object = {'status': 'fail', 'message': 'File does not exist'}
        log.debug(token)
        try:
            file = FileModel.query.filter_by(id=token).first()
            log.debug(user)
            if not file:
                return response_object, HTTPStatus.NOT_FOUND
            else:
                response_object = {'status': 'success', 'data': file.to_json()}
                return response_object, HTTPStatus.OK
        except ValueError:
            return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object[
                'message'] = "There's an error while fetch file detail"
            log.error(e)
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR


class FilesList(Resource):

    # @authenticate_restful
    def get(self):
        """Get all file meta data"""
        response_object = {
            'status': 'success',
            'files': [file.to_json() for file in FileModel.query.all()]
        }
        return response_object, HTTPStatus.OK

    # @authenticate_restful
    def post(self):

        file_name = request.form['name']
        file_extension = request.form['extension']
        file_contents = request.form['upload']

        response_object = {'status': 'fail', 'message': 'Invalid payload'}
        
        # if not is_admin(resp.id):
        #     response_object['message'] = \
        #         "You do not have permission to do that."
        #     return response_object, HTTPStatus.UNAUTHORIZED

        if not file_contents or not file_name or not file_extension:
            return response_object, HTTPStatus.BAD_REQUEST

        try:

            a_byte_array = bytearray(file_contents, "utf8")

            new_file = FileModel(name=file_name,extension=file_extension,data=a_byte_array)
            db.session.add(new_file)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'file was added.'
            }
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            log.error(e)


files_api.add_resource(Files, '/app/v1/files/<token>')
files_api.add_resource(FilesList, '/app/v1/files')
