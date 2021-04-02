# -*- coding: utf-8 -*-


### import libraries
import rdflib
import requests
import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, BNode,  Namespace #basic RDF handling
from rdflib.namespace import FOAF , XSD, SKOS, RDF, RDFS, OWL, DC, DCTERMS, VOID, DOAP #most common namespaces
import urllib.parse #for parsing strings to URI's
import configparser



""" reading the path from path.properties file,specify the path of path.properties file"""

config = configparser.ConfigParser()

''' specify the path of path.properties file here '''
config.readfp(open('./path.properties'))

#url= "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv" 

''' reading paths from path.properties file '''
url = config.get('PATH', 'url_path' )
rdf_path = config.get('PATH','rdf_path')
graphdb_path = config.get('PATH','graphdb_path')

''' read the csv file using pandas '''
df=pd.read_csv(url)

# df # uncomment to check for contents
df.head()

''' taking unique countries in the list '''

dist = df['countriesAndTerritories'].unique()
dist = dist.tolist()
len(dist)

''' initializing rdf graph here '''

g = Graph()

''' assigning namespaces '''
qb = Namespace('http://purl.org/linked-data/cube#')
scovo = Namespace('http://purl.org/NET/scovo#')
org = Namespace('http://www.w3.org/ns/org#')
admingeo = Namespace('http://data.ordnancesurvey.co.uk/ontology/admingeo/')
interval = Namespace('http://reference.data.gov.uk/def/intervals/')
eg = Namespace('http://example.org/ns#')
exgeo = Namespace('http://example.org/geo#')
sdmx = Namespace('http://purl.org/linked-data/sdmx#')
sdmxconcept = Namespace('http://purl.org/linked-data/sdmx/2009/concept#')
sdmxdimension = Namespace('http://purl.org/linked-data/sdmx/2009/dimension#')
sdmxattribute = Namespace('http://purl.org/linked-data/sdmx/2009/attribute#')
sdmxmeasure = Namespace('http://purl.org/linked-data/sdmx/2009/measure#')
sdmxcode = Namespace('http://purl.org/linked-data/sdmx/2009/code#')
sdmxmetadata = Namespace('http://purl.org/linked-data/sdmx/2009/metadata#')
sdmxsubject = Namespace('http://purl.org/linked-data/sdmx/2009/subject#')
dct = Namespace('http://purl.org/dc/terms/')

'''  Creating Dataset using Datacube'''

g.add((URIRef(eg+'dataset1'), RDF.type , URIRef(qb+'DataSet')))
g.add((URIRef(eg+'dataset1'), RDFS.label, Literal("covid-19 dataset" ,lang ='en')))
g.add((URIRef(eg+'dataset1'), URIRef(dct+'description'),Literal("contains information on newly reported COVID-19 cases and deaths in EU/EEA countries",lang='en')))
g.add((URIRef(eg+'dataset1'), URIRef(dct+'publisher'), URIRef(eg+'organization')))
g.add((URIRef(eg+'dataset1'), URIRef(qb+'structure'), URIRef(eg+'dsd1')))
g.add((URIRef(eg+'dataset1'), URIRef(dct+'subject'), URIRef(sdmxsubject+'1.4')))

### loop to dynamically create slices for every country present in the Dataframe ####
for i in range(1,len(dist)+1):
    vslice = 'slice' + str(i)
    g.add((URIRef(eg+'dataset1'), URIRef(qb+'Slice'), URIRef(eg+vslice)))

'''Creating Data structure definition using Datacube '''
## initializing blank nodes ###

y = BNode()
y1 = BNode()
y2 =  BNode()
y3 =  BNode()
y4 =  BNode()
y5 = BNode()
y6 = BNode()
y7 = BNode()
y8 = BNode()

g.add((URIRef(eg+'dsd1'), RDF.type, URIRef(qb+'DataStructureDefinition')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y))
g.add((y, URIRef(qb+'dimension'), URIRef(qb+'dateRep')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y1))
g.add((y1, URIRef(qb+'dimension'), URIRef(qb+'countriesAndTerritories')))
g.add((y1, URIRef(qb+'componentAttachment'),URIRef(qb+'Slice')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y2))
g.add((y2, URIRef(qb+'dimension'), URIRef(exgeo+'geoId')))
g.add((y2, URIRef(qb+'componentAttachment'), URIRef(qb+'Slice')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y3))
g.add((y3, URIRef(qb+'dimension'), URIRef(eg+'continentExp')))
g.add((y3, URIRef(qb+'componentAttachment'), URIRef(qb+'Slice')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y4))
g.add((y4, URIRef(qb+'dimension'), URIRef(eg+'popData2020')))
g.add((y4, URIRef(qb+'componentAttachment'), URIRef(qb+'Slice')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y5))
g.add((y5, URIRef(qb+'dimension'), URIRef(exgeo+'countryterritoryCode')))
g.add((y5, URIRef(qb+'componentAttachment'), URIRef(qb+'Slice')))

