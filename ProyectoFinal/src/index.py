from flask import Flask, render_template
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.parse('../data/result-with-links.ttl', format="turtle")


app = Flask(__name__)

@app.route('/PracticSemanticWebGroup03/{}')
def home():
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
        ?Station ns:places 24.           
        ?Stations ns:hasDirection ?Directions. 
        ?Directions rdfs:label ?Direction.
    } LIMIT 10''')
    
    ##ADAPTER##
    string = ''
    for r in g.query(q):
        string = r.Direction + '\n'

    datos = {'Resultados': string}

    return render_template('home.html', data=datos)

@app.route('/PracticSemanticWebGroup03/about')
def about ():
    return 'about'

if __name__ == '__main__':
    app.run(debug=True, port=5000)         ##Indicamos que cada vez que cambiemos algo  se reinicie el servidor, y en que puerto lanzarse