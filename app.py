#!/usr/bin/env python
from flask import Flask, request
from flask_cors import CORS
from properties import *
from utils import add_headers, validate_req
from errors import *
import user_repo as repo
import logging, jwt
import bc_service as bc
import datetime

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route("/register", methods=['POST'])
def register():
    logging.info('REQUEST: ' + str(request))
    fields = ['username', 'password']
    if not validate_req(request, fields):
        logging.error(str(JSON_ERROR))
        return add_headers(JSON_ERROR, JSON_ERROR['code'])
    user = request.json
    existing_user = repo.get_by_name_and_pw(user['username'], user['password'])
    if existing_user:
        return add_headers(EXISTING_USER, EXISTING_USER['code'])
    id = repo.create_one(user)
    trx = bc.register_bc(str(id))
    user['_id'] = str(id)
    user['hash'] = trx
    print(user)
    return add_headers(user, OK)



@app.route("/login", methods=['POST'])
def login():
    logging.info('REQUEST: ' + str(request))
    fields = ['username', 'password']
    if not validate_req(request, fields):
        logging.error(str(JSON_ERROR))
        return add_headers(JSON_ERROR, JSON_ERROR['code'])
    credentials = request.json
    user = repo.get_by_name_and_pw(credentials['username'], credentials['password'])
    if not user:
        return add_headers(UNKNOWN_USER, UNKNOWN_USER['code'])
    user['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_TIME)
    token = jwt.encode(user, SECRET, algorithm=ALG)
    SUCCESS['token'] = token.decode("utf-8")
    return add_headers(SUCCESS, OK)


@app.route("/thanks", methods=['GET'])
def get_thanks():
    logging.info('REQUEST: ' + str(request))
    token = request.headers['Authorization']
    print(token)
    token_user = jwt.decode(token, SECRET, algorithms=ALG)

    print(token_user)

    id = token_user['_id']
    db_user = repo.get_by_id(id)
    if not db_user:
        return add_headers(UNKNOWN_USER, UNKNOWN_USER['code'])
    print(db_user['_id'])
    bc_user = bc.get_thank(db_user['_id'])
    bc_user['name'] = db_user['username']
    return add_headers(bc_user, OK)


@app.route("/users", methods=['GET'])
def get_users():
    return add_headers("OK", OK)


@app.route("/thanks", methods=['POST'])
def add_thanks():
    logging.info('REQUEST: ' + str(request))
    thank = request.json
    fields = ['message', 'type']
    if not validate_req(request, fields):
        logging.error(str(JSON_ERROR))
        return add_headers(JSON_ERROR, JSON_ERROR['code'])
    token = request.headers['Authorization']
    from_user = jwt.decode(token, SECRET, algorithms=ALG)
    id = request.args.get('id')
    if id:
       to_user = repo.get_by_id(id)
    else:
        name = request.args.get('name')
        if not name:
            # no name or ID in header
            return add_headers(UNKNOWN_USER, UNKNOWN_USER['code'])
        else:
            to_user = repo.get_by_name(name)
    if not to_user:
        return add_headers(UNKNOWN_USER, UNKNOWN_USER['code'])
    thank['name'] = from_user['username']
    res = bc.add_thank(to_user['_id'], thank)
    SUCCESS['hash'] = res
    return add_headers(SUCCESS, OK)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

