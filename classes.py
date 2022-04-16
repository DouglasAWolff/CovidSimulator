import random
import math


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
        self.velocity = [0,0]
        self.selected = False
        self.size = 30 + (5 * len(self.connected_to))
        self.color = (150, 150 + (10 * len(self.connected_to)), 150 + (10 * len(self.connected_to)))
        self.screensize = screensize

    def update(self):
        self.calculate_velocity_vector()
        self.move_away_if_touching_walls()
        self.apply_velocity()


        self.size = 30 + (5 * len(self.connected_to))

        self.app.fill(150, 150 + (10 * len(self.connected_to)), 150 + (10 * len(self.connected_to)))  # fills in the circle
        self.app.ellipse(self.position[0], self.position[1], self.size, self.size)  # draws a circle at the position of the person


    def find_neighbours_in_approximate_distance(self, distance,
                                                plusminus):  # takes in a number and then spits out that number of closest neighbours
        people_distances = []
        for _person in self.people.people_array:
            people_distances.append([find_distance(self.position, _person.position), _person.index_in_people_array])
        people_distances.sort()

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
        if self.position[1]  - self.size < 0:
            self.velocity[1] += 50 / self.mass
        if self.position[0] + self.size > self.screensize[0]:
            self.velocity[0] -= 50 / self.mass
        if self.position[1] + self.size > self.screensize[1]:
            self.velocity[1] -= 50 / self.mass

                # def infect(self):


class Connection:
    def __init__(self, person1, person2, _people, _app):
        self.people = _people
        self.app = _app
        self.person1_index = person1
        self.person2_index = person2
        self.coords1 = self.people.get_coords_for_person(person1)
        self.coords2 = self.people.get_coords_for_person(person2)
        self.length_target = random.randint(200,250)
        self.length = self.calculate_length()
        self.spring_constant = 0.08

    def update(self):
        self.coords1 = self.people.get_coords_for_person(self.person1_index)
        self.coords2 = self.people.get_coords_for_person(self.person2_index)

        self.length = self.calculate_length()
        force = self.calculate_force()
        direction1, direction2 = self.calculate_force_direction()

        self.people.people_array[self.person1_index].add_force(force, direction1)
        self.people.people_array[self.person2_index].add_force(force, direction2)

        self.coords1 = self.people.get_coords_for_person(self.person1_index)
        self.coords2 = self.people.get_coords_for_person(self.person2_index)

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
        return (angle1, angle2)


class Connections:
    def __init__(self, _people, _app):
        self.app = _app
        self.people = _people
        self.connections = []
        for first_person in range(len(self.people.people_array)):  # iterates through the people array, setting first person to the index
            print(first_person)
            for second_person in self.people.people_array[first_person].connected_to:  # iterates through the connections array of the first person
                print(second_person)
                self.connections.append(Connection(first_person, second_person, self.people, self.app))  # appends a connection to the connections list

    def update(self):

        for connection in self.connections:
            connection.update()

    def is_connection_crossing_another(self, first_person, second_person):  # might not need this
        pass


class People:
    def __init__(self, screensize, number_of_people, _app):
        self.people_array = [
            Person(screensize, [random.randint(0, screensize[0]), random.randint(0, screensize[1])], _app, self, i) for i in range(number_of_people)]  # fills the people array with people

        for person in self.people_array:
            person.connected_to =  person.find_neighbours_in_approximate_distance(250,50)    #[i for i in [random.choice(self.people_array).index_in_people_array for i in range(random.choice([1,1,1,1,1,1,2,3,4]))] if not i == person.index_in_people_array]

    def update(self):  # calls the update function on all the people
        for i in range(len(self.people_array)):
            self.people_array[i].update()

    def get_coords_for_person(self, index):  # returns the coordinates for a person by index
        return self.people_array[index].position
