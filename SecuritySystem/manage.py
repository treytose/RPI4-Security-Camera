from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disable', methods=['GET', 'POST'])
def disable():
    f = open('security.txt', 'w')
    f.write('True')
    f.close()
    return 'Disabled 5 seconds'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