''' Creating measures using Datacube'''

g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y6))
g.add((y6, URIRef(qb+'measure'), URIRef(eg+'deaths')))
g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y7))
g.add((y7, URIRef(qb+'measure'), URIRef(eg+'cases')))

''' Creating attributes using Datacube'''

g.add((URIRef(eg+'dsd1'), URIRef(qb+'component'), y8))
g.add((y8, URIRef(qb+'attribute'), URIRef(sdmxattribute+'unitMeasure')))
g.add((y8, URIRef(qb+'componentRequired'),Literal("True",datatype=XSD.boolean)))
g.add((y8, URIRef(qb+'componentAttachment'),URIRef(qb+'DataSet')))

''' Creating slices using Datacube '''

g.add((URIRef(eg+'dsd1'), URIRef(qb+'sliceKey'), URIRef(eg+'sliceByDate')))


g.add((URIRef(eg+'sliceByDate'), RDF.type, URIRef(qb+'sliceKey')))
g.add((URIRef(eg+'sliceByDate'), RDFS.label, Literal("slice by date",lang ='en')))
g.add((URIRef(eg+'sliceByDate'), RDFS.comment, Literal("Slice by grouping dates together, fixing area, geoid, popdata, countryterritoryCode,continentexp",lang ='en')))
g.add((URIRef(eg+'sliceByDate'), URIRef(qb+'componentProperty'), URIRef(eg+'countriesAndTerritories')))
g.add((URIRef(eg+'sliceByDate'), URIRef(qb+'componentProperty'), URIRef(exgeo+'geoId')))
g.add((URIRef(eg+'sliceByDate'), URIRef(qb+'componentProperty'), URIRef(exgeo+'countryterritorycode')))
g.add((URIRef(eg+'sliceByDate'), URIRef(qb+'componentProperty'), URIRef(eg+'continentExp')))
g.add((URIRef(eg+'sliceByDate'), URIRef(qb+'componentProperty'), URIRef(eg+'popData2020')))


''' Creating Dimensions and measures using Datacube'''

