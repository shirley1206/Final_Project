from flask import Flask, render_template, request
import model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def housing():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        housing = model.get_housing(sortby, sortorder)
    else:
        housing = model.get_housing()

    return render_template("housing.html", housing=housing)


if __name__ == '__main__':
    model.init_housing()
    app.run(debug=True)
