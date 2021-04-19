from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import json
from base64 import b64encode
import secrets
from flask_cors import CORS

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(240), unique=True, nullable=False)

    def __repr__(self):
        return '<Model %r>' % self.name

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.String(80), unique=False, nullable=False)
    data = db.Column(db.LargeBinary, unique=False, nullable=False)

db.create_all()

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("homepage.html")

@app.route("/createmodel", methods=["POST", "GET"])
def createform():
    all_models = Model.query.all()
    name = request.args.get('name')
    if request.method == "GET":
        if(name):
            return render_template("index.html",name = name)
        return render_template("createmodel.html",models = all_models)

@app.route("/createmodel/success", methods=["POST", "GET"])
def createdform():
    if request.method == "POST":
        data = request.form.to_dict(flat=False)
        data_dict_keys = list(data.keys())
        print(data)
        data_dict_keys.remove("name")
        content = []
        for x in data_dict_keys:
            content.append({"name" : data[x][0], "type" : x})
        data_dict = {"model_name": data["name"][0], "content" : content}
        entry = Model(content = str(data_dict), name = data["name"][0])
        db.session.add(entry)
        db.session.commit()
        return "Success"
    else:
        return "Hello"

@app.route("/createinstance", methods=["POST", "GET"])
def createinstance():
    all_models = Model.query.all()
    name = request.args.get('name')
    if(name):
        model = Model.query.filter_by(name = name).first()
        model.content = model.content.replace("'","\"")
        model_json = json.loads(model.content)
        types = []
        names = []
        for x in model_json["content"]:
            types.append(x["type"])
            names.append(x["name"])
        return render_template("createinstance_form.html", model_name = name, types = types, names = names)
    return render_template("createinstance.html",models = all_models)

@app.route("/createinstance/accepted", methods=["POST", "GET"])
def createinstanceaccepted():
    model_class = {}
    field_names = list(request.form.keys())[1:]
    model_class[request.form["model_name"]] = type(request.form["model_name"], (db.Model,), 
    {
        "id" : db.Column(db.Integer, primary_key=True, autoincrement=True),
        "__table_args__" : {'extend_existing': True}
    })
    for column in field_names:
        if not hasattr(model_class[request.form["model_name"]], column):
            if len(request.form.getlist(column)) > 1:
                if request.form.getlist(column)[1] == "Text":
                    setattr(model_class[request.form["model_name"]], column, db.Column(db.String(80), unique=False, nullable=False))
                elif request.form.getlist(column)[1] == "Number":
                    setattr(model_class[request.form["model_name"]], column, db.Column(db.Integer, unique=False, nullable=False))
            else:
                setattr(model_class[request.form["model_name"]], column, db.Column(db.String(80), unique=False, nullable=False))
    
    db.create_all()

    entry = model_class[request.form["model_name"]]()

    for column in field_names:
        random_token = secrets.token_hex(16)
        if len(request.form.getlist(column)) > 1:
            setattr(entry, column, request.form[column])
        else:
            image_entry = Image(image_name = column + random_token, data = request.files[column].read())
            db.session.add(image_entry)
            db.session.commit()
            setattr(entry, column, "/image/" + column + random_token)

    db.session.add(entry)
    db.session.commit()

    del model_class[request.form["model_name"]]
    del entry

    return field_names[0]

@app.route("/models", methods=["POST", "GET"])
def models():
    models = {"models":[]}
    for x in Model.query.all():
        models["models"].append(x.name)
    return json.dumps(models)

@app.route("/models/<model>", methods=["POST", "GET"])
def model(model):
    base_model = Model.query.filter_by(name = model).first()
    base_model.content = base_model.content.replace("'","\"")
    models = json.loads(base_model.content)
    field_names = []
    for x in models["content"]:
        field_names.append(x["name"])
    model_class = {}
    model_class[models["model_name"]] = type(models["model_name"], (db.Model,), 
    {
        "id" : db.Column(db.Integer, primary_key=True),
        "__table_args__" : {'extend_existing': True}
    })
    for column in field_names:
        if not hasattr(model_class[models["model_name"]], column):
            setattr(model_class[models["model_name"]], column, db.Column(db.String(80), unique=False, nullable=False))
    

    data = model_class[model].query.all()

    del model_class

    return_dict = {models["model_name"]: []}
    images = []
    for x in list(data[0].__dict__.keys()):
        if type(data[0].__dict__[x]) is bytes:
            images.append(x)

    for x in data:
        del x.__dict__["_sa_instance_state"]
        for i in images:
            x.__dict__[i] = b64encode(x.__dict__[i]).decode("ascii")
        return_dict[models["model_name"]].append(x.__dict__)

    return return_dict

@app.route("/image/<image_name>", methods=["POST", "GET"])
def get_image(image_name):
    image = Image.query.filter_by(image_name = image_name).first()
    base_64_image= b64encode(image.data).decode("ascii")
    return render_template("image.html", image = base_64_image)

if __name__ == "__main__":
    app.run(debug=True)
