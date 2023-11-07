from flask import Flask, render_template, request
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.parse('../data/result-with-links.ttl', format="turtle")


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Directions')
def directions():
    return render_template('directions.html', data ="")

@app.route('/Directions/Request')
def directions_request():
    if request.method == 'GET':
        n_places = request.args.get('plazas')
        n_places = str(n_places)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Direction WHERE {
                ?Station ns:places ''' + n_places + '''.                 
                ?Station ns:hasDirection ?Directions. 
                ?Directions rdfs:label ?Direction.
            } LIMIT 10'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(r.Direction)

        if len(string) == 0:
            string.append("No se han encontrado Bases con dicho numero de plazas")

        datos = {'resultados': string}
        return render_template('directions.html', data=datos)

    

@app.route('/Streets')
def streets():
    return render_template('streets.html', data="")

@app.route('/Streets/Request')
def streets_request():
    if request.method == 'GET':
        calle = request.args.get('street')
        calle = str(calle)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?ID WHERE {
                ?Street rdfs:label "''' + calle + '''". 
                ?Direction ns:hasStreet ?Street.                
                ?Bases ns:hasDirection ?Direction. 
                ?Bases ns:id ?ID.
            } LIMIT 10'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(str(r.ID))

        if len(string) == 0:
            string.append("Dicha calle no tienen ninguna base de bicicletas")

        datos = {'resultados': string}
        return render_template('streets.html', data=datos)

@app.route('/Districts')
def districts():
    return render_template('districts.html', data="")

@app.route('/Districts/Request')
def districts_request():
    if request.method == 'GET':
        distrito = request.args.get('district')
        distrito = str(distrito)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Nombre WHERE {
                ?District rdfs:label "''' + distrito + '''". 
                ?Hood ns:neighbourhoodBelongsDistrict ?District.                
                ?Direction ns:directionBelongsNeighbourhood ?Hood. 
                ?Direction ns:hasStreet ?Street.
                ?Street rdfs:label ?Nombre
            } LIMIT 25'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(r.Nombre)

        if len(string) == 0:
            string.append("Dicho distrito no alberga ninguna calle con bases de bicicletas")

        datos = {'resultados': string}
        return render_template('districts.html', data=datos)

@app.route('/Companys')
def companys():
    return render_template('companys.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)         ##Indicamos que cada vez que cambiemos algo  se reinicie el servidor, y en que puerto lanzarse