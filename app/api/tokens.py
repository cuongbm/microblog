from flask import g, jsonify

from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import Token


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = Token.get_token(g.current_user)
    db.session.commit()
    return jsonify({'token': token.token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    print(g.current_token)