import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask_restx import Api, Resource

from project.modules.utils import authenticate_restful, is_admin
from project.extensions import db
from .models import Pubs as PubModel

log = logging.getLogger(__name__)
pubs_blueprint = Blueprint('pubs', __name__)
pubs_api = Api(pubs_blueprint)


class Pubs(Resource):

    @authenticate_restful
    def get(self, token: str):
        """Get single user details"""
        response_object = {'status': 'fail', 'message': 'Publication does not exist'}
        log.debug(token)
        try:
            pub = PubModel.query.filter_by(id=token).first()
            log.debug(user)
            if not pub:
                return response_object, HTTPStatus.NOT_FOUND
            else:
                response_object = {'status': 'success', 'data': pub.to_json()}
                return response_object, HTTPStatus.OK
        except ValueError:
            return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object[
                'message'] = "There's an error while fetch publication detail"
            log.error(e)
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR


class PubsList(Resource):

    # @authenticate_restful
    def get(self):
        """Get all pubs (publications) meta data"""
        response_object = {
            'status': 'success',
            'publications': [pub.to_json() for pub in PubModel.query.all()]
        }
        return response_object, HTTPStatus.OK

    # @authenticate_restful
    def post(self):

        post_data = request.get_json()

        pub_name = post_data['name']
        pub_author = post_data['author']
        pub_text = post_data['text']

        response_object = {'status': 'fail', 'message': 'Invalid payload'}
        
        # if not is_admin(resp.id):
        #     response_object['message'] = \
        #         "You do not have permission to do that."
        #     return response_object, HTTPStatus.UNAUTHORIZED

        if not pub_name or not pub_author or not pub_text:
            return response_object, HTTPStatus.BAD_REQUEST

        try:
            new_pub = PubModel(name=pub_name,author=pub_author,text=pub_text)
            db.session.add(new_pub)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'publication was added.'
            }
            return response_object, HTTPStatus.CREATED
        except Exception as e:
            log.error(e)


pubs_api.add_resource(Pubs, '/app/v1/pubs/<token>')
pubs_api.add_resource(PubsList, '/app/v1/pubs')
