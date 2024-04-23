import math
from typing import List

import numpy as np # numpy library to help with calculations
import pandas as pd # pandas library to help parse the star CSV
import datetime # used to compare quicksort vs heapsort runtimes


class Star: # Star class which holds all the attributes
    def __init__(self, id, id_type, proper_name, luminosity, x0, y0, z0, dist, app_size, ci):
        self.id = id
        self.id_type = id_type
        self.complete_id = f"{self.id}:{self.id_type}"
        self.luminosity = float(luminosity)
        self.proper_name = proper_name
        self.ci = ci
        self.temperature = 4600 * (1 / (0.92 * ci + 1.7) + 1 / (0.92 * ci + 0.62))  # ballestero equation

        self.x0 = float(x0)
        self.y0 = float(y0)
        self.z0 = float(z0)
        cos_th = self.z0 / (np.sqrt(np.sum(np.square([x0, y0, z0]))))
        tan_phi = self.y0 / self.x0
        self.phi = np.arctan(tan_phi)
        if (x0 < 0): # setting up for spherical coordinates
            if (y0 < 0):
                self.phi += math.pi
            else:
                self.phi -= math.pi
        self.theta = np.arccos(cos_th)
        self.theta = math.pi / 2 - self.theta
        self.app_size = float(app_size)
        self.distance = dist
        self.coords = f"{self.x0}, {self.y0}, {self.z0}"

    def get_luminosity(self):
        return float(self.luminosity)

    def get_coords(self):
        return str(self.coords)

    def get_distance(self):
        return float(self.distance)

    def get_complete_id(self):
        return self.complete_id

    def get_temperature(self):
        return self.temperature

    def get_phi(self):
        return self.phi

    def get_theta(self):
        return self.theta

    def get_x(self):
        return self.x0

    def get_y(self):
        return self.y0

    def get_z(self):
        return self.z0


