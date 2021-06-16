# WorldKG-Knowledge-Graph
This repository contains codes to reproduce the WorldKG knowledge graph. 
The WorldKG knowledge graph is a comprehensive large-scale geospatial knowledge graph based on OpenStreetMap that provides semantic representation of geographic entities from over 188 countries. WorldKG contains higher representation of geographic entities compared to other knowledge graph and can be used as an underlying data source for various applications such as geospatial question answering, geospatial data retrieval, and other cross-domain semantic data-driven applications.


<h3>Prerequisites</h3>
<ul>
	<li>Python = 3.6</li>
</ul>


<h3>Setup</h3>
<p>Steps to create the WorldKG triples for the particular OSM snapshot.</p>
<ol>
    <li>Clone the repository
		<div class="readme-code">git clone https://github.com/alishiba14/WorldKG-Knowledge-Graph.git<br>
		cd WorldKG-Knowledge-Graph</div>
	</li>
    <li>Install the Python Requirements
		<div class="readme-code">pip install -r requirements.txt</div>
	</li>


<li>Download the specific OpenStreetMap snapshot, e.g., from <a href="https://download.geofabrik.de/" target="_blank">https://download.geofabrik.de/</a>. We recommend using the osm.pbf format.</li>

<li>Run the CreateTriples.py:

<div class="readme-code">python3 CreateTriples.py /path-to-pbf-file /path-to-the-ttl-file-to-save-triples </div></li>

Example: <div class="readme-code">python3 CreateTriples.py italy-latest.osm.pbf italyTriples.ttl</li></div>
</old>

<h3>File Structure</h3>

<li>Key_List.csv - Contains list of OSM keys with valid OSM wiki page.</li>
<li>OSM_Ontology_map_features.csv - Contains tags collected from OSM map features (https://wiki.openstreetmap.org/wiki/Map_features).</li>
<li>requirements.txt - Contains versions of python libraries used.</li>
<li>CreateTriples.py - Main python file to create the WorldKG instance triples.</li>
<li>WorldKG_Ontology.ttl - WorldKG ontology triples in .ttl format.</li>