from tkinter import *
import math
from PIL import Image, ImageTk
from urllib.request import urlopen

#converts from radians to degrees, returns the degree
def radians_to_degrees(rad):
    return (rad*180)/math.pi

#turns a 3d vector 2d
def squish_3d_to_2d(vector):
    return [vector[0] + vector[2]/2, 
            vector[1] + vector[2]/2]

#returns a rgb value in hexademical so it can be used by tkinter
def rgb(r,g,b):
    return '#%02x%02x%02x' % (r, g, b)

#takes in points (list of numbers with 2 elements in it) and returbs the rotated version of it.
def rotate_manevour(point, deg):
    deg = (deg * math.pi)/180
    return [(point[0]*math.cos(deg) - point[1]*math.sin(deg)), (point[0]*math.sin(deg) + point[1]*math.cos(deg))]

def do_nothing():
    pass
#to create the window for your application
class window:
    def __init__(self, title = "Super_G", width = 500, height = 500, colour = "black", start_position = [0,0]):
        self.root = Tk()
        
        self.title = title
        self.width = width
        self.height = height
        self.colour = colour
        self.start_position = start_position
        
        self.window = Canvas(self.root, bg = self.colour, width = self.root.winfo_screenwidth(), height = self.root.winfo_screenheight())
    #shows the user the application
    def display(self):
        self.root.title("{}".format(self.title))
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.start_position[0], self.start_position[1]))
        self.window.pack()
    #without this function your app will close instantly so chunk this at the end of your program
    def keep_running(self):
        self.root.mainloop()
    
    #destroys the program
    def erase(self):
        self.root.destroy()
    
    #hides the program
    def hide(self):
        self.root.quit()
    
    #returns the width of the device you are using
    def device_width(self):
        return self.root.winfo_screenwidth()
    
    #returns the device height
    def device_height(self):
        return self.root.winfo_screenheight()
    
    #used to create keyboard shortcuts, if user press a key on the keyboard then execute some function
    #note on using this: create a dummy parameter in the function you want to execute and don't mention it
    #check the __name__ == '__main__' for clarity
    def keyboard_trigger(self, trigger, function):
        self.root.bind("<{}>".format(trigger), function)

#used to create polygons on the screen, the points given are 2d polygons
class polygon:
    def __init__(self, window, points, colour = "", border_width = 1, border_colour = "white"):
        self.window = window
        self.points = points
        self.colour = colour
        self.border_width = border_width
        self.border_colour = border_colour
        
        self.polygon = None
    
    #used to both display and initilase the polygon and polygon variable
    def display(self):
        self.polygon = self.window.window.create_polygon(self.points, 
                                                        fill=self.colour, 
                                                        outline = self.border_colour, 
                                                        width=self.border_width)
    #hides the polygon from the window
    def erase(self):
        self.window.window.delete(self.polygon)
    
    #setsup up the polygon variable without displaying the polygon
    def initilise(self):
        polygon.display(self)
        polygon.erase(self)
    
    #updates the info regarding the polygon
    def update(self):
        polygon.erase(self)
        polygon.display(self)
    
    #moves the polygon some amount x in the x diretion and same thing for the y direction
    def move(self, x, y):
        i = 0

        while (i < len(self.points)):
            self.points[i][0] += x
            self.points[i][1] += y
            i+=1
        
        polygon.update(self)
    
    #returns the center of the polygon
    def center_coor(self):
        avg_x = 0
        avg_y = 0

        num_of_points = 0

        for point in self.points:
            avg_x += point[0]
            avg_y += point[1]

            num_of_points += 1
        
        return [avg_x/num_of_points, avg_y/num_of_points]

    #rotates the polygon by some degree, positive degree means clockwise rotation
    def rotate(self, degree):
        x = polygon.center_coor(self)[0]
        y = polygon.center_coor(self)[1]
        
        polygon.move(self, -1*x, -1*y)

        i = 0
        while (i < len(self.points)):
            self.points[i] = rotate_manevour(self.points[i], degree)
            i+=1
        
        polygon.move(self, x, y)

#used to create an oval
class oval:
    def __init__(self, window, points, colour = "", border_colour = "red", border_width = 1):
        self.window = window
        self.points = points
        self.colour = colour
        self.border_colour = border_colour
        self.border_width = border_width
        
        self.oval = None
    #displays and initiliases the oval and the oval variable
    def display(self):
        self.oval = self.window.window.create_oval(self.points, 
                                                    fill = self.colour, 
                                                    outline = self.border_colour, 
                                                    width = self.border_width)

    #removes the oval from the screen
    def erase(self):
        self.window.window.delete(self.oval)
    
    #updates the information regarding the oval, also includes the oval onto the screen
    def update(self):
        oval.erase(self)
        oval.display(self)
    
    #initiliases the oval but does not display it
    def initilise(self):
        oval.display(self)
        oval.erase(self)

    #moves the oval some amount x in the x direction and some amount y in the y direction
    def move(self, x, y):
        self.points[0][0] += x
        self.points[0][1] += y

        self.points[1][0] += x
        self.points[1][1] += y

        oval.update(self)

