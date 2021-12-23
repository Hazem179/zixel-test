from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from nlp.tags_extraction import tags_extraction



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp/lite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)

class Software(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(70),nullable=False)
    description = db.Column(db.String(255),nullable=False)
    tags = db.Column(db.JSON,nullable=True)

    def __init__(self,title,description,tags):
        self.title = title
        self.description = description
        self.tags=tags


class SoftwareSchema(ma.Schema):
    class Meta:
        fields = ("id","title","description","tags")

software_schema = SoftwareSchema()
softwares_schema = SoftwareSchema(many=True)


############################################################################################################################################################
#####################################################################################################################
##############################################################################


@app.route('/software',methods=["POST"])
def create_software():
    title = request.json["title"]
    description = request.json["description"]
    tags = request.json['tags']
    tags = tags_extraction(description)
    new_software = Software(title, description, tags)
    db.session.add(new_software)
    db.session.commit()
    return software_schema.jsonify(new_software)


@app.route('/softwares',methods=["GET"])
def get_softwares():
    softwares = Software.query.all()
    serialized_result = softwares_schema.dump(softwares)
    return jsonify(serialized_result)

@app.route('/software/<id>',methods=["GET"])
def get_software_by_id(id):
    software = Software.query.get(id)
    serialized_result = jsonify(software_schema.dump(software))
    return serialized_result


@app.route('/software/<id>',methods=["PUT"])
def update_software(id):
    software = Software.query.get(id)
    title = request.json["title"]
    description = request.json["description"]
    software.title = title
    software.description = description
    db.session.commit()
    serialized_result = jsonify(software_schema.dump(software))
    return serialized_result


@app.route("/softwares/<id>",methods = ["DELETE"])
def delete_software(id):
    software = Software.query.get(id)
    db.session.delete(software)
    db.session.commit()
    serialized_result = jsonify(software_schema.dump(software))
    return serialized_result
if __name__ == '__main__':
    app.run()
