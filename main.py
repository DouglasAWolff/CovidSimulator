import processing_py
import classes

screensize = [600,400]
app = processing_py.App(600, 400)  # create window: width, height
people = classes.People(screensize, 20, app)

while (True):
    app.background(255, 255, 255)  # set background:  red, green, blue
    people.update()

    app.redraw()  # refresh the window
