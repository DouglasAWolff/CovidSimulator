import random
import math

import mouse


def find_difference(value1, value2):
    if value1 > value2:
        return value1 - value2
    elif value2 > value1:
        return value2 - value1
    else:
        return 0


def find_distance(position1, position2):  # takes in two coordinates and spits out the distance between them
    distance1 = position1[0] - position2[0]
    distance2 = position1[1] - position2[1]
    distance3 = math.sqrt(distance1 * distance1 + distance2 * distance2)

    return distance3


def find_angle_from_one_point_to_another(position1, position2):
    angle = math.atan2(position2[1] - position1[1], position2[0] - position1[0])  # the angle is from pointing upwards
    return angle


class Person:
    def __init__(self, screensize, position, _app, _people, index_in_people_array):
        self.position = position  # sets the position of the person to the position passed into the function
        self.connected_to = []
        self.app = _app  # this lets the class person use the class app defined in main.py
        self.people = _people
        self.index_in_people_array = index_in_people_array
        self.forces = []
        self.mass = 10
        self.resistance = 1.08
        self.velocity = [0, 0]
        self.selected = False
        self.size = 30 + (2.5 * len(self.connected_to))
        self.color = (150, 150 + (5 * len(self.connected_to)), 150 + (5 * len(self.connected_to)))
        self.screensize = screensize
        self.infected = False
        self.been_infected_for = 0
        self.deleted = False

    def update(self, check_mouse_left=False, check_mouse_right=False):
        if not self.deleted:
            if check_mouse_left:
                if self.position[0] + self.size > self.app.mouseX > self.position[0] - self.size:
                    if self.position[1] + self.size > self.app.mouseY > self.position[1] - self.size:
                        self.selected = True
                        self.people.person_selected = True

            if check_mouse_right:
                if self.position[0] + self.size > self.app.mouseX > self.position[0] - self.size:
                    if self.position[1] + self.size > self.app.mouseY > self.position[1] - self.size:
                        self.delete()
                        return

            if self.selected:
                if mouse.is_pressed(button='left'):
                    self.position = [self.app.mouseX, self.app.mouseY]
                else:
                    self.selected = False
                    self.people.person_selected = False
                    self.calculate_velocity_vector()
                    self.move_away_if_touching_walls()
                    self.apply_velocity()

            else:
                self.calculate_velocity_vector()
                self.move_away_if_touching_walls()
                self.apply_velocity()

            if self.infected:
                self.color = (255,0,0)

            else:
                self.color = (150, 150 + (5 * len(self.connected_to)), 150 + (5 * len(self.connected_to)))

            self.size = 30 + (2.5 * len(self.connected_to))

    def draw(self):
        if not self.deleted:
            self.app.fill(self.color[0], self.color[1], self.color[2])  # fills in the circle
            self.app.ellipse(self.position[0], self.position[1], self.size,
                             self.size)  # draws a circle at the position of the person

    def find_neighbours_in_approximate_distance(self, distance, plusminus):  # takes in a number and then spits out that number of closest neighbours
        people_distances = []
        for _person in self.people.people_array:
            people_distances.append([find_distance(self.position, _person.position), _person.index_in_people_array])

        people_in_distance = [distance_person[1] for distance_person in people_distances if distance_person[0] < random.randint(distance - plusminus, distance + plusminus) and distance_person[1] != self.index_in_people_array]

        return people_in_distance

    def add_force(self, force, direction):
        self.forces.append([force, direction])

    def calculate_total_forces(self):
        resultant_force = [0, 0]
        magnitudes_and_force_vectors = []
        for force in self.forces:
            magnitudes_and_force_vectors.append([math.cos(force[1]) * force[0], math.sin(force[1]) * force[0]])

        for vector in magnitudes_and_force_vectors:
            resultant_force[0] += vector[0]
            resultant_force[1] += vector[1]

        self.forces = []
        return resultant_force

    def calculate_velocity_vector(self):
        total_force = self.calculate_total_forces()
        self.velocity[0] = self.velocity[0] / self.resistance
        self.velocity[1] = self.velocity[1] / self.resistance

        self.velocity[0] += total_force[0] / self.mass
        self.velocity[1] += total_force[1] / self.mass

    def apply_velocity(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def move_away_if_touching_walls(self):
        if self.position[0] - self.size < 0:
            self.velocity[0] += 50 / self.mass
        if self.position[1] - self.size < 0:
            self.velocity[1] += 50 / self.mass
        if self.position[0] + self.size > self.screensize[0]:
            self.velocity[0] -= 50 / self.mass
        if self.position[1] + self.size > self.screensize[1]:
            self.velocity[1] -= 50 / self.mass

    def take_turn(self):
        if self.been_infected_for > 2:
            self.infect_others()

        if self.infected:
            self.been_infected_for += 1

    def get_infected(self):
        if not self.infected:
            self.infected = True
            print("infected")

    def infect_others(self):
        if self.infected:
            for person in self.connected_to:
                if random.randint(0,1):
                    self.people.people_array[person].get_infected()

    def delete(self):
        self.connected_to = []
        self.infected = False
        self.been_infected_for = 0
        self.color = (0,0,0)
        self.size = 0.00000000000000000000000000000000000000000000000001
        self.selected = False
        self.velocity = [0,0]
        self.resistance = 1000
        self.mass = 0.000000000000000000000000000000001
        self.forces = []
        self.position = [0,0]
        self.deleted = True
        print("deleted")


class Connection:
    def __init__(self, _index, person1, person2, _connections, _people, _app):
        self.index = _index
        self.connections = _connections
        self.people = _people
        self.app = _app
        self.person1_index = person1
        self.person2_index = person2
        self.coords1 = self.people.get_coords_for_person(person1)
        self.coords2 = self.people.get_coords_for_person(person2)
        self.length_target = random.randint(200, 250)
        self.length = self.calculate_length()
        self.spring_constant = 0.02
        self.deleted = False

    def update(self):
        if not self.deleted:
            self.del_if_doesnt_exist()

            self.coords1 = self.people.get_coords_for_person(self.person1_index)
            self.coords2 = self.people.get_coords_for_person(self.person2_index)

            self.length = self.calculate_length()
            force = self.calculate_force()
            direction1, direction2 = self.calculate_force_direction()

            self.people.people_array[self.person1_index].add_force(force, direction1)
            self.people.people_array[self.person2_index].add_force(force, direction2)

    def draw(self):
        if not self.deleted:
            self.app.line(self.coords1[0], self.coords1[1], self.coords2[0], self.coords2[1])

    def calculate_length(self):
        return find_distance(self.coords1, self.coords2)

    def calculate_force(self):
        displacement = self.length - self.length_target
        # find_difference(self.length, self.length_target)
        force = -1 * self.spring_constant * displacement
        return force

    def calculate_force_direction(self):  # returns a tuple with two values, one for each person
        angle2 = find_angle_from_one_point_to_another(self.coords1, self.coords2)
        angle1 = find_angle_from_one_point_to_another(self.coords2, self.coords1)
        return angle1, angle2

    def check_if_still_exists(self):
        exists = True

        if not self.people.people_array[self.person1_index].connected_to.count(self.person2_index) or not  self.people.people_array[self.person2_index].connected_to.count(self.person1_index):
            exists = False


        return exists

    def del_if_doesnt_exist(self):
        if not self.check_if_still_exists():
            self.deleted = True


class Connections:
    def __init__(self, _people, _app):
        self.app = _app
        self.people = _people
        self.connections = []
        for first_person in range(len(self.people.people_array)):  # iterates through the people array, setting first person to the index
            for second_person in self.people.people_array[first_person].connected_to:  # iterates through the connections array of the first person
                self.connections.append(Connection(len(self.connections), first_person, second_person, self, self.people, self.app))  # appends a connection to the connections list
                self.people.people_array[second_person].connected_to.append(first_person)

    def update(self):
        for connection in self.connections:
            connection.update()

    def draw(self):
        for connection in self.connections:
            connection.draw()

   #

class People:
    def __init__(self, screensize, number_of_people, _app):
        self.app = _app
        self.clicked_left = False
        self.clicked_right = False
        self.person_selected = False
        self.people_array = [Person(screensize, [random.randint(0, screensize[0]), random.randint(0, screensize[1])], _app, self, i) for i in range(number_of_people)]  # fills the people array with people

        for person in self.people_array:
            person.connected_to = person.find_neighbours_in_approximate_distance(300,0)  # [i for i in [random.choice(self.people_array).index_in_people_array for i in range(random.choice([1,1,1,1,1,1,2,3,4]))] if not i == person.index_in_people_array]

    def update(self):  # calls the update function on all the people
        if mouse.is_pressed(button='left'):
            if not self.person_selected:
                self.clicked_left = True  # could try putting a K-D tree here soon

        if mouse.is_pressed(button='right'):
            self.clicked_right = True

        for i in range(len(self.people_array)):
            if not self.people_array[i].deleted:
                self.people_array[i].update(self.clicked_left, self.clicked_right)

        self.clicked_left = False
        self.clicked_right = False
    def draw(self):
        for person in self.people_array:
            person.draw()

    def take_turn(self):
        for person in self.people_array:
            person.take_turn()

    def get_coords_for_person(self, index):  # returns the coordinates for a person by index
        return self.people_array[index].position

    def infect(self):
        for person in self.people_array:
            person.infect_others()

    def infect_random_person(self):
        random.choice(self.people_array).get_infected()