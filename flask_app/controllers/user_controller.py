from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band

# ------------------------DISPLAY ROUTES-------------------------

# principal route that takes us to the main site BUT REDIRECTS to welcome page if user is already in SESSION. So user can't go back to main page, he has to Logout.
@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/welcome")
    return render_template("index.html")

# second page that checks if a user is NOT in SESSION, welcome page won't be accessible for him.
@app.route("/welcome")
def welcome():
    if "user_id" not in session:
        return redirect("/") 
    data = { "id": session["user_id"] }
    logged_in_user = User.get_by_id(data) # This variable holds the information from the function and stores its ID in session. so we can use it later and deploy specific information from the user.
    all_bands = Band.get_all_bands() # Band is the class and it is calling the get_all_bands and displaying that info in Welcome page. FUNCTION was cerated in BAND.PY.
    return render_template("welcome.html", user = logged_in_user, all_bands = all_bands) # This is the way we can render more things on the template.


# ------------------------ACTION ROUTES-------------------------

# This route creates the user BUT checks first with our function REGISTRY_VALIDATOR if the user already exists.
@app.route("/users/create", methods=["POST"])
def create_user():
    if User.registry_validator(request.form): # the user gets validated and stored in SESSION, then it redirects him to the welcome page as a valid user.
        session["user_id"] = User.create(request.form)
        return redirect("/welcome")
    return redirect("/") # If the user does not meet the validation, he gets directed to the main page.
 
# This route is for a user to LOGIN 
@app.route("/login", methods=["POST"])
def login():
    if not User.login_validator(request.form): # Evaluates if the login does NOT meet the validations of email and password, checks if the user already exists in the DB.
        flash("Invalid Login")
        return redirect("/") # If it does not exists or didn't typed email and password correctly, it gets redirected to the same LOGIN page.
    user = User.get_by_email(request.form) # If the data typed is already in the DB (matches) SESSION holds its info and keeps it until he Logs Out. That way we can keep his info in the following pages.
    session["user_id"] = user.id
    return redirect("/welcome")

# Tis route is just to LogOut
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
