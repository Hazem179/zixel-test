from app import db,ma

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
