import sys
import math
import time
import random
import itertools
import cvxpy as cp
import numpy as np
import pandas as pd
from math import sin
import networkx as nx
import matplotlib.pyplot as plt
from pyflowchart import Flowchart
class flow:
    def __init__(self, source, destination, size, rate):
        self.source = source
        self.destination = destination
        self.size = size
        self.rate = rate
    def __str__(self):
        return "S:" + str(self.source) +" D:" + str(self.destination) \
    + " size:" + self.size + " Rate:" + str(self.rate)
class pack:
    packetSize = 1
    def __init__(self, source, destination):
        self.size = self.packetSize
        self.source = source
        self.destination = destination

    def setTimer(self,start):
        self.start = start
        return self.start
    def __str__(self):
        return "S:" + str(self.source) + ", D:" + \
               str(self.destination) + ", ID:"+ str(id(self))+" Initiated Time:"+str(self.start)+"\n"
class ntwrk:
    def __init__(self, topo, bufferSize):
        self.network = topo
        self.n = len(topo)
        # rate of generating packet at source
        # self.demand = [[0 for i in range(self.n)] for i in range(self.n)]
        self.BW = [[0 for i in range(self.n)] for i in range(self.n)]
        self.bufferSize = bufferSize
        self.buffer = [[[] for i in range(self.n)] for i in range(self.n)]
    def __str__(self):
        # print(self.network)
        print("%%%%%%%%NETWORK VISUALISATION%%%%%%%%%%%%")
        for i in range(self.n):
            print(f"switch {i} ====>:")
            print("Neighbors:")
            for j in range(self.n):
                if self.network[i][j] > 0:
                    print(f"   edge   {j} ====>")
                    cacheStr = "\tCache:\n"
                    for p in self.buffer[i][j]:
                        cacheStr += "\t       " + str(p) + " \n"
                    if len(self.buffer[i][j]) == 0:
                        cacheStr += "\t       " + '\x1b[6;30;42m' + "EMPTY" '\x1b[0m'
                    print(cacheStr)
        print("***************END*************")
        return ""
class cntrllr:
    def __init__(self, network):
        self.first = True
        self.network = network
        self.flowArr = []
        self.timer = 0
        self.bufferFlag = []#[[source, destination]] = [[1,2], [5,6], [5,2], [3,2], [2,3]]
        # for q in self.bufferFlag:
            #pop the first element in q
            # self.network.buffer[q[1]][q[2]].pop()
    def setFlowDict(self, inOutPoint, packetTime):
        if self.first:
            self.first = False
            self.flowDict = {}
        temp = {}
        tempNum = 0
        for key in packetTime:
            temp[tempNum] = key
            tempNum += 1
        self.flowDict[inOutPoint] = packetTime
    def simulation(self):
        result = 0
        self.droppedNum = {0:0}
        droppedSum = 0
        sum = 0
        sumsum = self.flowDict[(0,1)]
        sumi = len(sumsum)
        proccessedList = 0
        queueState=''
        self.droppedNum[self.timer] = 0
        while proccessedList < sumi:
                                    #  /\
                                    # 0o\o0 it is optimal to iterate over proccessed packets \in dropped, routed
            #                           ()
            queueState = ''
            print(f"\033[91m{self.timer}\033[0m")
            # input(str(sumi)+" "+ str(proccessedList))
            for inp,d in self.flowDict.items():
                #           \\    //
                #            \\  //
                #             \\//
                #  /\         //\\
                # 0o\o0      //  \\
                #   ()      //    \\
                #thi lopp is not optimal, it iterate over all demands in a dictionary
                for i in range(self.network.n):
                    for j in range(self.network.n):
                        if len(self.network.buffer[i][j]) > 0:
                            print("let's pop",self.network.buffer[i][j])
                            temp = self.network.buffer[i][j].pop(0)
                            print(str(temp))

                            print("Got poped",self.network.buffer[i][j])
                            for kk in self.network.buffer[i][j]:
                                print(str(kk))
                            proccessedList += 1
                            formatted_list = ', '.join(map(str, self.network.buffer[i][j]))
                            queueState += "SUCCESS"
                source = (list(inp)[0])
                destination = (list(inp)[1])
                start = self.timer
                dropFlag = False
                end = start + 0.9999
                for packet in d:
                    if float(packet) >= float(start) and float(packet) <= float(end):
                        tempP = pack(source, destination)
                        tempP.setTimer(packet)
                        if len(self.network.buffer[source][source+1]) < self.network.bufferSize:
                            self.network.buffer[source][source+1].append(tempP)
                            queueState += str(tempP)
                            sum +=1
                        else:
                            if dropFlag == False:
                                dropFlag = True
                                droppedSum += 1
                            result += 1
                            queueState += "packet dropped at"+ str(packet)
                            proccessedList += 1
                            self.droppedNum[self.timer] += 1
                            # self.droppedNum[self.timer + 1] = self.droppedNum[self.timer] + 1
                print("STATE:::::\n",queueState)
            # if dropFlag == False:
            self.droppedNum[self.timer + 1] = self.droppedNum[self.timer]
            self.timer += 1

        print("DRP:",str(result))
        print("TOT",str(sumi))
        print("here")
        return result,sumi
