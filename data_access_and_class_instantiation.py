from typing import List

import numpy as np
import pandas as pd


class Star:
    def __init__(self, id, id_type, luminosity, x0, y0, z0,dist, app_size):
        self.id = id
        self.id_type = id_type
        self.name = f"{self.id}:{self.id_type}"
        self.luminosity = float(luminosity)
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.z0 = float(z0)
        self.app_size = float(app_size)
        self.distance = dist
        self.coords = f"{self.x0}, {self.y0}, {self.z0}"
    def get_luminosity(self):
        return float(self.luminosity)

    def get_coords(self):
        return str(self.coords)

    def get_distance(self):
        return float(self.distance)
    def get_name(self):
        return self.name


class MaxHeap:
    def __init__(self):
        self.heap = [None]

    def insert(self, x):
        self.heap.append(x)
        i = len(self.heap) - 1

        while i != 1:
            parent = i // 2
            tmp = self.heap[i]
            if self.heap[i] > self.heap[parent]:
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
        while True:
            left = 2 * i
            right = 2 * i + 1

            if left < end and self.heap[i] < self.heap[left]:
                self.heap[left], self.heap[i] = self.heap[i], self.heap[left]
                i = left
            elif right < end and self.heap[i] < self.heap[right]:
                self.heap[right], self.heap[i] = self.heap[i], self.heap[right]
                i = right
            else:
                return popped

    def __str__(self):
        out = f"{self.heap[1]}"
        if len(self.heap) > 2:
            for x in range(2, len(self.heap)):
                out += f", {self.heap[x]}"

        return out


def create_star_data_heap():
    df = pd.read_csv('hyg_v37.csv')
    out = MaxHeap()

    select_cols = ["id","hip","hd","hr","gl","bf","x","y","z","mag","dist","lum",""]
    #find id
    name = ""
    id_type = ""
    x = 0.0
    y = 0.0
    z = 0.0
    mag = 0.0
    dist = 0.0
    lum = 0.0
    app_size = 0
    out = []
    for index,row in df.iterrows():

        if row["hip"] == "":
            if row["hd"] == "":
                if row["hr"] == "":
                    if row["gl"] =="":
                        if row["bf"] =="":
                            name = row["id"]
                            id_type = "dbid"
                        else:
                            name = row["gl"]
                            id_type = "gl"
                    else:
                        name = row["hr"]
                        id_type = "hr"
                else:
                    name = row["hr"]
                    id_type = "hr"
            else:
                name = row["hd"]
                id_type = "hd"
        else:
            name = row["hip"]
            id_type = "hip"

        x = row["x"]
        y = row["y"]
        z = row["z"]
        mag = row["mag"]
        dist = row["dist"]
        lum = row["lum"]
        app_size = row["mag"]

        inp = Star(name,id_type,lum,x,y,z,dist,app_size)
        out.append(inp)
    return out


A = create_star_data_heap()




