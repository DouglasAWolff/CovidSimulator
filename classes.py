import random


class Person:
    def __init__(self, connected_to, screensize, position, _app):
        self.position = position  # sets the position of the person to the position passed into the function
        self.connections = connected_to  # sets the connections of the Person to the array of connections passed into the Class
        self.app = _app  # this lets the class person use the class app defined in main.py

    def update(self):
        self.app.fill(150, 150, 150)  # fills in the circle
        self.app.ellipse(self.position[0], self.position[1], 50, 50)  # draws a circle at the position of the person

    # def infect(self):


class Connection:
    def __init__(self, person1, person2, _people):
        self.people = _people
        self.person1 = person1
        self.person2 = person2
        self.coords1 = self.people.get_coords_for_person(person1)
        self.coords2 = self.people.get_coords_for_person(person2)

    def update(self):
        self.coords1 = self.people.get_coords_for_person(self.person1)
        self.coords2 = self.people.get_coords_for_person(self.person2)



class People:
    def __init__(self, screensize, number_of_people, _app):
        self.people_array = [
            Person([], screensize, [random.randint(0, screensize[0]), random.randint(0, screensize[1])], _app) for i in
            range(number_of_people)]  # fills the people array with people

    def update(self):  # calls the update function on all the people
        for i in range(len(self.people_array)):
            self.people_array[i].update()

    def get_coords_for_person(self, index):  # returns the coordinates for a person by index
        return self.people_array[index].position