#used to display images on the device
#make sure that you can see the image using the photos app before trying this
class on_device_image:
    def __init__(self, window, x, y, link):
        self.window = window
        self.x = x
        self.y = y
        self.link = link
        
        self.load_image = ImageTk.PhotoImage(Image.open(self.link))
        self.image = Label(self.window.window, image = self.load_image)
    
    #displays the image onto the screen
    def display(self):
        self.image.place(x = self.x, y = self.y)
    
    #removes the image from the screen
    def erase(self):
        self.image.place_forget()

    #updates the data surrounding the image and display the image
    def update(self):
        on_device_image.erase(self)
        on_device_image.display(self)

    #moves the image some amount x in the x direction and some amount y in the y direction
    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        on_device_image.update(self)
    
    #resizes the image on the screen, note this acts weird
    def resize(self, new_width, new_height):
        self.load_image = Image.open(self.link).resize((new_width, new_height))
        self.load_image = ImageTk.PhotoImage(self.load_image)

        on_device_image.update(self)

    #rotates the image on the screen, note this acts weird
    def rotate(self,degree):
        self.load_image = ImageTk.PhotoImage(Image.open(self.link).rotate(degree))
        on_device_image.update(self)

#add some text onto the screen
class text:
    def __init__(self, window, text = "Text", x = 0, y = 0, colour = "black", text_colour = "white"):
        self.window = window
        self.text = text
        self.colour = colour
        self.text_colour = text_colour
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1
        self.font = "Arial"
        self.font_size = 12
        self.font_style = None

        self.text = Label(self.window.window, 
                        text = self.text, 
                        bg = self.colour, 
                        fg = self.text_colour)
    
    #displays the text onto the screen and also setsup the font for the text
    def display(self):
        if (self.font_style != None):
            self.text.config(font = (self.font, self.font_size, self.font_style))
        else:
            self.text.config(font = (self.font, self.font_size))

        self.text.place(x = self.x, y = self.y)
    
    #removes the text from the screen
    def erase(self):
        self.text.place_forget()
    
    #updates the information surrounding the text and displays the text onto the screen
    def update(self):
        text.erase(self)
        text.display(self)
    
    #moves the text some amount x in the x direction and same thing with the y direction
    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        text.update(self)

#creates a button
class button:
    def __init__(self, window, x, y, text= "Button", function = do_nothing, colour = "black", text_colour = "white"):
        self.window = window
        self.x = x
        self.y = y
        self.text = text
        self.function = function
        self.colour = colour
        self.text_colour = text_colour
        self.font = "Arial"
        self.font_size = 12
        self.font_style = None

        self.button = Button(self.window.window, 
                            text = self.text,
                            bg = self.colour,
                            fg = self.text_colour,
                            command = self.function)
    
    def display(self):
        if (self.font_style != None):
            self.button.config(font = (self.font, self.font_size, self.font_style))
        
        else:
            self.button.config(font = (self.font, self.font_size))

        self.button.place(x = self.x, y = self.y)
    
    def erase(self):
        self.button.place_forget()
    
    def update(self):
        button.erase(self)
        button.display(self)
    
    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        button.update(self)

#cannot resize or rotate online images, yet
#used to display online images onto the window
class online_image:
    def __init__(self, window, x, y, link):
        self.window = window
        self.x = x
        self.y = y
        self.link = link

        self.load_image = ImageTk.PhotoImage(data = urlopen(self.link).read())
        self.image = Label(self.window.window, image = self.load_image)
    
    #displays the web image
    def display(self):
        self.image.place(x = self.x, y = self.y)

    #removes the web image from the window
    def erase(self):
        self.image.place_forget()

    #updates the information regarding the image
    def update(self):
        online_image.erase(self)
        online_image.display(self)
    
    #moves the image
    def move(self, move_x,  move_y):
        self.x += move_x
        self.y += move_y

        online_image.update(self)

