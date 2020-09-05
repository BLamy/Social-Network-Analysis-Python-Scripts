#import statements
import networkx as nx
import pandas as pd
import numpy as np
import math

df = pd.read_csv('edgelist.csv') #read in CSV file with edgelist

G = nx.from_pandas_edgelist(df, create_using=nx.DiGraph()) #create graph from edgelist as a directed network (DiGraph())

Indegrees = [val for (node, val) in G.in_degree()] #gets the in-degree of all nodes in the network
Outdegrees = [val for (node, val) in G.out_degree()] #gets the out-degree of all nodes in the network
Nodes = G.nodes() #gets the name of all nodes in the network

G = nx.from_pandas_edgelist(df, create_using=nx.Graph()) #recreate the network as a undirected network to calculate betweenness score and plot

Betweenness_dict = nx.betweenness_centrality(G, normalized=False) #gets the betweenness score for of all nodes in the network
for node,value in Betweenness_dict.items():
    Betweenness_dict[node] = value/2 #divide each betweenness score by 2 because in directed networks betweeness scores are half what they would be in undirected networks
    
n_color = np.asarray([(Betweenness_dict[n] + 1) for n in Nodes]) #creates list of users from highest to lowest betweenness score for the color map
nx.draw(G, node_color=n_color, cmap="cool", node_size=[math.log(v+1/2,10) * 2 for v in Betweenness_dict.values()]) #draws the undirected network using a color map and also adjusts node size by the log of the betweenness score + 1

network_analysis_df = pd.DataFrame() #creates dataframe to output analysis
network_analysis_df["Nodes"] = Nodes #column 1 inlcudes each node name 
network_analysis_df["In-Degree"] = Indegrees #column 2 inlcudes each node's in-degree 
network_analysis_df["Out-Degree"] = Outdegrees #column 3 inlcudes each node's out-degree 
network_analysis_df["Betweenness"] = Betweenness_dict.values() #column 4 inlcudes each node's betweenness score
network_analysis_df.to_excel("output.xlsx") #outputs the dataframe to an excel file

