from flask_restful import Resource, reqparse
from libs.helper import StrLen, email, get_remote_ip
from libs.password import valid_password
from controllers.xinshu_plugin_api import api
from configs import dify_config
from services.account_service import TenantService, RegisterService,AccountStatus
import logging

class InviteApi(Resource):
    def get(self):
        """
        对外提供一个邀请链接
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=email, required=True, nullable=True, location="args")
        args = parser.parse_args()
        name = args["email"].split("@")[0]
        
        account = RegisterService.register(email=args['email'],name=name, language='zh-CN',status=AccountStatus.PENDING)
        tenant = TenantService.create_tenant(f"{account.name}'s Workspace")
        logging.info(f"[DIFY-xinshu-MT] Invite by API: account:{account.name}, tenant: {tenant.id}")
        TenantService.create_tenant_member(tenant, account, role="owner") 
        TenantService.switch_tenant(account, tenant.id)

        token = RegisterService.generate_invite_token(tenant,account)
        #http://127.0.0.1:3000/activate?email=test4@test.com&token=eece....2637
        invite_url = f"{dify_config.CONSOLE_WEB_URL}/activate?token={token}"
        logging.info(f"[DIFY-xinshu-MT] Invite by API: token:{token}")
        return {
            "token":token,
            "invite-url":invite_url
        }

api.add_resource(InviteApi, "/invite")