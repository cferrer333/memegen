from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Img, img_schema, imgs_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}

@api.route('/memes', methods = ['POST'])
@token_required
def create_meme(current_user_token):
    image = request.json['image']
    name = request.json['name']
    mimetype = request.json['mimetype'] 
    url = request.json['url']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    img = Img(image, name, mimetype, user_token, url)

    db.session.add(img)
    db.session.commit()

    response = img_schema.dump(img)
    return jsonify(response)

@api.route('/memes', methods = ['GET'])
@token_required
def get_memes(current_user_token):
    a_user = current_user_token.token
    imgs = Img.query.filter_by(user_token = a_user).all()
    response = imgs_schema.dump(imgs)
    return jsonify(response)

@api.route('/memes/<id>', methods = ['GET'])
@token_required
def get_single_meme(current_user_token, id):
    img = Img.query.get(id)
    response = img_schema.dump(img)
    return jsonify(response)
    
@api.route('/memes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_meme(current_user_token, id):
    img = Img.query.get(id)
    img.image = request.json['image']
    img.name = request.json['name']
    img.mimetype = request.json['mimetype']
    img.url = request.json['url']
    img.user_token = current_user_token.token

    db.session.commit()
    response = img_schema.dump(img)
    return jsonify(response)

@api.route('/memes/<id>', methods = ['DELETE'])
@token_required
def delete_meme(current_user_token, id):
    img = Img.query.get(id)
    db.session.delete(img)
    db.session.commit()
    response = img_schema.dump(img)
    return jsonify(response)