from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_jwt_claims,
)

from tools.errors import AuthException
from tools.utils import Role

JWT = JWTManager()


@JWT.user_claims_loader
def add_claims_to_access_token(user):
    return {"aud": str(user.role)}


@JWT.user_identity_loader
def user_identity_lookup(user):
    return user.id


def scoped(scope: Role):
    def fn_wrap(fn):
        def arg_wrap(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            user_roles = Role.from_str(claims.get("aud")).full()

            if scope not in user_roles:
                raise AuthException("Insufficient scope", code=403)
            return fn(*args, **kwargs)

        return arg_wrap

    return fn_wrap


def check_scope_claims(claims, scope_required):
    assert claims.issuperset(list(Role)[list(Role).index(scope_required) :])