g.add((URIRef(eg+'dateRep'),RDF.type, RDF.Property))
g.add((URIRef(eg+'dateRep'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(eg+'dateRep'),RDFS.label, Literal("refernce period",lang='en')))
g.add((URIRef(eg+'dateRep'),RDFS.subPropertyOf, URIRef(sdmxdimension+'refPeriod')))
g.add((URIRef(eg+'dateRep'),RDFS.range, URIRef(interval+'Interval')))
g.add((URIRef(eg+'dateRep'),URIRef(qb+'concept'), URIRef(sdmxconcept+'refPeriod')))

g.add((URIRef(eg+'countriesAndTerritories'),RDF.type, RDF.Property))
g.add((URIRef(eg+'countriesAndTerritories'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(eg+'countriesAndTerritories'),RDFS.label, Literal("refernce country",lang='en')))
g.add((URIRef(eg+'countriesAndTerritories'),RDFS.subPropertyOf, URIRef(sdmxdimension+'refArea')))
g.add((URIRef(eg+'countriesAndTerritories'),RDFS.range, URIRef(eg+'allcountries')))
g.add((URIRef(eg+'countriesAndTerritories'),URIRef(qb+'concept'), URIRef(sdmxconcept+'refArea')))

g.add((URIRef(eg+'continentExp'),RDF.type, RDF.Property))
g.add((URIRef(eg+'continentExp'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(eg+'continentExp'),RDFS.label, Literal("refernce continent",lang='en')))
g.add((URIRef(eg+'continentExp'),RDFS.subPropertyOf, URIRef(sdmxdimension+'refArea')))
g.add((URIRef(eg+'continentExp'),RDFS.range, URIRef(eg+'allcontinents')))
g.add((URIRef(eg+'continentExp'),URIRef(qb+'concept'), URIRef(sdmxconcept+'refArea')))

g.add((URIRef(exgeo+'countryterritoryCode'),RDF.type, RDF.Property))
g.add((URIRef(exgeo+'countryterritoryCode'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(exgeo+'countryterritoryCode'),RDFS.label, Literal("country territory code ",lang='en')))
g.add((URIRef(exgeo+'countryterritoryCode'),RDFS.subPropertyOf, URIRef(sdmxcode+'area')))
g.add((URIRef(exgeo+'countryterritoryCode'),RDFS.range, URIRef(eg+'allteritoriescode')))
g.add((URIRef(exgeo+'countryterritoryCode'),URIRef(qb+'concept'), URIRef(sdmxconcept+'refArea')))


g.add((URIRef(exgeo+'geoId'),RDF.type, RDF.Property))
g.add((URIRef(exgeo+'geoId'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(exgeo+'geoId'),RDFS.label, Literal("geography code ",lang='en')))
g.add((URIRef(exgeo+'geoId'),RDFS.subPropertyOf, URIRef(sdmxcode+'area')))
g.add((URIRef(exgeo+'geoId'),RDFS.range, URIRef(eg+'allgeographycode')))
g.add((URIRef(exgeo+'geoId'),URIRef(qb+'concept'), URIRef(sdmxconcept+'refArea')))

g.add((URIRef(eg+'popData2020'),RDF.type, RDF.Property))
g.add((URIRef(eg+'popData2020'),RDF.type, URIRef(qb+'DimensionProperty')))
g.add((URIRef(eg+'popData2020'),RDFS.label, Literal("population of the country ",lang='en')))
g.add((URIRef(eg+'popData2020'),RDFS.subPropertyOf, URIRef(sdmxmeasure+'obsvalue')))
g.add((URIRef(eg+'popData2020'),RDFS.range, XSD.int64))


g.add((URIRef(eg+'deaths'),RDF.type, RDF.Property))
g.add((URIRef(eg+'deaths'),RDF.type, URIRef(qb+'MeasureProperty')))
g.add((URIRef(eg+'deaths'),RDFS.label, Literal("death number",lang='en')))
g.add((URIRef(eg+'deaths'),RDFS.subPropertyOf, URIRef(sdmxmeasure+'obsvalue')))
g.add((URIRef(eg+'deaths'),RDFS.range, XSD.int64))

g.add((URIRef(eg+'cases'),RDF.type, RDF.Property))
g.add((URIRef(eg+'cases'),RDF.type, URIRef(qb+'MeasureProperty')))
g.add((URIRef(eg+'cases'),RDFS.label, Literal("case number",lang='en')))
g.add((URIRef(eg+'cases'),RDFS.subPropertyOf, URIRef(sdmxmeasure+'obsvalue')))
g.add((URIRef(eg+'cases'),RDFS.range, XSD.int64))


''' taking countries in tuple with their index in order to read the data from dataframe '''
tup =[] # initialize empty list to store the tuple 
for i in range(1,len(dist)+1):
    tup.append(tuple((i,dist[i-1])))

    
for i,j in tup: # reading data from tuple in order to retrieve values from dataframe
    count=0
#    print(i,j)
    ''' taking variables to avoid duplicacy ''' 
    if len(str(i)) == 1:
        z = str(0)+str(0)+str(i)
    if len(str(i)) == 2:
        z = str(0)+str(i)
#    if len(str(i)) == 3:
#        z = str(i)
        
    vslice='slice'+str(i)
#    print(slice,j)
    for index,row in df.iterrows():    
        if row['countriesAndTerritories'] == j:
            count+=1
            g.add((URIRef(eg+vslice), RDF.type, URIRef(qb+'Slice')))
            g.add((URIRef(eg+vslice), URIRef(qb+'sliceStructure'), URIRef(eg+'sliceByDate')))
            g.add((URIRef(eg+vslice), URIRef(eg+'countriesAndTerritories'), URIRef(exgeo+row['countriesAndTerritories'])))
            g.add((URIRef(eg+vslice), URIRef(exgeo+'geoId'), URIRef(exgeo+row['geoId'])))
            g.add((URIRef(eg+vslice), URIRef(exgeo+'countryterritoryCode'), URIRef(exgeo+row['countryterritoryCode'])))
            g.add((URIRef(eg+vslice), URIRef(eg+'continentExp'), URIRef(exgeo+row['continentExp'])))
            g.add((URIRef(eg+vslice), URIRef(eg+'popData2020'), Literal(row['popData2020'])))
            a = 'o'+str(z)+str(count)
            g.add((URIRef(eg+vslice), URIRef(qb+'observation'), URIRef(eg+a)))
            
            g.add((URIRef(eg+a), RDF.type, URIRef(qb+'observation')))
            g.add((URIRef(eg+a), URIRef(qb+'dataset'), URIRef(eg+'dataset1')))
            g.add((URIRef(eg+a), URIRef(eg+'dateRep'), Literal(row['dateRep'],datatype=XSD.string)))
            g.add((URIRef(eg+a), URIRef(eg+'deaths'),  Literal(row['deaths'])))
            g.add((URIRef(eg+a), URIRef(eg+'cases'),   Literal(row['cases'])))  
    
            
           
''' storing the rdf file locally using turtle syntax '''
g.serialize(rdf_path, format='turtle')



''' storing rdf based on datacube into GraphDB by using python requests '''


headers = {
    'Content-Type': 'application/x-turtle',
}

data = g.serialize(format='turtle').decode('UTF-8')



response = requests.post(graphdb_path, data=data, headers=headers)


