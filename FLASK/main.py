from    flask       import  Flask, render_template, json, request, redirect, session
from    werkzeug    import  generate_password_hash, check_password_hash
import  MySQLdb     as      mysql 
import  os
import  uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
username    = 'root'
passwd      = 'NO'
dbname      = 'Boletin0'
hostname    = 'localhost'
tablename   = 'tbl_user'


# These environnment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME    = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER               = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD           = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
    # When deployed to App Engine, the 'SERVER_SOFTWARE' environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE','').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        conn = mysql.connect(
            unix_socket = cloudsql_unix_socket,
            user        = CLOUDSQL_USER,
            passwd      = CLOUDSQL_PASSWORD,
            db          = dbname)

    # If the unix socket is unavailable, then try to connect using TCP. This 
    # will work if you are running a local MySQL server or using the Clud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=abogangster-182717:europe-west3:boletin=tcp:3306
    #

    else:
        print "local mysql"
        conn = mysql.connect(
            host    = '127.0.0.1',
            user    = 'root',
            passwd  = 'NO',
            db      = 'Boletin0')

    return conn

@app.route('/')
@app.route('/main')
def main():
    return render_template('index.html')

# This is a dummy function to test cathing any path and using it to render content
# @app.route('/public/<path:path>/')
@app.route('/public')
def bla():
    # print path
    return render_template('index_carousel.html', first_slider="path")



@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
    # return render_template('signup.html')
    return render_template('signup_image.html')

@app.route('/userHome/<path:path>/')
# @app.route('/userHome')
def userHome(path):

    # If we are in the same session, this prohibits the current user to visit other profiles
    if (str(session.get('user')) == str(path)):

        conn    = connect_to_cloudsql()
        cursor  = conn.cursor()
        # cursor.callproc('sp_validateLogin',(_username,))
        mysql_query = "SELECT * FROM tbl_user WHERE user_id = " + path
        cursor.execute(mysql_query)
        data    = cursor.fetchall()

        data_name           = data[0][1]
        data_email          = data[0][2]
        data_description    = data[0][4]
        data_jpg1           = data[0][6]
        data_jpg2           = data[0][7]
        data_jpg3           = data[0][8]
        data_case1          = data[0][9]
        data_case2          = data[0][10]
        data_case3          = data[0][11]

        return render_template('userhome_1.html', 
            name        = data_name, 
            email       = data_email, 
            description = data_description,
            jpg1        = data_jpg1,
            jpg2        = data_jpg2,
            jpg3        = data_jpg3,
            case1       = data_case1,
            case2       = data_case2,
            case3       = data_case3)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')



@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        conn    = connect_to_cloudsql()
        cursor  = conn.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data    = cursor.fetchall()
 
        if len(data) > 0:
            # 0 is the first row, and 3 is the 4th column !!! obviously 
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                path = "/userHome/" +  str(data[0][0])
                # return redirect('/userHome/')
                return redirect(path)
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
        # return render_template('loginerror.html',error = 'Unauthorized Access')


@app.route('/getProfile')
def getProfile():
    try:
        if session.get('user'):
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    # TODO: This sucks, but its a way of making it work for now
    _name       = ''
    _email      = ''
    _password   = ''
    _description= ''
    _link       = ''
    _jpg1       = ''
    _jpg2       = ''
    _jpg3       = ''
    _case1      = ''
    _case2      = ''
    _case3      = ''
    try:
        _name       = request.form['inputName']
        _email      = request.form['inputEmail']
        _password   = request.form['inputPassword']
        _description= request.form['description']
        _jpg1       = request.form['filePath1']
        _jpg2       = request.form['filePath2']
        _jpg3       = request.form['filePath3']
        _case1      = request.form['case1']
        _case2      = request.form['case2']
        _case3      = request.form['case3']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL
            # conn              = mysql.connect(host=hostname,user=username,passwd=passwd,db=dbname)
            conn                = connect_to_cloudsql()
            cursor              = conn.cursor()
            _hashed_password    = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password, _description, _link, _jpg1, _jpg2, _jpg3, _case1, _case2, _case3))
            data                = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully!'})
                # return render_template('index_table.html', data = data)
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:

        return json.dumps({'error':str(e)})
    finally:
        # TODO: This shit is bad, if name email and password are not valid, no cursor nor conn will
        # have been created so here they will be null, fix this!
        cursor.close() 
        conn.close()


@app.route('/display')        
def display():
    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()
    # query               = 'SELECT * from tbl_user'
    cursor.execute('SELECT user_id, user_name, user_username from tbl_user')
    # cursor.execute('SELECT * from tbl_user')

    data = cursor.fetchall()
    conn.commit()
    cursor.close() 
    conn.close()
    return render_template('index_table.html', data = data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload handler code will be here
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})


if __name__ == "__main__":
    app.run()



