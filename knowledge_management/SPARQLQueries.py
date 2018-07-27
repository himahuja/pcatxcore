# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 12:57:11 2018

@author: amichels
"""

from SPARQLWrapper import SPARQLWrapper, JSON

queryString = "SELECT * WHERE { ?s ?p ?o. }"
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# add a default graph, though that can also be part of the query string
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])
