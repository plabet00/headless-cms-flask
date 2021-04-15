from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from app import db
from app import Model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
models = []
for x in Model.query.all():
    x.content = x.content.replace("'","\"")
    models.append(json.loads(x.content))
model_classes = {}

for model in models:
    model_classes[model["model_name"]] = type(model["model_name"], (db.Model,), 
    {
        "id" : db.Column(db.Integer, primary_key=True)
    })
    for column in model["content"]:
        setattr(model_classes[model["model_name"]], column["name"], db.Column(db.String(80), unique=True, nullable=False))

print(models[0]["content"])
#for column in models[0]: