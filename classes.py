import random


class Person:
    def __init__(self, connected_to, screensize, _app):
        self.position = [random.randint(0, screensize[0]), random.randint(0, screensize[0])]  # sets the position of the person to a random point within the screen
        self.connections = connected_to  # sets the connections of the Person to the array of connections passed into the Class
        self.app = _app  # this lets the class person use the class app defined in main.py

    def update(self):
        self.app.fill(150, 150, 150)  # fills in the circle
        self.app.ellipse(self.position[0], self.position[1], 50, 50)  # draws a circle at the position of the person

    # def infect(self):


class People:
    def __init__(self, screensize, number_of_people, _app):
        self.people_array = [Person([], screensize, _app) for i in range(number_of_people)] # fills the people array with people

    def update(self):
        for i in range(len(self.people_array)):
            self.people_array[i].update()