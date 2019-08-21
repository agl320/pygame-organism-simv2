import time
import math
import pygame
import random

list_direction = ['N', 'S', 'E', 'W']

class Cell():

    # cell x pos, y pos, radius of cell, speed, total hunger capacity,
    # loss per movement, range to spot food, hunger gained when food is eaten
    def __init__(self, cell_x, cell_y, cell_radius, cell_speed, window_width, window_height,
                 cell_hunger, cell_hunger_loss, cell_range, cell_hunger_gain):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.cell_radius = cell_radius
        self.cell_speed =cell_speed
        self.cell_hunger = cell_hunger
        self.cell_hunger_loss = cell_hunger_loss
        self.cell_counter_food = 0
        self.cell_range = cell_range
        self.cell_hunger_gain = cell_hunger_gain
        self.cell_direction = random.choice(list_direction)
        self.window_width = window_width
        self.window_height = window_height


    def position(self):
        return self.cell_x, self.cell_y

    def reproduce(self, list_cell):
        # adds a cell instance to cell list and removes one food
        list_cell.append(Cell(self.cell_x, self.cell_y, self.cell_radius, self.cell_speed, self.window_width, self.window_height))
        self.cell_counter_food -= 1


    def moveToFood(self, food_x, food_y):
        if self.cell_x > food_x:
            self.cell_x -= self.cell_speed
        elif self.cell_x < food_x:
            self.cell_x += self.cell_speed
        elif self.cell_y > food_y:
            self.cell_y -= self.cell_speed
        elif self.cell_y < food_y:
            self.cell_y += self.cell_speed

    # randomly roam
    def roam(self):
        # random number from 0 to 100
        chance_roam = random.randint(0, 100)

        # Change direction, go idle
        if chance_roam < 59:
            self.cell_hunger -= self.cell_hunger_loss
        else:
            if chance_roam <= 70 and chance_roam >= 60:
                self.cell_direction = random.choice(list_direction)

            # makes sure cell does not leave window
            while True:
                if self.cell_direction == 'N' and self.cell_y > self.cell_speed:
                    self.cell_y -= self.cell_speed
                    break
                elif self.cell_direction == 'S' and self.cell_y < self.window_height:
                    self.cell_y += self.cell_speed
                    break
                elif self.cell_direction == 'E' and self.cell_x < self.window_width:
                    self.cell_x += self.cell_speed
                    break
                elif self.cell_direction == 'W' and self.cell_x > self.cell_speed:
                    self.cell_x -= self.cell_speed
                    break
                else:
                    self.cell_direction = random.choice(list_direction)


    # find food; go to food or roam
    def action(self, list_food, list_cell):
        if list_food:
            # list of all foods and their distances
            list_food_distances = []

            # for all foods in the list of foods, get position and distance
            for i in range(len(list_food)):
                food_x, food_y = list_food[i].position()

                # finds the distance between the cell and the food
                list_food_distances.append(math.sqrt((food_x - self.cell_x) ** 2 + (food_y - self.cell_y) ** 2))

            # retrieves the index of the closest food in order to get the actual instance of that food object
            index_closest_food = list_food_distances.index(min(list_food_distances))

            # if the closest food to the cell is within range
            if min(list_food_distances) < self.cell_range:
                food_closest = list_food[index_closest_food]
                food_x, food_y = food_closest.position()

                # if the cell is close enough to food, eat
                if abs(self.cell_x - food_x) <= 3 and abs(self.cell_y - food_y) <= 3:

                    list_food.pop(index_closest_food)
                    self.cell_counter_food += 1
                    self.cell_hunger += self.cell_hunger_gain

                    # cell will reproduce after eating 2 foods
                    if self.cell_counter_food % 5 == 0:
                        self.reproduce(list_cell)

                # else, just move to food
                else:
                    self.moveToFood(food_x, food_y)

            # else, just roam around
            else:
                self.roam()
        else:
            self.roam()

        self.cell_hunger -= self.cell_hunger_loss

        return list_food, list_cell



