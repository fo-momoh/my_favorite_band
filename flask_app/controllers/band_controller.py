from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band

#===========================DISPLAY ROUTES==========================

# Shows the create_band html
@app.route("/create/band")
def new():
    if "user_id" not in session:
        return redirect ("/welcome")
    # bands = Band.get_all_bands()
    logged_in_user = User.get_by_id({"id": session["user_id"]}) # We use this in order to get user in session.
    return render_template("create_band.html", user = logged_in_user) # user must is used in the html with jinja

# Shows the show_band html
@app.route("/show/bands")
def show_bands():
    if "user_id" not in session:
        return redirect ("/welcome")
    logged_in_user = User.get_band_of_user({"id": session["user_id"]}) #get_band _of_user is here because it will show the method that I wrote in user.py We will be able to see each band from each user.   
    return render_template("show_band.html", user = logged_in_user) # user is used in html with jinja.

# Renders the edit_band html, BUT also checks the get_one which gets the band by ID. Then in line 32 checks if the user in session will be able to modify the band.
@app.route('/edit/band/<int:id>')
def edit_band(id):
    if "user_id" not in session:
        return redirect('/welcome')
    bands = Band.get_one({ "id": id })
    if session["user_id"] != bands.user_id:
        return redirect('/welcome')
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("edit_band.html", band = bands, user=logged_in_user)


#========================ACTION ROUTES==========================

# Creates the band after validating it. We write the dictionary because we need the user_id in line 46 in order to know which user created the band.
@app.route('/new/band', methods = ["POST"])
def create_band():
    if not Band.band_validator(request.form):
        return redirect("/create/band")
    data= {
        "user_id": session["user_id"],
        "band_name": request.form["band_name"],
        "music_genre": request.form["music_genre"],
        "home_city": request.form["home_city"],
        }
    Band.create_band(data)
    return redirect ("/welcome")

# Updates the band after validating it.
@app.route('/update/band', methods = ["POST"])
def update():
    if "user_id" not in session:
        return redirect('/welcome')
    if Band.band_validator(request.form):
        Band.update_band(request.form)
        return redirect("/welcome")
    return redirect("/welcome")

# Deletes the band 
@app.route('/band/delete/<int:id>')
def delete_band(id):
    if "user_id" not in session:
        return redirect("/welcome")    
    data = { "id": id }
    Band.delete_band(data)
    return redirect("/welcome")