#used to display 2d shapes in 3d shapes and map it back onto the 2d window
#future moduels to add: depth perception, spin_xy, spin_yz, spin_xz
class poly_in_3d:
    def __init__(self, window, points, colour = "", border_colour = "white", border_width = 1):
        self.window = window
        self.points = points
        self.colour = colour
        self.border_colour = border_colour
        self.border_width = border_width

        self.usable_points = []
        self.polygon = None

    def display(self):

        self.usable_points = []

        for x in self.points:
            self.usable_points.append(squish_3d_to_2d(x))
        
        self.polygon = polygon(self.window, 
                                self.usable_points, 
                                colour = self.colour, 
                                border_colour = self.border_colour, 
                                border_width = self.border_width)
        
        self.polygon.display()

    def erase(self):
        self.polygon.erase()
    
    def update(self):
        poly_in_3d.erase(self)
        poly_in_3d.display(self)
    
    #returns the coordinates of the center point of the polygon
    def center_coor(self):
        x = 0
        y = 0
        z = 0
        length = 0
        
        for j in self.points:
            x += j[0]
            y += j[1]
            z += j[2]
            length += 1
        
        return [x/length, y/length, z/length]

    
    def move(self, x, y, z):
        for i in range(0, len(self.points)):
            self.points[i][0] += x
            self.points[i][1] += y
            self.points[i][2] += z
        
        poly_in_3d.update(self)
    
    #there are 3 rotate functions which rotate the polygon around the point (0,0,0) in the plane that is in their name
    #experiment with these funcitons inorder to find out how they work better
    def rotate_xy(self, degree):
        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][0], self.points[i][1]], degree)
            point.append(self.points[i][2])

            self.points[i] = point
        
        poly_in_3d.update(self)
    
    def rotate_yz(self, degree):
        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][1], self.points[i][2]], degree)
            self.points[i] = [self.points[i][0], point[0], point[1]]
        
        poly_in_3d.update(self)
    
    def rotate_xz(self, degree):
        for i in range(0, len(self.points)):
            point  = rotate_manevour([self.points[i][0], self.points[i][2]], degree)
            self.points[i] = [point[0], self.points[i][1], point[1]]
        
        poly_in_3d.update(self)


if __name__ == '__main__':
    main_window = window("Testing")
    main_window.display()

    square = polygon(main_window, [[50,50],[100, 50],[100,100], [50, 100]])
    square.colour = "red"
    square.display()
    
    rhombus = square
    rhombus.colour = "green"
    rhombus.initilise()

    rhombus.move(100,0)

    txt = text(main_window, text = "Hello", x = 100, y = 200)
    txt.move(100,100)

    butt = button(main_window, x = 200, y = 200, function = lambda: rhombus.rotate(10))
    butt.display()
    butt.move(-90, -100)

    #web_img = online_image(main_window, x = 300, y = 200, link = "https://upload.wikimedia.org/wikipedia/commons/a/a0/Bill_Gates_2018.jpg")
    #web_img.display()
    #web_img.move(100, 0)

    cube = [
        poly_in_3d(main_window, [[300, 300, 0], [300, 400, 0], [400, 400, 0], [400, 300, 0]], colour = 'white'), #back
        poly_in_3d(main_window, [[300, 400, 0],[400, 400, 0],[400, 400, 100],[300, 400, 100]], colour = 'green'), #bottom
        poly_in_3d(main_window, [[300, 300, 0], [300, 400, 0], [300, 400, 100], [300, 300, 100]], colour = 'purple'), #left
        poly_in_3d(main_window, [[400, 300, 0], [400, 400, 0], [400, 400, 100], [400, 300, 100]], colour = 'cyan'), #right
        poly_in_3d(main_window, [[300, 300, 0], [400, 300, 0], [400, 300, 100], [300, 300, 100]], colour = 'orange'), #top
        poly_in_3d(main_window, [[300, 300, 100], [300, 400, 100], [400, 400, 100], [400, 300, 100]], colour = 'red') #front
        ]
    
    for x in cube:
        x.display()
    
    def right(p):
        for x in cube:
            x.move(10,0,0)
    
    def left(p):
        for x in cube:
            x.move(-10,0,0)
    def up(p):
        for x in cube:
            x.move(0, -10, 0)
    
    def down(p):
        for x in cube:
            x.move(0, 10, 0)
    
    def turn_right(p):
        for x in cube:
            x.rotate_xz(1)
    
    def turn_left(p):
        for x in cube:
            x.rotate_xz(-1)
    

    
    main_window.keyboard_trigger("d", right)
    main_window.keyboard_trigger("a",left)
    main_window.keyboard_trigger("Right", turn_right)
    main_window.keyboard_trigger("Left", turn_left)
    main_window.keyboard_trigger("w", up)
    main_window.keyboard_trigger('s', down)

    main_window.keep_running()
