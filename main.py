import processing_py
import classes

screensize = [1200,800]
app = processing_py.App(screensize[0],screensize[1])  # create window: width, height
people = classes.People(screensize, 10, app)
connections = classes.Connections(people, app)

while (True):
    app.background(255, 255, 255)  # set background:  red, green, blue

    connections.update()
    people.update()
    app.redraw()  # refresh the window
