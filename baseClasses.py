import os, math, time, random, enum
import numpy as np
import pygame as pg
from shapely import affinity
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon


class DrawableObject(object):
    def __init__(self, polygon):
        self.polygon = polygon
        self.internalFrame = 0

    def draw(self, display):
        pg.gfxdraw.filled_polygon(display, self.polygon.exterior.coords, pg.Color(0,0,0))

    def advanceFrameCounter(self, numberofframes=1):
        self.internalFrame += numberofframes

    def resetFrameCounter(self):
        self.internalFrame = 0

    def getCoords(self):
        return int(list(self.polygon.centroid.coords)[0][0]), int(list(self.polygon.centroid.coords)[0][1])

    def recenter(self, coords):
        coordsDifference = (self.getCoords()[0] - coords[0], self.getCoords()[1] - coords[1])
        self.polygon = affinity.translate(self.polygon, self.getCoords()[0] - coordsDifference[0], self.getCoords()[1] - coordsDifference[1])

class CollisionObject(DrawableObject):
    def colliding(self, PhysicsObject):
        return self.polygon.intersects(PhysicsObject.polygon)

class MovablePhysicsObject(CollisionObject):
    def __init__(self, polygon, directionalvector, speed):
        super().__init__(polygon)
        self.directionalVector = directionalvector
        self.speed = speed

    def teleport(self):
        pass

    def move(self, map):
        denormalizedVector = [math.sqrt(math.pow(self.speed,2)-math.pow(self.directionalVector[1],1)),math.sqrt(math.pow(self.speed,2)-math.pow(self.directionalVector[0],1))]
        self.polygon = affinity.translate(self.polygon, denormalizedVector[0], denormalizedVector[1])

