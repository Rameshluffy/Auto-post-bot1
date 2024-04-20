from flask import Flask
app = Flask(__name__)
@app.route('/')
def JaiShreeKrishna():
    return "<h1 style='color: red;'>Jai Shree Krishnsa</h1>"
if __name__ == '__main__':
    app.run()