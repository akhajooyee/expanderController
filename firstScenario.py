from main import ntwrk
from main import cntrllr
import math
import time
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

# exit(0)
STRATtopo = [[0,1,0,0,0,0],\
[1,0,1,0,0,0],\
[0,1,0,1,0,0],\
[0,0,1,0,1,0],\
[0,0,0,1,0,1],\
[0,0,0,0,1,0]]
STRAT = ntwrk(STRATtopo, 4)
STRATn =STRAT.n
STRAT.BW = [[1 for i in range(STRATn)] for j in range(STRATn)]
c1 = cntrllr(STRAT)
#
#
# def routWtih5Srvers(self):
#     # the dropped packets num
#     result = 0
#     # at time t how many packets are dropped
#     self.droppedNum = {0: 0}
#     # this one is the same as result
#     droppedSum = 0
#     # count the all packets generated
#     sum = len(self.flowDict.items())
#     proccessed = 0
#     # the simulation run until 1000 time units
#     while proccessed > sum:
#         # inp is the (source, destination) tuple and d is the time of packet generated
#         passed = []
#         generated = []
#         print("==========================", str(self.timer), "========================")
#         for inp, d in self.flowDict.items():
#             suc = []
#             source = (list(inp)[0])
#             destination = (list(inp)[1])
#             start = self.timer
#             end = start + 0.9999
#             print("******GENRATING____PACKETS******")
#             for packet in d:
#                 if float(packet) >= float(start) and float(packet) <= float(end):
#                     # generate the new packets
#                     tempP = pack(source, destination, packet)
#                     generated.append(tempP)
#                     proccessed += 1
#                     d.remove(packet)
#                     print("packet ", str(tempP), " is in the generated queue")
#
#         print("******SELECT_____PASSING____PACKETS******")
#         for i in range(self.network.n):
#             for j in range(self.network.n):
#                 # for i in range(self.bandWidth):
#                 if self.network.buffer[i][j]:
#                     # dequeue passing packets
#                     passed.extend(self.network.buffer[i][j][:self.bandWidth])
#                     self.network.buffer[i][j] = self.network.buffer[i][j][self.bandWidth:]
#                     for el in passed:
#                         print("selected packets: ", str(el))
#                     for el in self.network.buffer[i][j]:
#                         print(str(el), " Left")
#
#         # spray generated packets
#         print("buffer size", str(self.network.bufferSize))
#         for el in generated:
#             if len(self.network.buffer[el.source][el.destination]) < self.network.bufferSize:
#                 self.network.buffer[el.source][el.destination].append(el)
#                 print("packet ", str(el), "is generated at switch", str(el.source))
#             else:
#                 print("packet ", str(el), "is dropped and switch", str(el.source), "'s queue is full")
#                 result += 1
#
#         # pass selected packets for passing to the next node
#         for el in passed:
#             if len(self.network.buffer[el.destination][el.source]) < self.network.bufferSize:
#                 self.network.buffer[el.destination][el.source].append(el)
#             else:
#                 print("packet ", str(el), "is dropped and switch", str(el.destination), "'s queue is full")
#                 result += 1
#         print("lets take a look at network\n", str(self.network))
#         for el in passed:
#             print("selected packets: ", str(el))
#         # proccess packets at the destinations
#         for el in passed:
#             for i in range(self.network.n):
#                 for j in range(self.network.n):
#                     if el in self.network.buffer[j][i]:
#                         if j == el.destination:
#                             self.network.buffer[j][i].remove(el)
#                             suc.append(el)
#                             print("packet ", str(el), "routed successfully")
#         # input(str(result)+"packets dropped")
#
#         self.timer += 1
#
#     print("dropped", str(result))
#     return result, sum


def generate_packets(rate, duration):
    t = 0
    count = 0
    while count < 1000:
        print(f"\033[92m{int(t/duration*100)}\033[0m")
        time_interval = np.random.exponential(1.0 / rate)
        yield t, time_interval
        t += time_interval
        count += 1

average_rate = 1  # Adjust this value to your desired average rate (r packets/second)
# simulation_duration = 100  # Adjust this value to the desired simulation duration in seconds
simulation_duration = 3 # Adjust this value to the desired simulation duration in seconds

xPoints = []
yPoints = []
average_rate = 0.1
packetNumberList = []
while average_rate < 15:


    print(f"\033[94mB{str(average_rate)}\033[0m")
    c1 = cntrllr(STRAT)
    average_rate += 1


    packet_generator = generate_packets(average_rate, simulation_duration)
    demand = []

    for packet_number, (packet_time, interval) in enumerate(packet_generator, start=1):

        # print(f"Packet {packet_number}: Time = {packet_time:.3f} seconds")
        demand.append(packet_time)
        time.sleep(interval)  # Simulate packet transmission time

    #########simulation has been started already###########
    print(". #########simulation has been started already###########")
    c1.setFlowDict((0,1), demand)
    dropNum, tot = c1.simulation()
    # input(str(dropNum)+'---'+str(tot))
    ######### results illustration###############
    print(".  ######### results illustration###############")
    xPoints.append(average_rate)
    yPoints.append(math.log10(((dropNum/tot))))
    packetNumberList.append(tot)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$dropped number is ", str(dropNum/tot))
    print("x: ", str(xPoints))
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$average number is ", str(average_rate))
    # plt.ion()
    print("y: ", str(yPoints))
    # print(str(average_rate))
    print(str(packetNumberList))
plt.plot(xPoints, yPoints,  marker='*')
plt.xlabel("packet rate generating")
plt.ylabel("average drop ration")
print(str(packetNumberList))
print("here")
# plt.savefig('/Users/khajoii/PycharmProjects/simulatorFirstScenario/venv/chart.png')
plt.show()
print(str(average_rate))
