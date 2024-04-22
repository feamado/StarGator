import math
from typing import List

import numpy as np
import pandas as pd
import datetime


class Star:
    def __init__(self, id, id_type, proper_name, luminosity, x0, y0, z0, dist, app_size, ci):
        self.id = id
        self.id_type = id_type
        self.complete_id = f"{self.id}:{self.id_type}"
        self.luminosity = float(luminosity)
        self.proper_name = proper_name
        self.ci = ci
        if self.ci == np.nan:
            self.ci = 0
        self.temperature = 4600 * (1 / (0.92 * ci + 1.7) + 1 / (0.92 * ci + 0.62))  # ballestero equation

        self.x0 = float(x0)
        self.y0 = float(y0)
        self.z0 = float(z0)
        cos_th = self.z0 / (np.sqrt(np.sum(np.square([x0, y0, z0]))))
        tan_phi = self.y0 / self.x0
        self.phi = np.arctan(tan_phi)
        self.theta = np.arcsin(cos_th)
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


class MaxHeap:
    def __init__(self, mode):
        self.heap = [None]
        self.mode = mode

    def insert(self, x):
        self.heap.append(x)
        i = len(self.heap) - 1

        if self.mode == "lum":

            while i > 1:
                parent = i // 2
                if self.heap[i].luminosity > self.heap[parent].luminosity:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "app_size":

            while i > 1:
                parent = i // 2
                if self.heap[i].app_size > self.heap[parent].app_size:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "temperature":

            while i > 1:
                parent = i // 2
                if self.heap[i].temperature > self.heap[parent].temperature:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "distance":

            while i > 1:
                parent = i // 2
                if self.heap[i].distance > self.heap[parent].distance:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "ci":

            while i > 1:
                parent = i // 2
                if self.heap[i].ci > self.heap[parent].ci:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "x":

            while i > 1:
                parent = i // 2
                if self.heap[i].x0 > self.heap[parent].x0:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "y":

            while i > 1:
                parent = i // 2
                if self.heap[i].y0 > self.heap[parent].y0:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        elif self.mode == "z":

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

    def pop(self):

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
                if left < end and self.heap[left].app_size > self.heap[largest].app_size:
                    largest = left
                if right < end and self.heap[right].app_size > self.heap[largest].app_size:
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
                if left < end and self.heap[left].temperature > self.heap[largest].temperature:
                    largest = left
                if right < end and self.heap[right].temperature > self.heap[largest].temperature:
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
                if left < end and self.heap[left].ci > self.heap[largest].ci:
                    largest = left
                if right < end and self.heap[right].ci > self.heap[largest].ci:
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
                if left < end and self.heap[left].distance > self.heap[largest].distance:
                    largest = left
                if right < end and self.heap[right].distance > self.heap[largest].distance:
                    largest = right

                if largest != i:
                    self.heap[i], self.heap[largest], i = self.heap[largest], self.heap[i], largest
                else:
                    return popped
        elif self.mode == "x0":
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
        elif self.mode == "y0":
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
        elif self.mode == "z0":
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

    def re_heapify_helper(self, i, end):
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
        
        
        elif self.mode == "x0":
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
        elif self.mode == "y0":
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
        elif self.mode == "z0":
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
        else:
            return 

    def re_heapify(self, mode):
        if mode == self.mode:
            return
        self.mode = mode

        i = len(self.heap) // 2
        end = len(self.heap)
        while i >= 1:
            self.re_heapify_helper(i, end)
            i = i - 1

    def heap_sort(self):
        swap = []
        while len(self.heap) != 1:
            swap.append(self.pop())
        swap = [None] + swap
        self.heap = swap

    def __str__(self):
        out = f"{self.heap[1]}"
        if len(self.heap) > 2:
            for x in range(2, len(self.heap)):
                out += f", {self.heap[x]}"

        return out

def create_star_data_heap(mode):
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
        ci = row["ci"]
        proper_name = row["proper"]
        inp = Star(id, id_type, proper_name, lum, x, y, z, dist, app_size, ci)
        out.insert(inp)
    return out


def create_star_data_list(mode):
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
    x_delta = s1.x - s0.x
    y_delta = s1.y - s0.y
    z_delta = s1.z - s0.z
    sos = np.sum(np.square([x_delta, y_delta, z_delta]))
    return np.sqrt(sos)


def quick_sort(x):
    return


start_time = datetime.datetime.now()
A = create_star_data_heap("lum")
B = create_star_data_heap("temperature")
print(A.heap[1].luminosity)
print(A.heap[1].temperature)
print(B.heap[1].luminosity)
A.re_heapify("temperature")
print(A.heap[1].temperature)
print(B.heap[1].temperature)
end_time = datetime.datetime.now()
execution_time = end_time - start_time
print("Execution time:", execution_time)

