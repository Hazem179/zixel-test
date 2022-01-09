from app import app, db
from flask import request, jsonify, Blueprint
from products.models import Software, software_schema, softwares_schema
from nlp.tags_extraction import tags_extraction

software = Blueprint('software', __name__)



@software.route('/software', methods=["POST"])
def create_software():
    title = request.json["title"]
    description = request.json["description"]
    tags = tags_extraction(description)
    new_software = Software(title, description, tags)
    db.session.add(new_software)
    db.session.commit()
    return software_schema.jsonify(new_software)


@software.route('/softwares', methods=["GET"])
def get_software_list():
    software_list = Software.query.all()
    serialized_result = softwares_schema.dump(software_list)
    return jsonify(serialized_result)


@app.route('/software/<id>', methods=["GET"])
def get_software_by_id(id):
    chosen_software = Software.query.get(id)
    serialized_result = jsonify(software_schema.dump(chosen_software))
    return serialized_result


@software.route('/software/<id>', methods=["PUT"])
def update_software(id):
    chosen_software = Software.query.get(id)
    title = request.json["title"]
    description = request.json["description"]
    chosen_software.title = title
    chosen_software.description = description
    db.session.commit()
    serialized_result = jsonify(software_schema.dump(chosen_software))
    return serialized_result


@software.route("/softwares/<id>", methods=["DELETE"])
def delete_software(id):
    chosen_software = Software.query.get(id)
    db.session.delete(chosen_software)
    db.session.commit()
    serialized_result = jsonify(software_schema.dump(chosen_software))
    return serialized_result
