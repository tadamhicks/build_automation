from flask import Flask, request, session, redirect, url_for, render_template, \
    jsonify, make_response, send_file
from models import LastBuild, GH


# configuration
DEBUG = True
SECRET_KEY = 'aledjyufg2qwe2244lkjhae0900'
# JAPI = 'https://jenkins.bertramlabs.com'
# JAPI = 'http://10.30.20.122:8080'


# Application
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


# Route and function to get the latest build
@app.route('/lastjenkinsbuild', methods=['POST'])
def getLastBuild():

    user = request.json.get('username')
    pw = request.json.get('password')
    japi = request.json.get('japi')
    proj = request.json.get('project')
    results = LastBuild(japi, user, pw, proj).get()

    return jsonify(md5=results[1], lastbuild=results[0])


# Route and function to push into git
@app.route('/editrepo', methods=['POST'])
def editCode():

    # First get the payload rom the request
    user = request.json.get('username')
    pw = request.json.get('password')
    token = request.json.get('token')
    organization = request.json.get('organization')
    repository = request.json.get('repo')
    fileage = request.json.get('file')
    commitM = request.json.get('commit_message')
    content = request.json.get('file_content')

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
