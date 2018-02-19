import pandas as pd
from collections import Counter
import json
import re
import plotly.plotly as py

raw_data = pd.read_csv('/home/StrobiHealth/PatientFlow/Raw Data/tbl_neu.csv')
bewegung = pd.read_csv('/home/StrobiHealth/PatientFlow/Raw Data/Bewegungsarten.csv')

#step 1: parse raw_data to compute Steps number for each Case and corresponding Source and Target. 
output = {1:[]}  #dictionary key is Case number (i.e. 'FallNr'), value is list of Stations tuples 
counter = 0  #counter represents number of step for each Case 
row_iterator = raw_data.iterrows()
for i, row in row_iterator: 
    if i > 0: 
        current_row = raw_data.loc[i]
        previous_row = raw_data.loc[i-1]   
        if current_row['FallNr'] == previous_row['FallNr']:    
            counter += 1      #counter incremented if previous Case number is similar 
            tup1 = (counter, previous_row['Ort'], current_row['Ort'])      #previous row = source, current row = target
            output[current_row['FallNr']].append(tup1)  
        else: 
            counter = 0      #counter reset for each new Case
            output[current_row['FallNr']] = []  
            
#step 2: aggregate tuples (i.e. (Step, Source, Target)) and compute frequency of each tuple
output_values = list(output.values())
frequency = dict(Counter(x for xs in output_values for x in set(xs)))       

#step 3: create dictionary structure with links and nodes from frequency dictionary
sankey = {"links": [], "nodes": []}
for i, y in frequency.items():     #links are created first, from items of frequency dictionary    
    if i[0] < 5: 
        link = dict(
            source = str(i[1]) + "_" + str(i[0]),
            target = str(i[2]) + "_" + str(i[0]+1),
            value = y, 
            )
        sankey["links"].append(link)     
        check_node = [link[x] for x in ['source', 'target']]     #nodes derived from links 'source' and 'target' 
        for x in check_node:        #append a new node, only if it does not already exists   
            if not any(d.get('name', None) == x for d in sankey["nodes"]): 
                name = dict(
                    name = x,
                    station = re.sub('[^a-zA-Z]+', '', x),
                    step = re.sub('[^0-9]+', '', x)
                )
                sankey["nodes"].append(name)  
                
#step 4: sort nodes (by Step number and index position in dataframe 'bewegung') and sort links by number of Steps                               
def bewegung_index(station):      #looks up index value in table 'bewegung'
    return bewegung.loc[bewegung['Bewgungsarten'] == station].index[0]               
                
sorted_nodes = sorted(sankey['nodes'], key=lambda k: (k['step'], bewegung_index(k['station']))) 
for w, node in enumerate(sorted_nodes):
    node['id'] = w
    node['color'] = 'rgba(31, 119, 180, 0.8)' 
    
def id_lookup(node, sorted_list):
    for item in sorted_list: 
        if item['name'] == node['source']:
            return item['id']
        
for d in sankey['links']: 
    d['source_id'] = id_lookup(d, sorted_nodes)    

sorted_links = sorted(sankey['links'], key=lambda k: (k['source_id']))  


#step 5: create data structure with node labels and link lists based on node index 
data = dict(
        nodes = dict(
                    label = [node['name'] for node in sorted_nodes],
                    color = [node['color'] for node in sorted_nodes]
                ),
        link = dict(
                    source = [nodes["label"].index(link['source']) for link in sorted_links ],
                    target = [nodes["label"].index(link['target']) for link in sorted_links ],
                    value = [link['value'] for link in sorted_links]
                )
            )

#step 6: plot graph with plotly
py.sign_in('xxx', 'xxxxxxx')

data_trace = dict(
    type='sankey',
    domain = dict(
      x =  [0,1],
      y =  [0,1]
    ),
    orientation = "h",
    valueformat = ".0f",
    valuesuffix = "Patients",
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label =  data["nodes"]["label"],
      color =  data["nodes"]["color"]
    ), 

    link = dict(
      source =  data["link"]["source"],
      target =  data["link"]["target"],
      value =  data["link"]["value"],
      label =  data["nodes"]["label"]
  )   

)

layout =  dict(
    title = "Patient Flow Analysis",
    font = dict(
      size = 10
    )
)

fig = dict(data=[data_trace], layout=layout)
py.iplot(fig, validate = False)
