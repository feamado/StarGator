from typing import List

import numpy as np
import pandas as pd
import datetime


class Star:
    def __init__(self, id, id_type,proper_name,luminosity, x0, y0, z0, dist, app_size,ci):
        self.id = id
        self.id_type = id_type
        self.complete_id = f"{self.id}:{self.id_type}"
        self.luminosity = float(luminosity)
        self.proper_name = proper_name
        self.ci = ci
        self.temperature = 4600*(1/(0.92*ci + 1.7) + 1/(0.92*ci +0.62)) #ballestero equation
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
            self.heap.append(x)
            i = len(self.heap) - 1

            while i > 1:
                parent = i // 2
                if self.heap[i].app_size > self.heap[parent].app_size:
                    self.heap[i], self.heap[parent], i = self.heap[parent],self.heap[i], parent
                else:
                    break
        elif self.mode == "temperature":
            self.heap.append(x)
            i = len(self.heap) - 1

            while i > 1:
                parent = i // 2
                if self.heap[i].temperature > self.heap[parent].temperature:
                    self.heap[i], self.heap[parent], i = self.heap[parent], self.heap[i], parent
                else:
                    break
        else:

            while i != 1:
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
    df = pd.read_csv('hyg_v37.csv')

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

        x = row["x"]
        y = row["y"]
        z = row["z"]
        dist = row["dist"]
        lum = row["lum"]
        app_size = row["mag"]
        ci = row["ci"]
        proper_name = row["proper"]
        inp = Star(id, id_type, proper_name,lum, x, y, z, dist, app_size,ci)
        out.insert(inp)
    return out


def create_star_data_list(mode):
    df = pd.read_csv('hyg_v37.csv')

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

        x = row["x"]
        y = row["y"]
        z = row["z"]
        dist = row["dist"]
        lum = row["lum"]
        app_size = row["mag"]
        ci = row["ci"]
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

print(A.heap[1].theta)
A.heap_sort()
print(A.heap[11].luminosity)
end_time = datetime.datetime.now()
execution_time = end_time - start_time
print("Execution time:", execution_time)
