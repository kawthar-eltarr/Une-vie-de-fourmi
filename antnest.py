# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:25:19 2020

@author: straw
"""
import re
import numpy as np
import matplotlib.pyplot as plt

import networkx as nx 
import matplotlib.pyplot as plt

class Ant:
    def __init__(self, idx):
        self.idx = idx
        self.room = 'Sv'
        
class Room:
    def __init__(self, name, contains=[], capacity=1):
        self.name = name
        self.contains = contains
        self.capacity = capacity

class Antnest:
    def __init__(self):
        self.content = self.__load_file__()
        self.nba = self.__find_ants__()
        self.tunnels = self.__find_tunnels__(self.content)
        self.rooms = self.__build_rooms__()

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
        objects = [Room(name='Sv', contains=[Ant(i) for i in range(self.nba)], capacity=float("inf"))]
        for room in rooms:
            if '{' in room:
                n = room.split()[0]
                c = room.split()[2]
                objects.append(Room(name=n, capacity=c))
            else:
                objects.append(Room(name=room))
                
        objects.append(Room(name='Sd', capacity=float("inf")))
        return objects
    
    def look_at_the_graph(self):
        return 0
        
if __name__ == '__main__':
    nest = Antnest()
    
