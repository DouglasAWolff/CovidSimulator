import processing_py
import classes
import time

screensize = [1800,1000]
app = processing_py.App(screensize[0],screensize[1])  # create window: width, height
people = classes.People(screensize, 200, app)


people.infect_random_person()

turn_timer = time.time() + 300000

while True:
    if time.time() - turn_timer > 1:
        people.take_turn()
        turn_timer = time.time()
        print(f"turn,   {time.time()}")

    app.background(255, 255, 255)  # set background:  red, green, blue

    people.update()


    people.draw()

    app.redraw()  # refresh the window
