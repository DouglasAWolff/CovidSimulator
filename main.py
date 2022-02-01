import processing_py
import classes

screensize = [600,400]
app = processing_py.App(600, 400)  # create window: width, height
person = classes.Person([1, 2, 3, 4, 5], screensize, app)

while (True):
    app.background(255, 255, 255)  # set background:  red, green, blue
    person.update()

    app.redraw()  # refresh the window
