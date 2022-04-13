import random
import math


def find_distance(position1, position2):  # takes in two coordinates and spits out the distance between them
    distance1 = position1[0] - position2[0]
    distance2 = position1[1] - position2[1]
    distance3 = math.sqrt(distance1 * distance1 + distance2 * distance2)

    return distance3


class Person:
    def __init__(self, screensize, position, _app, _people, index_in_people_array):
        self.position = position  # sets the position of the person to the position passed into the function
        self.connected_to = []
        self.app = _app  # this lets the class person use the class app defined in main.py
        self.people = _people
        self.index_in_people_array = index_in_people_array

    def update(self):
        self.app.fill(150, 150, 150)  # fills in the circle
        self.app.ellipse(self.position[0], self.position[1], 50, 50)  # draws a circle at the position of the person

    def find_neighbours_in_aproximate_distance(self, distance, plusminus):  # takes in a number and then spits out that number of closest neighbours
        people_distances = []
        for _person in self.people.people_array:
            people_distances.append([find_distance(self.position, _person.position), _person.index_in_people_array])
        people_distances.sort()

        people_in_distance = [distance_person[1] for distance_person in people_distances if
                              distance_person[0] < random.randint(distance - plusminus, distance + plusminus)]

        return people_in_distance

    # def infect(self):


class Connection:
    def __init__(self, person1, person2, _people, _app):
        self.people = _people
        self.app = _app
        self.person1 = person1
        self.person2 = person2
        self.coords1 = self.people.get_coords_for_person(person1)
        self.coords2 = self.people.get_coords_for_person(person2)

    def update(self):
        self.coords1 = self.people.get_coords_for_person(self.person1)
        self.coords2 = self.people.get_coords_for_person(self.person2)
        self.app.line(self.coords1[0], self.coords1[1], self.coords2[0], self.coords2[1])

class Connections:
    def __init__(self, _people, _app):
        self.app = _app
        self.people = _people
        self.connections = []
        for first_person in range(len(self.people.people_array)):  # iterates through the people array, setting first person to the index
            for second_person in self.people.people_array[first_person].connected_to:  # iterates through the connections array of the first person
                self.connections.append(Connection(first_person, second_person, self.people, self.app))  # appends a connection to the connections list

    def update(self):

        for connection in self.connections:
            connection.update()

    def is_connection_crossing_another(self, first_person, second_person):
        pass


class People:
    def __init__(self, screensize, number_of_people, _app):
        self.people_array = [
            Person(screensize,
                   [random.randint(0, screensize[0]), random.randint(0, screensize[1])], _app, self, i) for i in
            range(number_of_people)]  # fills the people array with people

        for person in self.people_array:
            person.connected_to = person.find_neighbours_in_aproximate_distance(200, 200)

    def update(self):  # calls the update function on all the people
        for i in range(len(self.people_array)):
            self.people_array[i].update()

    def get_coords_for_person(self, index):  # returns the coordinates for a person by index
        return self.people_array[index].position
