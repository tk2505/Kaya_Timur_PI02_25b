#Пример создания мультисписка (вложенного списка):
groups = [['Hong', 'Ryan'], ['Andry', 'Ross'], ['Mike', 'Smith']]

#Пример создания очереди:
from queue import Queue
q = Queue()
q.put(1) 
q.put(2) 
q.put(3)

#Пример реализации дека:
from collections import deque
tasks = deque() 
tasks.append("task1")
tasks.append("task2")
tasks.append("task3") 

#Пример реализации приоритетной очереди:
from queue import PriorityQueue 
q = PriorityQueue()
q.put((2, 'mid-priority item')) 
q.put((1, 'high-priority item')) 
q.put((3, 'low-priority item')) 

#Пример приоритетной очереди с использованием бинарной кучи:
import heapq   
heapq.heappush(customers, (2, "Harry")) 
heapq.heappush(customers, (3, "Charles")) 
heapq.heappush(customers, (1, "Riya")) 
heapq.heappush(customers, (4, "Stacy")) 