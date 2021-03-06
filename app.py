from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        search = request.form['search']
        housing = model.get_housing(search=search)
        result = len(housing)
        map = model.maponplotly(housing)
        graph = model.graph(housing)
        bar = model.bar(housing)


    else:
        housing = model.get_housing()
        result = len(housing)
        map = model.maponplotly(housing)
        graph = model.graph(housing)
        bar = model.bar(housing)




    return render_template('housing.html', housing=housing, map=map, graph=graph,result=result, bar=bar)


@app.route('/filter', methods=['GET', 'POST'])
def housing():
    if request.method == "POST":
        bed = request.form.get('bed')
        bath = request.form['bath']
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        buildingtype = request.form['buildingtype']
        pet = request.form['pet']
        parking = request.form['parking']
        status = request.form['status']
        housing = model.get_housing(bed=bed, bath=bath, pet=pet, parking=parking, buildingtype=buildingtype, sortorder=sortorder, sortby=sortby, status=status)
        result = len(housing)
        map = model.maponplotly(housing)
        graph = model.graph(housing)
        bar = model.bar(housing)



    else:
        housing = model.get_housing()
        result = len(housing)
        map = model.maponplotly(housing)
        graph = model.graph(housing)
        bar = model.bar(housing)



    return render_template('housing.html', housing=housing, map=map, result=result, graph=graph, bar=bar)




if __name__ == '__main__':
    model.init_housing()
    app.run(debug=True)
