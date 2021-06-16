import osmium
import numpy as np
import pandas as pd
import re
import sys
import urllib
import time
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD

start = time.time()
class osm2rdf_handler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)    
        self.counts=0
        self.g = Graph()
        self.graph = self.g
        self.wd = Namespace("http://www.wikidata.org/wiki/")
        self.g.bind("wd", self.wd)
        self.wdt = Namespace("http://www.wikidata.org/prop/direct/")
        self.g.bind("wdt", self.wdt)
        self.wkg = Namespace("http://www.worldkg.org/resource/")
        self.g.bind("wkg", self.wkg)
        self.wkgs = Namespace("http://www.worldkg.org/schema/")
        self.g.bind("wkgs", self.wkgs)
        self.geo = Namespace("http://www.opengis.net/ont/geosparql#")
        self.g.bind("geo", self.geo)
        self.rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.g.bind("rdfs", self.rdfs)
        self.rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self.g.bind('rdf',self.rdf)
        self.ogc=Namespace("http://www.opengis.net/rdf#")
        self.g.bind('ogc',self.ogc)
        self.sf = Namespace("http://www.opengis.net/ont/sf#")
        self.g.bind('sf', self.sf)
        self.osmn = Namespace("https://www.openstreetmap.org/node/")
        self.g.bind("osmn", self.osmn)
        self.supersub = pd.read_csv('OSM_Ontology_map_features.csv', sep='\t', encoding='utf-8')
        self.key_list = pd.read_csv('Key_List.csv', sep='\t', encoding='utf-8')
        self.key_list = list(self.key_list['key'])
        self.supersub = self.supersub.drop_duplicates()
        
        self.dict_class = self.supersub.groupby('key')['value'].apply(list).reset_index(name='subclasses').set_index('key').to_dict()['subclasses']
    
    def to_camel_case_class(self, word):
        word = word.replace(':','_')
        return ''.join(x.capitalize() or '_' for x in word.split('_'))
    
    def to_camel_case_classAppend(self, key, val):
        return self.supersub.loc[(self.supersub['value'] == val) & (self.supersub['key'] == key)]['appendedClass'].values[0]
    
    def to_camel_case_key(self, input_str):
        input_str = input_str.replace(':','_')
        words = input_str.split('_')
        return words[0] + "".join(x.title() for x in words[1:])
    
    def printTriple(self, s, p, o):
        if p in self.dict_class: 
            if o in self.dict_class[p]:
                rel = URIRef('http://www.worldkg.org/resource/' + s)
                instanceOf = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
                res = URIRef('http://www.worldkg.org/schema/' + self.to_camel_case_classAppend(p,o))
                self.g.add((rel, instanceOf , res))
            if o == 'Yes':
                rel = URIRef('http://www.worldkg.org/resource/' + s)
                instanceOf = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
                res = URIRef('http://www.worldkg.org/schema/' + self.to_camel_case_class(p))
                self.g.add((rel, instanceOf , res))
        else:
            if p=='Point':
                sub = URIRef('http://www.worldkg.org/resource/' + s)
                geoprop = URIRef('http://www.worldkg.org/schema/spatialObject')
                geoobj = URIRef('http://www.worldkg.org/resource/geo' + s)
                prop = URIRef('http://www.opengis.net/ont/sf#Point')
                typ = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
                self.g.add((sub, geoprop, geoobj))
                self.g.add((geoobj, typ, prop))
                self.g.add((geoobj, self.geo["asWKT"], Literal(o, datatype=self.geo.wktLiteral)))
            elif p == 'osmLink':
                sub = URIRef('http://www.worldkg.org/resource/' + s)
                prop = URIRef('http://www.worldkg.org/schema/osmLink')
                obj = URIRef('https://www.openstreetmap.org/node/'+o)
                self.g.add((sub,prop,obj))
            elif p == 'name':
                sub = URIRef('http://www.worldkg.org/resource/' + s)
                prop = URIRef('http://www.w3.org/2000/01/rdf-schema#label')
                self.g.add((sub, prop, Literal(o)))
            elif p == 'wikidata':
                sub = URIRef('http://www.worldkg.org/resource/' + s)
                prop = URIRef("http://www.worldkg.org/schema/" + p)
                if o.startswith('Q'):
                    obj = URIRef('http://www.wikidata.org/wiki/' + o)
                else:
                    obj = Literal(o)
                self.g.add((sub, prop, obj))
            elif p == 'wikipedia':
                sub = URIRef('http://www.worldkg.org/resource/' + s)
                prop = URIRef("http://www.worldkg.org/schema/wikipedia" )
                try:
                    country = o.split(':')[0]
                    ids = urllib.parse.quote(o.split(':')[1])
                except IndexError:
                    country = ''
                    ids = urllib.parse.quote(o)
                url = country+'.wikipedia.org/wiki/'+country+':'+ids
                url = 'https://'+urllib.parse.quote(url)
                obj = URIRef(url)
                self.g.add((sub, prop, obj))
            else:
                if p in self.key_list:
                    sub = URIRef('http://www.worldkg.org/resource/' + s)
                    prop = URIRef("http://www.worldkg.org/schema/" + self.to_camel_case_key(p))
                    self.g.add((sub, prop, Literal(o)))
        
    def __close__(self):
        print(str(self.counts))

    def node(self, n):
        if len(n.tags)>1:
            lat = str(n.location.lat)
            lon = str(n.location.lon)
            id = str(n.id)



            point = 'Point('+str(n.location.lon)+' '+str(n.location.lat)+')'

            #self.printTriple(id, "lat", lat)
            #self.printTriple(id, "long", lon)
            self.printTriple(id, "Point", point)
            self.printTriple(id,"osmLink",id)


            for k,v in n.tags:

                val = str(v)

                val=val.replace("\\", "\\\\")
                val=val.replace('"', '\\"')
                val=val.replace('\n', " ")

                k = k.replace(" ", "")

                self.printTriple(id, k, val)
h = osm2rdf_handler()
h.apply_file(sys.argv[1])
h.graph.serialize(sys.argv[2],format="turtle", encoding = "utf-8" )
end = time.time()
print(end - start)
