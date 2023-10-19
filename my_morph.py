import morph_kgc
from rdflib import Graph

# Genera los triples y carga en un gráfico RDFLib
g_rdflib = morph_kgc.materialize('C:\\Users\\nerea\\Desktop\\UPM\\4º Año\\Semestre 1\\Web linked\\Group03\\config.ini')

# Realiza consultas en el gráfico RDFLib
q_res = g_rdflib.query('SELECT DISTINCT ?classes WHERE { ?s a ?classes }')

# Genera los triples y carga en Oxigraph
g_oxigraph = morph_kgc.materialize_oxigraph('C:\\Users\\nerea\\Desktop\\UPM\\4º Año\\Semestre 1\\Web linked\\Group03\\config.ini')

# Realiza consultas en Oxigraph
q_res = g_oxigraph.query('SELECT DISTINCT ?classes WHERE { ?s a ?classes }')


# Crear un nuevo gráfico RDF
g_nt = Graph()

# Cargar los triples RDFLib en el nuevo gráfico
g_nt += g_rdflib

# Guardar el gráfico RDF en formato NTriples en un archivo
with open('output.nt', 'w', encoding='utf-8') as f:
    f.write(g_nt.serialize(format='nt'))