class MaxHeap: # MaxHeap class used for heap sort
    def __init__(self, mode):
        self.heap = [None]
        self.mode = mode
        self.sort_mode = "max"  # max by default

    def insert(self, x): # insert into heap
        if self.sort_mode == "min":
            return
        self.heap.append(x)
        i = len(self.heap) - 1

        if self.mode == "lum": # luminosity sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].luminosity > self.heap[parent].luminosity:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "app_size": # apparent size sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].app_size > self.heap[parent].app_size:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "temperature": # temperature sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].temperature > self.heap[parent].temperature:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "distance": # distance sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].distance > self.heap[parent].distance:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "ci": #color index sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].ci > self.heap[parent].ci:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "x": # cartesian x coordinate sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].x0 > self.heap[parent].x0:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "y": # cartesian y coordinate sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].y0 > self.heap[parent].y0:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "z": # cartesian z coordinate sorting mode

            while i > 1:
                parent = i // 2
                if self.heap[i].z0 > self.heap[parent].z0:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        else:

            while i > 1:
                parent = i // 2
                tmp = self.heap[i]
                if self.heap[i].app_size > self.heap[parent].app_size:
                    self.heap[i], self.heap[parent], i = self.heap[parent], tmp, parent
                else:
                    break
            return

    def pop(self): # pop from heap
        if self.sort_mode  == min:
            return self.min_pop()

        if len(self.heap) == 1:
            return None
        popped = self.heap[1]
        self.heap[1], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]
        del self.heap[len(self.heap) - 1]
        if len(self.heap) == 1:
            return popped

        self.heap[1], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]

        i = 1
        end = len(self.heap)

        if self.mode == "lum":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].luminosity > self.heap[largest].luminosity:
                    largest = left
                if right < end and self.heap[right].luminosity > self.heap[largest].luminosity:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                    i = largest
                else:
                    return popped

        elif self.mode == "app_size":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].app_size >= self.heap[largest].app_size:
                    largest = left
                if right < end and self.heap[right].app_size >= self.heap[largest].app_size:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "temperature":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].temperature >= self.heap[largest].temperature:
                    largest = left
                if right < end and self.heap[right].temperature >= self.heap[largest].temperature:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "ci":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].ci >= self.heap[largest].ci:
                    largest = left
                if right < end and self.heap[right].ci >= self.heap[largest].ci:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped

        elif self.mode == "distance":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].distance >= self.heap[largest].distance:
                    largest = left
                if right < end and self.heap[right].distance >= self.heap[largest].distance:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "x":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].x0 > self.heap[largest].x0:
                    largest = left
                if right < end and self.heap[right].x0 > self.heap[largest].x0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "y":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].y0 > self.heap[largest].y0:
                    largest = left
                if right < end and self.heap[right].y0 > self.heap[largest].y0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "z":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].z0 > self.heap[largest].z0:
                    largest = left
                if right < end and self.heap[right].z0 > self.heap[largest].z0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped

    def re_heapify_helper(self, i, end): # helper function for re_heapify that sorts by attribute
        if self.mode == "lum":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].luminosity > self.heap[largest].luminosity:
                    largest = left
                if right < end and self.heap[right].luminosity > self.heap[largest].luminosity:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                    i = largest
                else:
                    return

        elif self.mode == "app_size":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].app_size > self.heap[largest].app_size:
                    largest = left
                if right < end and self.heap[right].app_size > self.heap[largest].app_size:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        elif self.mode == "temperature":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].temperature > self.heap[largest].temperature:
                    largest = left
                if right < end and self.heap[right].temperature > self.heap[largest].temperature:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        elif self.mode == "distance":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].distance > self.heap[largest].distance:
                    largest = left
                if right < end and self.heap[right].distance > self.heap[largest].distance:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        elif self.mode == "ci":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].ci > self.heap[largest].ci:
                    largest = left
                if right < end and self.heap[right].ci > self.heap[largest].ci:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return


        elif self.mode == "x":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].x0 > self.heap[largest].x0:
                    largest = left
                if right < end and self.heap[right].x0 > self.heap[largest].x0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        elif self.mode == "y":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].y0 > self.heap[largest].y0:
                    largest = left
                if right < end and self.heap[right].y0 > self.heap[largest].y0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        elif self.mode == "z":
            while True:
                left = 2 * i
                right = 2 * i + 1
                largest = i
                if left < end and self.heap[left].z0 > self.heap[largest].z0:
                    largest = left
                if right < end and self.heap[right].z0 > self.heap[largest].z0:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return
        else:
            return

    def min_re_heapify_helper(self, i, end): # helper function that sorts by attribute for min heap
        if self.mode == "lum":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].luminosity < self.heap[smallest].luminosity:
                    smallest = left
                if right < end and self.heap[right].luminosity < self.heap[smallest].luminosity:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                    i = smallest
                else:
                    return

        elif self.mode == "app_size":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].app_size < self.heap[smallest].app_size:
                    smallest = left
                if right < end and self.heap[right].app_size < self.heap[smallest].app_size:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        elif self.mode == "temperature":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].temperature < self.heap[smallest].temperature:
                    smallest = left
                if right < end and self.heap[right].temperature < self.heap[smallest].temperature:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest],i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        elif self.mode == "distance":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].distance < self.heap[smallest].distance:
                    smallest = left
                if right < end and self.heap[right].distance < self.heap[smallest].distance:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        elif self.mode == "ci":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].ci < self.heap[smallest].ci:
                    smallest = left
                if right < end and self.heap[right].ci < self.heap[smallest].ci:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return


        elif self.mode == "x":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].x0 < self.heap[smallest].x0:
                    smallest = left
                if right < end and self.heap[right].x0 < self.heap[smallest].x0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        elif self.mode == "y":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].y0 < self.heap[smallest].y0:
                    smallest = left
                if right < end and self.heap[right].y0 < self.heap[smallest].y0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        elif self.mode == "z":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].z0 < self.heap[smallest].z0:
                    smallest = left
                if right < end and self.heap[right].z0 < self.heap[smallest].z0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return
        else:
            return

    def re_heapify(self, mode,sort_mode = "max" ): # heapify for max heap

        if mode == self.mode and sort_mode == self.sort_mode:
            return

        if sort_mode =="min":
            self.sort_mode = "min"
        self.sort_mode = sort_mode
        self.mode = mode
        if sort_mode == "min":
            i = len(self.heap) // 2
            end = len(self.heap)
            while i > 0:
                self.min_re_heapify_helper(i, end)
                i = i - 1
        else:
            i = len(self.heap) // 2
            end = len(self.heap)
            while i > 0:
                self.re_heapify_helper(i, end)
                i = i - 1

    def min_pop(self): # pop from min heap
        if self.sort_mode !="min":
            return
        if len(self.heap) == 1:
            return None
        popped = self.heap[1]
        self.heap[1], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]
        del self.heap[len(self.heap) - 1]
        if len(self.heap) == 1:
            return popped

        self.heap[1], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]

        i = 1
        end = len(self.heap)

        if self.mode == "lum":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].luminosity < self.heap[smallest].luminosity:
                    smallest = left
                if right < end and self.heap[right].luminosity < self.heap[smallest].luminosity:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                    i = smallest
                else:
                    return popped

        elif self.mode == "app_size":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].app_size <= self.heap[smallest].app_size:
                    smallest = left
                if right < end and self.heap[right].app_size <= self.heap[smallest].app_size:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped
        elif self.mode == "temperature":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].temperature <= self.heap[smallest].temperature:
                    smallest = left
                if right < end and self.heap[right].temperature <= self.heap[smallest].temperature:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped
        elif self.mode == "ci":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].ci <= self.heap[smallest].ci:
                    smallest = left
                if right < end and self.heap[right].ci <= self.heap[smallest].ci:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped

        elif self.mode == "distance":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].distance <= self.heap[smallest].distance:
                    smallest = left
                if right < end and self.heap[right].distance <= self.heap[smallest].distance:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped
        elif self.mode == "x":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].x0 < self.heap[smallest].x0:
                    smallest = left
                if right < end and self.heap[right].x0 < self.heap[smallest].x0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped
        elif self.mode == "y":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].y0 < self.heap[smallest].y0:
                    smallest = left
                if right < end and self.heap[right].y0 < self.heap[smallest].y0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped
        elif self.mode == "z":
            while True:
                left = 2 * i
                right = 2 * i + 1
                smallest = i
                if left < end and self.heap[left].z0 < self.heap[smallest].z0:
                    smallest = left
                if right < end and self.heap[right].z0 < self.heap[smallest].z0:
                    smallest = right

                if smallest != i:
                    self.heap[i], self.heap[smallest], i = self.heap[smallest], self.heap[i], smallest
                else:
                    return popped

    def heap_sort(self,mode,sort_mode): # heap sort function



        if(mode != self.mode or sort_mode != self.sort_mode):
            self.re_heapify(mode,sort_mode)




        swap = []
        if(self.sort_mode == "max"):
            while len(self.heap) != 1:
                swap.append(self.pop())
            swap = [None] + swap
            self.heap = swap
            return
        elif(self.sort_mode == "min"):

            while len(self.heap) != 1:
                swap.append(self.min_pop())
            swap = [None] + swap
            self.heap = swap
            return

    def __str__(self):
        out = f"{self.heap[1]}"
        if len(self.heap) > 2:
            for x in range(2, len(self.heap)):
                out += f", {self.heap[x]}"

        return out



