from flask import session, render_template, redirect, url_for, flash, Blueprint, request , abort
from models.helper_functions import (
    get_article_by_id,
    check_in_articles,
    addArticleToDatabase,
    getArticlesData,
    get_user_Data,
    get_user_likes,
    saveImage,
    check_in_likes,
    add_like,
    remove_like,
    filter_articles_by_name,
    get_user_articles,
    remove_article_by_id
)
from forms import AddArticles, updateArticle

articles = Blueprint('articles', __name__,
                     template_folder='../templates', static_folder='../static')


@articles.route('/articles/<int:article_id>')
def article(article_id):
    if 'name' in session and 'password' in session:
        user_Data = get_user_Data(session['name'] , session['password'])



        article = get_article_by_id(article_id)


        if article is None :
            return abort(404)


        article_image = article['article_image']
        article_name = article['article_name']
        article_content = article['article_content']
        return render_template('article.html', title=article_name, article_name=article_name, article_image=article_image, article_content=article_content, logout=True, has_bg=False, delete_acc=True,  update_account=True, user_image=user_Data['user_profile_image'], search_icon=False)
    else:
        raise PermissionError('you need to login first')


@articles.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if not 'name' in session and not 'password' in session:
        raise PermissionError('you need to login first')

    form = AddArticles()
    user_Data = get_user_Data(session['name'] , session['password'])


    if form.validate_on_submit():
        articleName = form.article_name.data
        articleBio = form.article_bio.data
        articleImg = form.article_img.data

        if check_in_articles(articleName, articleBio):
            flash('This Article Is Already Exists', 'danger')
        else:
            Imagename = saveImage(articleImg)
            addArticleToDatabase(articleName, articleBio, Imagename)
            flash('Article Successfully Added', 'success')
            return redirect(url_for('articles.articles_page'))

    return render_template('add_article.html', title='Add Article', login=False, signUp=False, currentRoute='add_article', logout=True, has_bg=False, delete_acc=True, form=form, limit=10,  update_account=False, user_image=user_Data['user_profile_image'], search_icon=False)


@articles.route('/', methods=['GET', 'POST'])
@articles.route('/articles', methods=['GET', 'POST'])
def articles_page():

    if 'name' in session and 'password' in session:
        articles = getArticlesData()
        user_Data = get_user_Data(session['name'], session['password'])
        user_id = user_Data.get('user_id') if user_Data else None
        if user_id is None:
            return redirect(url_for('auth.delete_account'))
        user_likes = get_user_likes(user_id)
        user_articles_ids = [lst['article_id'] for lst in user_likes]
        user_created_articles = get_user_articles(user_id)
        user_created_articles_ids = list(map(lambda article : article.get('id') , user_created_articles))


        if request.method == 'POST':
            searchFormValue = request.form['search']
            articles_ = filter_articles_by_name(searchFormValue)

            return render_template('articles.html', css_file='article.css', title='Articles', add_articles=True, login=False, signUp=False, logout=True, user_image=user_Data['user_profile_image'], has_bg=False, delete_acc=True, articles=articles_, user_likes=user_articles_ids, search=searchFormValue,  update_account=True, search_icon=True, user_created_articles_ids=user_created_articles_ids)

        if 'action' in request.args and 'article_id' in request.args:
            action = request.args['action']
            article_id = request.args['article_id']

            user_Data = get_user_Data(session['name'], session['password'])
            user_id = user_Data.get('user_id') if user_Data else None

            if user_id is None:
                return redirect(url_for('auth.delete_account'))

            if action == 'add_like':
                if not check_in_likes(user_id, article_id):
                    add_like(user_id, article_id)
                else:
                    remove_like(user_id, article_id)

            return redirect(url_for('articles.articles_page'))

        user_Data = get_user_Data(session['name'], session['password'])
        return render_template('articles.html',
                                css_file='article.css',
                                title='Articles',
                                add_articles=True,
                                login=False,
                                signUp=False,
                                logout=True,
                                user_image=user_Data['user_profile_image'],
                                has_bg=False,
                                delete_acc=True,
                                articles=articles,
                                user_likes=user_articles_ids,
                                update_account=True,
                                user_created_articles_ids=user_created_articles_ids,
                                search_icon=True)

    articles = getArticlesData(limit=10)

    return render_template('articles.html', css_file='article.css', title='Articles', limit=10, login=True, signUp=True, logout=False, has_bg=False, delete_acc=False, articles=articles, update_account=False)


@articles.route('/articles/remove/<int:article_id>')
def remove_article(article_id):
    if 'name' in session and 'password' in session:
        #check if article is yours
        user_id = get_user_Data(session['name'] , session['password'])['user_id']
        article = get_article_by_id(article_id)
        user_articles_data = get_user_articles(user_id)

        if article:
            if article in user_articles_data:
                #delete article
                remove_article_by_id(article_id , user_id)
                flash('removed article successfully!', category='success')
                return redirect(url_for('articles.articles_page'))
            else:
                raise PermissionError('you can\'t delete this article because it\'s not yours')
        else:
            raise PermissionError('article not found or you don\'t have permission to delete it')

    else:
        raise PermissionError('you don\'t have permission to use this page')

#i need to complete this update articles it's not ended yet
@articles.route('/update_article/<int:article_id>' , methods = ['GET' , 'POST'])
def update_article(article_id):
    #check if article is exists and you who created it
    user_id = get_user_Data(session['name'], session['password'])['user_id']
    article = get_article_by_id(article_id)
    user_articles_data = get_user_articles(user_id)

    if article:

        if article in user_articles_data:
            article_name = article['article_name']
            article_bio  = article['article_content']



            form = updateArticle()
            return render_template('update_article.html', 
                                    title='Update Article',
                                    login=False, 
                                    signUp=False,
                                    currentRoute='update_article', 
                                    logout=True,
                                    has_bg=False, 
                                    delete_acc=True,
                                    form=form,  
                                    update_account=False , 
                                    search_icon=False,
                                    article_name = article_name,
                                    article_bio = article_bio)
        else:
            raise PermissionError('you can\'t delete this article because it\'s not yours')


    else:
        return abort(404)