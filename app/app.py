from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return "Hello Piotr"


if __name__ == '__main__':
    app.run(port=5000)