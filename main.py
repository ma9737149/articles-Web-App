from flask import Flask, render_template
from markupsafe import Markup
from flask_ckeditor import CKEditor
from view import *
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
ckeditor = CKEditor(app)


app.register_blueprint(articles)
app.register_blueprint(auth)






@app.template_filter()
def convertToHTML(st):
    return Markup(st)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_page.html')

@app.errorhandler(PermissionError)
def permission_error(error):
    return render_template('perm_error.html' , error = error)


if __name__ == "__main__":
    app.run(debug=True)
