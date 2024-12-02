from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
