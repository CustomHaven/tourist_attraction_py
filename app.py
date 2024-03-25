import os
from flask import Flask, render_template, request, redirect, url_for
from locations import Locations
# Q13 import forms.py
from forms import AddLocationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'

visit = Locations()

categories = {"recommended": "Recommended", "tovisit": "Places To Go", "visited": "Visited!!!", }

UP_ACTION = "\u2197"
DEL_ACTION = "X"

@app.route("/<category>", methods=["GET", "POST"])
def locations(category):
  # category = u
  print("locations route", category)
  locations = visit.get_list_by_category(category)
  # Q13 instance off AddLocationForm()
  add_location = AddLocationForm()
  ## Check the request for form data and process Q9
  if request.method == "POST":
    # Q10 assign tuple in list of name and action to the form data
    # [(name, action)] = [(None, None)]
    [(name, action)] = request.form.items()

    if action == UP_ACTION:
      visit.moveup(name)
    elif action == DEL_ACTION:
      visit.delete(name)
  ## Return the main template with variables
  # Q1 add render_template url html
  # Q2 assign variables
  # Q13 add add_location
  return render_template("locations.html", template_category=category, template_categories=categories, template_locations=locations, template_add_location=add_location)

@app.route("/add_location", methods=["POST"])
def add_location():
  ## Validate and collect the form data Q19 add_form & the if statement
  add_form = AddLocationForm(csrf_enable=False)
  if add_form.validate_on_submit():
      name= add_form.name.data
      description= add_form.description.data
      category= add_form.category.data
      visit.add(name, description, category)

  ## Redirect to locations route function Q21
  return redirect(url_for("locations", category=category, _external=True, _scheme="https" if os.environ["ENV"] == "prod" else "http"))

@app.route("/")
def index():
  print("Inside index page")

  ## Redirect to locations route function Q21
  return redirect(url_for("locations", category="recommended", _external=True, _scheme="https" if os.environ["ENV"] == "prod" else "http"))