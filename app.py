from flask import Flask, render_template, request, redirect, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGOURI", "mongodb://localhost:27017/contact_manager")
app.config["SECRET_KEY"] = os.getenv("SECRETKEY") or os.urandom(32)
mongo = PyMongo(app)
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        contacts = mongo.db.Contacts.find()
        return render_template("index.html", contacts = contacts)
@app.route("/delete_flash")
def delete_flash():
    session.pop('_flashes', None)
    return redirect("/")
@app.route("/delete/<contact_id>")
def delete(contact_id):
    mongo.db.Contacts.delete_one({"_id": ObjectId(contact_id)})
    flash("Successfully deleted a contact")
    return redirect("/")
@app.route("/add", methods = ["POST"])
def add():
    print(request.form)
    if len(request.form["name"]) < 3:
        flash("Name cannot have less than 3 characters")
        return redirect("/")
    if mongo.db.Contacts.find_one({"name": request.form["name"], "phone": request.form["phone"], "email": request.form["email"]}):
        flash("Contact already exists, try another one")
        return redirect("/")
    document = {}
    document["name"] = request.form.get("name")
    document["phone"] = request.form.get("phone")
    document["email"] = request.form.get("email")
    mongo.db.Contacts.insert_one(document)
    flash("Successfully added a contact")
    return redirect("/")
if __name__ == "__main__":
    app.run(debug = True)