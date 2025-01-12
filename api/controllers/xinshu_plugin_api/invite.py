import logging

from flask_restful import Resource, reqparse

from configs import dify_config
from controllers.xinshu_plugin_api import api
from libs.helper import email
from services.account_service import Account, AccountStatus, RegisterService, TenantService


class InviteApi(Resource):
    def get(self):
        """
        对外提供一个邀请链接
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=email, required=True, nullable=True, location="args")
        args = parser.parse_args()
        reg_email = args["email"]
        name = reg_email.split("@")[0]
        account = Account.query.filter_by(email=reg_email).first()

        if not account:
            account = RegisterService.register(email=reg_email, name=name, 
                                               language='zh-Hans', status=AccountStatus.PENDING)
            tenant = TenantService.create_tenant(f"{account.name}'s Workspace")
            logging.info(f"[DIFY-xinshu-MT] Invite by API: account:{account.name}, tenant: {tenant.id}")
            TenantService.create_tenant_member(tenant, account, role="owner") 
            TenantService.switch_tenant(account, tenant.id)

            token = RegisterService.generate_invite_token(tenant, account)
            # http://127.0.0.1:3000/activate?email=test4@test.com&token=eece....2637
            invite_url = f"{dify_config.CONSOLE_WEB_URL}/activate?token={token}"
            logging.info(f"[DIFY-xinshu-MT] Invite by API: token:{token}")
            return {
                "result": "success",
                "token": token,
                "invite-url": invite_url
            }
        else:
            return {
                "result": "faild",
                "error": "邮箱已经存在"
            }


api.add_resource(InviteApi, "/invite")