def create_star_data_heap(mode): # parses CSV file to create Star class objects into maxHeap
    start_time = datetime.datetime.now()
    df = pd.read_csv('hyg_v37.csv')
    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)
    # find id
    proper_name = ""
    id = ""
    id_type = ""
    x = 0.0
    y = 0.0
    z = 0.0
    mag = 0.0
    dist = 0.0
    lum = 0.0
    app_size = 0.0
    ci = 0.0
    out = MaxHeap(mode)
    cnt = 0
    for index, row in df.iterrows():

        if row["hip"] == "":
            if row["hd"] == "":
                if row["hr"] == "":
                    if row["gl"] == "":
                        if row["bf"] == "":
                            id = row["id"]
                            id_type = "dbid"
                        else:
                            id = row["gl"]
                            id_type = "gl"
                    else:
                        id = row["hr"]
                        id_type = "hr"
                else:
                    id = row["hr"]
                    id_type = "hr"
            else:
                id = row["hd"]
                id_type = "hd"
        else:
            id = row["hip"]
            id_type = "hip"

        x = float(row["x"])
        y = float(row["y"])
        z = float(row["z"])
        dist = float(row["dist"])
        lum = (row["lum"])
        app_size = float(row["mag"])
        ci = float(row["ci"])
        if ci == math.nan:
            ci = 20
        proper_name = row["proper"]
        inp = Star(id, id_type, proper_name, lum, x, y, z, dist, app_size, ci)
        out.insert(inp)
    return out


def create_star_data_list(mode): # parses CSV file to create Star class objects in a list
    start_time = datetime.datetime.now()
    df = pd.read_csv('hyg_v37.csv')
    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    # find id
    proper_name = ""
    id = ""
    id_type = ""
    x = 0.0
    y = 0.0
    z = 0.0
    mag = 0.0
    dist = 0.0
    lum = 0.0
    app_size = 0.0
    ci = 0.0
    out = []
    for index, row in df.iterrows():

        if row["hip"] == "":
            if row["hd"] == "":
                if row["hr"] == "":
                    if row["gl"] == "":
                        if row["bf"] == "":
                            id = row["id"]
                            id_type = "dbid"
                        else:
                            id = row["gl"]
                            id_type = "gl"
                    else:
                        id = row["hr"]
                        id_type = "hr"
                else:
                    id = row["hr"]
                    id_type = "hr"
            else:
                id = row["hd"]
                id_type = "hd"
        else:
            id = row["hip"]
            id_type = "hip"

        x = float(row["x"])
        y = float(row["y"])
        z = float(["z"])
        dist = float(row["dist"])
        lum = float(row["lum"])
        app_size = float(row["mag"])
        ci = float(row["ci"])
        if app_size == 6.38:
            print(ci, "helloooo")
        proper_name = row["proper"]
        inp = Star(id, id_type, proper_name, lum, x, y, z, dist, app_size, ci)
        out.append(inp)
    return out





def distance_between_stars(s1, s0):  # in parsecs
    x_delta = s1.x0 - s0.x0
    y_delta = s1.y0 - s0.y0
    z_delta = s1.z0 - s0.z0
    sos = np.sum(np.square([x_delta, y_delta, z_delta]))
    return np.sqrt(sos)


#comparison of times

start_time = datetime.datetime.now()
#A = create_star_data_heap("x")
#print(A.heap[1].luminosity)
#print(A.heap[1].temperature)
#A.heap_sort("lum","min")
#print(A.heap[1].luminosity)
end_time = datetime.datetime.now()
execution_time = end_time - start_time
print("Execution time:", execution_time)
arr = [None,9,4,10,11,3]
print(arr)
