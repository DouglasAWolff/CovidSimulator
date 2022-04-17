import processing_py
import classes
import mouse

screensize = [1800,1000]
app = processing_py.App(screensize[0],screensize[1])  # create window: width, height
people = classes.People(screensize, 40, app)
connections = classes.Connections(people, app)


while True:
    app.background(255, 255, 255)  # set background:  red, green, blue


    people.update()
    connections.update()
    connections.draw()
    people.draw()

    app.redraw()  # refresh the window
