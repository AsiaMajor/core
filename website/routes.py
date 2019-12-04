from flask import Blueprint, render_template, current_app

website_routes = Blueprint('website', __name__, template_folder='templates', static_folder='static', static_url_path='')

#Main app routes
@website_routes.route('/')
def IndexController():
    # data = {
    #     'backend_url' : current_app.config["BACKEND_URL"],
    # }
    return render_template('index.html')