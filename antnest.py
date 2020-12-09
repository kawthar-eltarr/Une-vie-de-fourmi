# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:25:19 2020

@author: straw
"""
import re
import numpy as np
import random
from copy import copy

import networkx as nx 
import matplotlib.pyplot as plt

class Ant:
    def __init__(self, idx):
        self.idx = idx
        self.room = 'Sv'
        
class Room:
    def __init__(self, idx, name, contains=[], capacity=1):
        self.idx = idx
        self.name = name
        self.contains = contains
        self.capacity = capacity

class Antnest:
    def __init__(self):
        self.content = self.__load_file__()
        self.nba = self.__find_ants__()
        self.tunnels = self.__find_tunnels__(self.content)
        self.rooms = self.__build_rooms__()
        self.M = self.adjacency_matrix()

    def __load_file__(self):
        file = open("Nests/fourmiliere_quatre.txt", "r")
        content = file.read()
        file.close()
        return content
        
    def __find_ants__(self):
        res = re.findall(r"f=[0-9]*", self.content)
        return int(res[0][2:])
    
    def __find_tunnels__(self, content):
        res = re.findall(r"S[0-9a-z] - S[0-9a-z]", content)
        return res
    
    def __find_rooms__(self):
        content = self.content
        res = re.findall(r"f=[0-9]*", content)
        content = content.replace(res[0], '')
        res = self.__find_tunnels__(content)
        for r in res:
            content = content.replace(r, '')
        rooms = re.findall(r"S[0-9a-z].*", content)
        return rooms
    
    def __build_rooms__(self):
        rooms = self.__find_rooms__()
        objects = [Room(idx=0, name='S0', contains=[Ant(i) for i in range(self.nba)], capacity=float("inf"))]
        for i, room in enumerate(rooms, 1):
            if '{' in room:
                n = room.split()[0]
                c = int(room.split()[2])
                objects.append(Room(idx=i, name=n, capacity=c))
            else:
                objects.append(Room(idx=i, name=room))
        objects.append(Room(idx=len(objects), name='S{}'.format(len(objects)), capacity=float("inf")))
        return objects
    
    def adjacency_matrix(self):
        nbr = len(self.rooms)
        M = np.zeros((nbr, nbr))
        for tunnel in self.tunnels:
            if 'v' in tunnel:
                tunnel = tunnel.replace('v', '0')
            if 'd' in tunnel:
                tunnel = tunnel.replace('d', '{}'.format(nbr-1))
            ind = re.findall(r"(?!S)[0-9]", tunnel)
            ind = [int(i) for i in ind]
            M[ind[0]][ind[1]] = 1
            M[ind[1]][ind[0]] = 1
        return M
    
    def look_at_the_graph(self):
        G = nx.from_numpy_array(self.M)
        dic = {0: 'Sv'}
        nbr = len(self.rooms)-1
        for i in range(1, nbr):
            dic[i] = self.rooms[i].name
        dic[len(self.rooms)-1] = 'Sd'
        G = nx.relabel_nodes(G, dic)
        nx.draw(G, with_labels=True, font_size=8)
        plt.show()
    
    def adjacent_room(self, room):
        ind = room.idx
        emp = np.where(self.M[ind] == 1)
        list_adj = []
        for i in np.nditer(emp):
            if len(self.rooms[i].contains) < self.rooms[i].capacity:
                 list_adj.append(self.rooms[i])
        return list_adj
    
    def test(self, room1, room2):
        if len(room1.contains) > room2.capacity:
            room2.contains = copy(room2.contains) + copy(room1.contains[0:room2.capacity])
            room1.contains = copy(room1.contains[room2.capacity:])
        else:
            room2.contains = copy(room2.contains) + copy(room1.contains)
            room1.contains = []
        return room1, room2
        
    
    def shift(self):
        nbr = len(self.rooms)-1
        while len(self.rooms[-1].contains) < self.nba :
            for k in range(nbr,-1,-1):
                print('Current room', self.rooms[k].name)
                print('Contains', len(self.rooms[k].contains))
                print()
                list_adj = self.adjacent_room(self.rooms[k])
                if not list_adj:
                    pass
                else:
                    adj = random.choice(list_adj)
                    print('Next room', adj.name)
                    print('Contains', len(adj.contains))
                    print()
                    self.rooms[k], adj = self.test(self.rooms[k], adj)
                    #print('-------------------')
            break
        
if __name__ == '__main__':
    nest = Antnest()
    nest.shift()
    
    










