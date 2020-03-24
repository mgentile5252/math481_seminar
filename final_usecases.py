#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:44:55 2019

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
from networkx.algorithms import bipartite

################################################################################################################################################

# This file shows how to utilize the functions and develop the ranking dictionaries for various metrics. 

################################################################################################################################################
################################################################################################################################################
## OFFENSIVE RATING


team_df_dict = get_team_data()

graph_dict_offrating = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"OFF_RATING")
    print(team_name)
    graph_dict_offrating[team_name] = team_graph

player_player_graph_offrating = {}
for team_name, team_graph in graph_dict_offrating.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_offrating[team_name] = team_player_player_graph


team_player_rankings_offrating = {}
for team_name, team_player_player_graph in player_player_graph_offrating.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_offrating[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Rockets","J_Harden")
dbooker_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Suns","D_Booker")
dmitchell_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Jazz","D_Mitchell")
giannis_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Bucks","G_Antetokounmpo")
dmitchell_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Jazz","D_Mitchell")
njokic_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Nuggets","N_Jokic")
dfox_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Kings","D_Fox")
agordon_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Magic","A_Gordon")
dlillard_teammate_offrating = get_teammate_ranking(player_player_graph_offrating,"Trail Blazers","D_Lillard")



################################################################################################################################################
################################################################################################################################################
    
## True Shooting Percentage


graph_dict_tspct = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"TS_PCT")
    print(team_name)
    graph_dict_tspct[team_name] = team_graph

player_player_graph_tspct = {}
for team_name, team_graph in graph_dict_tspct.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_tspct[team_name] = team_player_player_graph


team_player_rankings_tspct = {}
for team_name, team_player_player_graph in player_player_graph_tspct.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_tspct[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_tspct = get_teammate_ranking(player_player_graph_tspct,"Rockets","J_Harden")



################################################################################################################################################
################################################################################################################################################
    
##  Net Rating 


graph_dict_netrating = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"NET_RATING")
    print(team_name)
    graph_dict_netrating[team_name] = team_graph

player_player_graph_netrating = {}
for team_name, team_graph in graph_dict_netrating.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_netrating[team_name] = team_player_player_graph


team_player_rankings_netrating = {}
for team_name, team_player_player_graph in player_player_graph_netrating.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_netrating[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_netrating = get_teammate_ranking(player_player_graph_netrating,"Rockets","J_Harden")
dbooker_teammate_netrating = get_teammate_ranking(player_player_graph_netrating,"Suns","D_Booker")

    
    
    
    
    
################################################################################################################################################
################################################################################################################################################
    
## Effective Net Rating Percentage


graph_dict_enetrating = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"E_NET_RATING")
    print(team_name)
    graph_dict_enetrating[team_name] = team_graph

player_player_graph_enetrating = {}
for team_name, team_graph in graph_dict_enetrating.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_enetrating[team_name] = team_player_player_graph


team_player_rankings_enetrating = {}
for team_name, team_player_player_graph in player_player_graph_enetrating.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_enetrating[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_enetrating = get_teammate_ranking(player_player_graph_enetrating,"Rockets","J_Harden")
dbooker_teammate_enetrating = get_teammate_ranking(player_player_graph_enetrating,"Suns","D_Booker")

    
    
    
    
    
################################################################################################################################################
################################################################################################################################################
    
## PACE


graph_dict_pace = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"PACE")
    print(team_name)
    graph_dict_pace[team_name] = team_graph

player_player_graph_pace = {}
for team_name, team_graph in graph_dict_pace.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_pace[team_name] = team_player_player_graph


team_player_rankings_pace = {}
for team_name, team_player_player_graph in player_player_graph_pace.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_pace[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_pace = get_teammate_ranking(player_player_graph_pace,"Rockets","J_Harden")

    
     
################################################################################################################################################
################################################################################################################################################
    
## assist turnover raito


graph_dict_ast_to = {}

for team_name, team_df in team_df_dict.items():
    team_name = team_name
    team_graph = create_team_graph_new(team_df,"AST_TO")
    print(team_name)
    graph_dict_ast_to[team_name] = team_graph

player_player_graph_ast_to = {}
for team_name, team_graph in graph_dict_ast_to.items():
    team_bipartite_dict= {}
    team_name = team_name
    print(team_name)
    
    team_bipartite_dict = nx.classes.function.get_node_attributes(team_graph, "bipartite")
    team_player_nodes = [key for key,val in team_bipartite_dict.items() if val ==  "players"]
    team_player_player_graph = bipartite.generic_weighted_projected_graph(team_graph,team_player_nodes, weight_function = custom_weight2)  
    player_player_graph_ast_to[team_name] = team_player_player_graph


team_player_rankings_ast_to = {}
for team_name, team_player_player_graph in player_player_graph_ast_to.items():
    team_node_centrality_dict = nx.eigenvector_centrality_numpy(team_player_player_graph, weight = "weight", tol = 1e-05)
    team_node_centrality_ranking = sorted(team_node_centrality_dict, key = team_node_centrality_dict.__getitem__, reverse=True)
    team_player_rankings_ast_to[team_name] = team_node_centrality_ranking


#format for other players
jharden_teammate_ast_to = get_teammate_ranking(player_player_graph_ast_to,"Rockets","J_Harden")

    