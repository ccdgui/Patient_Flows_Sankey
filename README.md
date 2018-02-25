# Patient Flows Sankey
## Patient flow analysis with a Sankey diagram



#### Overview 
This project is about modeling patient flows between units of a hospital using a Sankey diagram. Sankey diagrams are flow diagrams, in which the width of the links is shown proportionally to the flow quantity. Sankey diagrams put a visual emphasis on transfers or flows within a system. This diagram illustrates the complexity of patient flows between various units of a large hospital. By improving patient flows,  a hospital can save money and boost patient and provider satisfaction.

#### Ouput 

Sankey diagram with Plotly: 

<img width="995" alt="screen shot 2018-02-19 at 10 12 59 am" src="https://user-images.githubusercontent.com/25650135/36398595-d7787a8c-1595-11e8-8f2c-b569b6e715b6.png">


Each horizontal stack represents a different step in patient journey. 

#### Script Outline  

sankey.py formats data from hospital records to create a graph structure with source-target pairs and nodes which are used as inputs to create a visualization. 

There are 6 steps in this script: 

  * step 1:  The script parse raw data to compute how many stations ('Step') each patient ('Case') visits. For each step in the patient journey, the script generates a tuple with a Source and Target stored inside the 'ouput' dictionary. 
  
  * step 2: The tuples (i.e. (Step, Source, Target)) in the 'output' are aggregated and the frequency determined with a Counter. 
  
  * step 3: Dictionary 'sankey' is created from the frequency dictionary. It represents a graph structure with links (Source, Target) and nodes. First the links are created: the names of source and target reflect the step position in the patient journey. For example: step 1 in 'Normal' Station becomes Normal_1. Second: the nodes are created from the links. 
  
  * step 4: Nodes in the Dictionary 'sankey' are sorted along 2 criteria: 1. the step number and 2. the order in which the nodes appear in an index called 'Bewgungsarten'. This is done so that the nodes appear in a consistent order in the graph. 
  
  * step 5: A new dictionary called 'data' is created. It contains the indexed values of the ordered nodes and links. 
  
  * step 6: The actual graph is created with Plotly based on the 'data' dictionary.
