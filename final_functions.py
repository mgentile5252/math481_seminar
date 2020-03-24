#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:34:31 2019

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

########################################################################################################################################################################################################
########################################################################################################################################################################################################



headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def get_team_data(stat_page = "Advanced"):
    '''
    Draws data from the stats.nba.com team lineups and creates a dictionary keyed by team name where 
    the value is a pandas dataframe containing all the lineup information
    
    Arguement is which stats page's data is to be pulled, default is advanced. Can also be ran for 
    "Base", "Misc", "Four Factors", "Scoring", "Usage", "Defense", "Opponent"
    '''
    teams = nba_api.stats.static.teams

    list_teams = teams.get_teams()
    #print(list_teams)
    
    
    team_df_dict = {}

    for team_dict in list_teams:
        
        team_name = team_dict['nickname']
        print(team_name)
        team_id = team_dict['id']
        team_df_api = teamdashlineups.TeamDashLineups(team_id = team_id, season = "2018-19", measure_type_detailed_defense = stat_page, timeout=30, headers = headers)
        print(team_name)
        team_df = team_df_api.lineups.get_data_frame()
        
        team_df["GROUP_NAME"] = [group.replace(" ","").replace(".", "_") for group in team_df["GROUP_NAME"]]
 
        
        team_df_dict[team_name]=team_df
        
    return team_df_dict




########################################################################################################################################################################################################
########################################################################################################################################################################################################




def custom_weight2(team_graph, u, v, weight = "weight"):
    '''
    
    Creates the edge weight for the projected player only graph. Weight between two players is
    the weighted average of the metric value of the lineups that the two players played in 
    together (weighted by minutes that each lineup player together)
    
    '''
    weight = 0
    total_min = 0
    
    for lineup in set(team_graph[u]) & set(team_graph[v]):
        
        weight += team_graph.nodes[lineup]["minutes"] * team_graph.nodes[lineup]["metric"]
        total_min += team_graph.nodes[lineup]["minutes"]
        
    weight = weight/total_min
    
    return weight
               


########################################################################################################################################################################################################
########################################################################################################################################################################################################


def create_team_graph_new(team_df, metric):
    '''
    Creates the bipartite graph with player and lineup nodes for each of team. 
    Only lineups that logged more than 27 minutes together are included. The lineup nodes
    hold attributes for metric (argument) values and minutes value, both are needed for 
    the projection step. 
    
    
    '''
    
    team_lineup_groups = team_df['GROUP_NAME']

    team_lineups_string = [group.replace(" ","").replace(".", "_") for group in team_lineup_groups]
    
    team_lineups_split = [group.split("-") for group in team_lineups_string] 

    team_roster = numpy.unique(functools.reduce(operator.add, team_lineups_split))
    
    team_graph = nx.Graph() 
    
    team_graph.add_nodes_from(team_roster, bipartite = "players")

    team_graph.add_nodes_from(team_lineups_string, bipartite = "lineups")
    
    attribute_dict = {}
    for lineup in team_lineups_string:
        attribute_dict[lineup] = {}
        lineup_data = team_df.loc[team_df["GROUP_NAME"] == lineup]
        min_val = lineup_data["MIN"].values[0]
    
        if min_val == 0:
            min_val = 1
        metric_val = lineup_data[metric].values[0]
        attribute_dict[lineup]["minutes"] = min_val
        attribute_dict[lineup]["metric"] = metric_val
        
    nx.set_node_attributes(team_graph, attribute_dict)
        
    ###CHANGE
    #rockets_bipartite.nodes.data("minutes")
    node_att_dict = team_graph.nodes.data("minutes")
    team_lineups_string_new = []
    for lineup in team_lineups_string:
        if node_att_dict[lineup] <= 27:
            team_graph.remove_node(lineup)
            #team_graph.remove_edge
        else:
            team_lineups_string_new.append(lineup)
    
    

    for player in team_roster:
        for lineup in team_lineups_string_new:
            if player in lineup:
                team_graph.add_edge(player,lineup)
    team_graph.remove_nodes_from(list(nx.isolates(team_graph)))
                
    l, r = nx.bipartite.sets(team_graph)
    pos = {}

    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))
    
   
    return team_graph






########################################################################################################################################################################################################
########################################################################################################################################################################################################




def get_teammate_ranking(graph_dictionary,team_name,player_name):
    '''
    Creates list of ranking of teammates based on weight of shared edge with inputted player. 
    
    '''
    
    team_graph = graph_dictionary[team_name]
    
    player_edges = list(team_graph.edges(player_name))
    
    player_edge_weights_dict = {}
    
    for edge in player_edges:
        
        player_edge_weights_dict[edge[1]] = team_graph.get_edge_data(edge[0],edge[1])["weight"]
    
    sorted_player_edge_weights_dict = sorted(player_edge_weights_dict, key=lambda k: player_edge_weights_dict[k], reverse=True)
           
    return sorted_player_edge_weights_dict
    


########################################################################################################################################################################################################
########################################################################################################################################################################################################



def scale_weights(weight_list):
    wmin = min(weight_list)
    wmax = max(weight_list)
    scaled_weights = []
    for i in range(len(weight_list)):
        val = 1 + ((weight_list[i]-wmin)/(wmax-wmin))*(6-1)
        scaled_weights.append(val)
        
        
        
    return scaled_weights



