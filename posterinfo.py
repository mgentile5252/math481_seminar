#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 21:17:41 2019

@author: matthewgentile
"""



import nba_api
import nba_api.stats.static.teams
import pandas

from nba_api.stats.endpoints import teamdashlineups

import networkx as nx
import numpy
import operator
import functools

import requests

import matplotlib.pyplot as plt

### EXAMPLE TEAM WILL BE HOUSTON ROCKETS ###


example_rockets_players = ["P_Tucker","E_Gordon","J_Harden","C_Capela","D_HouseJr_","A_Rivers","C_Paul"]

example_rockets_lineups = ["P_Tucker-E_Gordon-J_Harden-C_Capela-D_HouseJr_", 
                           "P_Tucker-J_Harden-A_Rivers-C_Capela-D_HouseJr_",
                           "C_Paul-P_Tucker-E_Gordon-J_Harden-C_Capela"]

example_nodes = example_rockets_players + example_rockets_lineups

rockets_bipartite = graph_dict_offrating["Rockets"]
example_graph = rockets_bipartite.subgraph(example_nodes)

example_graph.nodes.data("bipartite")


##################################################################################################################
#code for example bipartite
X, Y= bipartite.sets(example_graph)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i*2.5+.5)) for i, n in enumerate(Y) ) # put nodes from Y at x=2


# nodes
nx.draw_networkx_nodes(example_graph,pos,
                       nodelist=X,
                       node_color='r',
                       node_size=300,
                   alpha=1)


nx.draw_networkx_nodes(example_graph,pos,
                       nodelist=Y,
                       node_color='b',
                       node_size=300,
                   alpha=1)


lineup_weight = [val for val in nx.get_node_attributes(example_graph,"metric").values()]
lineup_weight_full= numpy.repeat(lineup_weight,5)
lineup_weight_full2 = []
lineup_weight_full2[0:5] = lineup_weight_full[10:15]
lineup_weight_full2[5:10] = lineup_weight_full[0:5]
lineup_weight_full2[10:15] = lineup_weight_full[5:10]
scaled_lineup_weights = scale_weights(lineup_weight_full2)

nx.draw_networkx_edges(example_graph, pos = pos, edgelist = example_graph.edges(nbunch = Y), width=scaled_lineup_weights)

pos2 = {}
for n,tup in pos.items():
    if len(n) > 12:
        pos2[n] = (tup[0]+1,tup[1])
    else:
        pos2[n] = (tup[0],tup[1]-.5)
    
plt.text(.9,0-.5,"P_Tucker")
plt.text(.9,.5,'D_HouseJr_')
plt.text(.9,2-.5, "E_Gordon")
plt.text(.9,3-.5, "J_Harden")
plt.text(.9,4-.5, "A_Rivers")
plt.text(.9,5-.5, "C_Capela")
plt.text(.9,6-.5, "C_Paul")

plt.text(2.05,-.25,'D_HouseJr \nP_Tucker \nE_Gordon \nJ_Harden \nC_Capela')

plt.text(2.05,2.2,'D_HouseJr \nP_Tucker \nA_Rivers \nJ_Harden \nC_Capela')

plt.text(2.05,4.5,'C_Paul \nP_Tucker \nE_Gordon \nJ_Harden \nC_Capela')


                           
#nx.draw_networkx_labels(example_graph, pos = pos2)




plt.xlim(0.85,2.4)
plt.ylim(-1,6.5)

#############################################################################################################
#############################################################################################################



#check the example graph has right number of edges
len(rockets_bipartite.edges(["J_Harden"]))
len(example_graph.edges("P_Tucker-E_Gordon-J_Harden-C_Capela-D_HouseJr_"))
len(example_graph.edges(["J_Harden"]))



rockets_example_bipartite_dict= nx.classes.function.get_node_attributes(example_graph, "bipartite")
rockets_example_player_nodes = [key for key,val in rockets_example_bipartite_dict.items() if val ==  "players"]

example_player_graph = bipartite.generic_weighted_projected_graph(example_graph,rockets_example_player_nodes, weight_function = custom_weight2)  



len(example_rockets_players)

len(example_player_graph.edges("E_Gordon"))
len(example_player_graph.edges("C_Capela"))
len(example_player_graph.edges("D_HouseJr_"))


#############################################################################################################
#############################################################################################################

###### DRAW PLAYER ONLY EXAMPLE GRAPH

weights = [example_player_graph[u][v]['weight'] for u,v in example_player_graph.edges()]
scaled_weights = scale_weights(weights)

pos_player = nx.circular_layout(example_player_graph)
nx.draw(example_player_graph, pos = pos_player, width=scaled_weights)

pos3 = {}
for player,tup in pos_player.items():
    if player == "D_HouseJr_" or player == "E_Gordon":
        pos3[player] = (tup[0],tup[1]+.12)
    if player == "J_Harden":
        pos3[player] = (tup[0]-.15,tup[1]+.12)
    if player == "P_Tucker":
        pos3[player] = (tup[0]+.25,tup[1])
    if player == "A_Rivers":
        pos3[player] = (tup[0]-.25,tup[1])
    if player == "C_Paul" or player == "C_Capela":
        pos3[player] = (tup[0],tup[1]-.12)


nx.draw_networkx_labels(example_player_graph,pos = pos3)

plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

#############################################################################################################
#############################################################################################################



