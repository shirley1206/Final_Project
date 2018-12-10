from flask import Flask, render_template, request
import model

app = Flask(__name__)


# @app.route('/')
# def index():
#     housing = model.get_housing()
#     map = model.maponplotly()
#     return render_template('housing.html', housing=housing, map=map)
#

@app.route('/housing', methods=['GET', 'POST'])
def housing():
    if request.method == "POST":
        bed = request.form.get('bed')
        bath = request.form['bath']
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        buildingtype = request.form['buildingtype']
        pet = request.form['pet']
        parking = request.form['parking']
        housing = model.get_housing(bed=bed, bath=bath, pet=pet, parking=parking, buildingtype=buildingtype, sortorder=sortorder, sortby=sortby)
        map = model.maponplotly()
        result = len(housing)

    else:
        housing = model.get_housing()
        map = model.maponplotly()
        result = len(housing)

    return render_template('housing.html', housing=housing, map=map, result=result)


if __name__ == '__main__':
    model.init_housing()
    app.run(debug=True)
