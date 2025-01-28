import os
from flask import session , render_template , redirect , url_for  , flash , Blueprint
from models.helper_functions import check_in_data, add_user_to_database, get_user_Data, saveUserProfile, update_Account, check_unique_name , check_user_in_data
from forms import SignForm , LoginForm , updateAccount
from db import db

auth = Blueprint('auth' , __name__ , template_folder='../template' , static_folder='../static')




@auth.route("/signUp", methods=['GET', 'POST'])
def sign_up():
    if 'name' in session and 'password' in session :
        if check_user_in_data(session.get('name') , session.get('password')):
            raise PermissionError('you already logged in')

    form = SignForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if not check_in_data(username, password):
            add_user_to_database(username, password)
            flash('You Have Created An Account', 'success')
            return redirect(url_for('articles.articles_page'))
        else:
            flash('This Account Is Already Exists', 'danger')

    return render_template('signup.html', form=form, css_file='form.css', title='Sign up', login=True, signUp=True,  currentRoute='sign_up', logout=False, has_bg=True, delete_acc=False, limit=10)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'name' in session and 'password' in session :
        if check_user_in_data(session.get('name') , session.get('password')):
            raise PermissionError('you already logged in')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # check is username and password in database
        if check_in_data(username, password):
            session['name'] = username
            session['password'] = password
            flash('You Have Successfully Logged In', 'success')
            return redirect(url_for('articles.articles_page'))
        else:
            flash('Check The Username Or Password', 'danger')

    return render_template('login.html', form=form,  css_file='form.css', title='Login', login=True, signUp=True, currentRoute='login_page', logout=False, has_bg=True, delete_acc=False, limit=10,  update_account=False)


@auth.route("/logout")
def logout():
    if 'name' in session and 'password' in session :
        if check_user_in_data(session.get('name') , session.get('password')):
            session.clear()
            return redirect(url_for('auth.login_page'))
    else:
        return redirect(url_for('auth.articles_page'))


@auth.route('/delete_account')
def delete_account():
    if 'name' in session and 'password' in session :
        if check_user_in_data(session.get('name') , session.get('password')):
            # get account from session
            name = session['name']
            password = session['password']

            # delete account from database
            with db.get_connection() as cnx:
                cursor = cnx.cursor(dictionary=True)
                cursor.execute(
                    'DELETE FROM users WHERE username = %s AND password= %s', (name, password))
                cnx.commit()

            # remove account from session
            session.clear()


            flash('You Have Deleted Your Account', category='success')

            # back to the login page

            return redirect(url_for('auth.login_page'))

    else:
        flash('You Don\'t Logged In To Delete Your Account' , category='danger')
        return redirect(url_for('articles.articles_page'))


@auth.route('/update_account' , methods = ['GET' , 'POST'])
def update_account():

    if 'name' in session and 'password' in session :
        if check_user_in_data(session.get("name") , session.get("password")):
            user_Data = get_user_Data(session['name'] , session['password'])

            form = updateAccount()





            if form.validate_on_submit():
                username = form.username.data
                userImage = form.userImage.data
                password = form.password.data

                #updata user data
                if user_Data['username'] == username and user_Data['password'] == password and userImage is None :
                    flash('The username and password is the same' , category='danger')

                else:



                    if user_Data['username'] != username : 
                        if check_unique_name(username):
                            if userImage:
                                if user_Data['user_profile_image']:
                                    os.remove(os.path.join(f'static/{user_Data["user_profile_image"] }'))
                                imageName = saveUserProfile(userImage)
                                update_Account(username , password , 'imgs/account_imgs/' + imageName)
                                session['name'] = username
                                session['password'] = password
                                flash('Updated Account Data Successfully' , category='success')
                                return redirect(url_for('articles.articles_page'))
                            else:
                                update_Account(username , password)
                                session['name'] = username
                                session['password'] = password
                                flash('Updated Account Data Successfully WITH OUT IMAGE',
                                    category='success')
                                return redirect(url_for('articles.articles_page'))
                        else:
                            flash('username is used before try unique one' , category='danger')
                    else:
                        if userImage:
                            if user_Data['user_profile_image'] :
                                os.remove(os.path.join(f'static/{user_Data["user_profile_image"] }'))
                            imageName = saveUserProfile(userImage)
                            update_Account(username, password,
                                        'imgs/account_imgs/' + imageName)
                            session['name'] = username
                            session['password'] = password
                            flash('Updated Account Data Successfully' , category='success')
                            return redirect(url_for('articles.articles_page'))
                        else:
                            update_Account(username , password)
                            session['name'] = username
                            session['password'] = password
                            flash('Updated Account Data Successfully WITH OUT IMAGE',
                                category='success')
                            return redirect(url_for('articles.articles_page'))

            return render_template(
                'updateAccount.html',
                form=form,
                user_Data=user_Data,
                title='Update Account',
                add_articles=True,
                login=False,
                sign_up=False,
                logout=True,
                has_bg=False,
                delete_account=True,
                update_account=False,
                user_image=user_Data['user_profile_image']
            )

    else:
        raise PermissionError('you need to login first to update your account')
