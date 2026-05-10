from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'test to chekck if the server is running new code'

if __name__ == '__main__':
    app.run(debug=True)
