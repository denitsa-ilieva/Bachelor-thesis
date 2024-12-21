# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#from flask import Blueprint, render_template, request, redirect
#from users_mgt import User

from server import app, server
from flask_login import logout_user, current_user
from views import success, login, login_fd, logout 
from views.success import layout_function

#auth = Blueprint('auth', __name__)

header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link'),
		#html.A("Link to external site", href='https://my-dash-health.herokuapp.com/', target="_blank")
            ]),
	    html.Div([
		html.A("Link to external site", href='https://my-dash-health.herokuapp.com/', target="_blank"), 
		], className='eight columns', style={'margin':0}),
        ]
    )
)

app.layout = html.Div(
    [
        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/':
		return login.layout
	elif pathname == '/login':
		return login.layout
	elif pathname == '/success':
		if current_user.is_authenticated:
			return layout_function()
		else:
			return login_fd.layout
	elif pathname == '/logout':
		if current_user.is_authenticated:
			logout_user()
			return logout.layout
		else:
			return logout.layout
	else:
		return '404'


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''

'''
@auth.route('/signup', methods=['POST'])
def signup_post():
	# code to validate and add user to database goes here
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')

	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

	if user: # if a user is found, we want to redirect back to signup page so user can try again
		flash('Email adress already exists')
		return redirect(url_for('auth.signup'))

	# create new user with the form data. Hash the password so plaintext version isn't saved.
	new_user = User(email=email, username=name, password=generate_password_hash(password, method='sha256'))

	# add the new user to the database
	db.session.add(new_user)
	db.session.commit()
	return redirect(url_for('auth.login'))
'''

if __name__ == '__main__':
    app.run_server(debug=True)
