from fastapi import FastAPI
from rdflib import Graph

app = FastAPI()

# Cargar datos desde el archivo TTL
g = Graph()
g.parse("rdf/result-with-links.ttl", format="ttl")


# Definir un modelo de datos para una estación de bicicletas
class BicycleStation:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

# Ruta para obtener todas las estaciones de bicicletas
@app.get("/bicycle_stations")
async def get_all_bicycle_stations():
    try:
        # Ejemplo de consulta SPARQL para obtener estaciones con detalles
        query = """
                SELECT ?id
                WHERE {
                    ?station a ns1:BicycleStation ;
                    ns1:id ?id ;
                
                    }
                    LIMIT 10
        """

        results = g.query(query)
        bicycle_stations = [
            {"id": str(result.id)}
            for result in results
        ]

        return bicycle_stations
    except Exception as e:
        # Manejar excepciones
        return {"error": str(e)}

# Ruta para obtener detalles de una estación de bicicletas específica
@app.get("/bicycle_stations/{station_id}")
async def get_bicycle_station(station_id: str):
    # Consulta RDF para obtener detalles de una estación específica
    # Procesa los datos y devuelve un objeto BicycleStation

    # Ejemplo de consulta SPARQL para una estación específica:
    query = f"""
    SELECT ?name ?latitude ?longitude
    WHERE {{
        <http://smartcity.linkeddata.es/lcc/resource/BicycleStation/{station_id}> a ns1:BicycleStation ;
                 ns1:latitude ?latitude ;
                 ns1:longitude ?longitude .
    }}
    """

    results = g.query(query)
    bicycle_station = None

    for result in results:
        bicycle_station = BicycleStation(id=station_id, latitude=str(result.latitude), longitude=str(result.longitude))
        break

    if bicycle_station:
        return bicycle_station
    else:
        return {"message": "Bicycle station not found"}


# Swagger generará automáticamente la documentación en http://localhost:8000/docs


