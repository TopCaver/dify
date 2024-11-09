from flask_restful import Resource

from controllers.xinshu_plugin_api import api


class XinshuApi(Resource):
    def get(self):
        """
        For connection health check
        """
        return {"result": "OK!"}


api.add_resource(XinshuApi, "/test")