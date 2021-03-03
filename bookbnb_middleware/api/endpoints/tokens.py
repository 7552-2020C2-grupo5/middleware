from flask_restx import Namespace, Resource

from bookbnb_middleware.constants import BOOKBNB_TOKEN
from bookbnb_middleware.api.models.tokens_models import server_token_model, error_model
from bookbnb_middleware.exceptions import (
    InvalidEnvironment,
    ServerTokenError,
    UnsetServerToken,
)

from bookbnb_middleware.api.handlers.tokens_handlers import add_env_var, remove_env_var

ns = Namespace(
    name="Server tokens",
    path="/bookbnb/token",
    description="Register server tokens",
)

ns.models[server_token_model.name] = server_token_model
ns.models[error_model.name] = error_model


@ns.route('')
class ServerTokenResource(Resource):
    @ns.doc('add_server_token')
    @ns.expect(server_token_model)
    @ns.response(200, "Server token removed")
    @ns.response(code=403, model=error_model, description="Invalid environment")
    @ns.response(code=500, model=error_model, description="Error processing request")
    def post(self):
        """Register server token."""
        try:
            data = ns.payload
            add_env_var(BOOKBNB_TOKEN, data.get("token"))
            return {"message": "success"}, 200
        except InvalidEnvironment:
            return {"message": "Invalid environment"}, 403
        except ServerTokenError as e:
            ns.logger.error("Error setting server token", exc_info=e)
            return {"message": f"{e}"}, 500

    @ns.response(200, "Server token removed")
    @ns.response(code=400, model=error_model, description="Error when removing")
    @ns.response(code=403, model=error_model, description="Invalid environment")
    @ns.response(code=500, model=error_model, description="Error processing request")
    @ns.doc('remove_server_token')
    def delete(self):
        """Remove set server token."""
        try:
            remove_env_var(BOOKBNB_TOKEN)
            return {"message": "success"}, 200
        except InvalidEnvironment:
            return {"message": "Invalid environment"}, 403
        except UnsetServerToken:
            return {"message": "server token was not set"}, 400
        except ServerTokenError as e:
            ns.logger.error("Error deleting server token", exc_info=e)
            return {"message": "Internal error"}, 500
