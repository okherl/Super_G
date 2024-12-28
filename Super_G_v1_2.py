#Version 1_2
#Created by Aryan Pokhrel
#Uploaded on 28/Dec/2024

#EDIT on the 29/DEC/2024: there was a bug with the fps and timer function for the window class which i fixed

from tkinter import *
import math, time
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

        self.window = Canvas(self.root, bg = self.colour, highlightthickness = 0)        

        self.Super_G_version = "Version 1_2"

    #shows the user the application
    def display(self):
        self.root.title("{}".format(self.title))
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.start_position[0], self.start_position[1]))
        
        self.window.pack(side = LEFT, fill = BOTH, expand = 1)
    
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
    
    #waits for a few seconds to execute some function
    def timer(self, seconds, function):
        self.root.after(int(1000*seconds), function)
    
    #a single frame in this instance being one execution of the function
    #repeats a single function fps amount of times in a second
    def fps(self, fps, function):
        self.root.after(int(1000/fps), function)

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
class poly3d:
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
        poly3d.erase(self)
        poly3d.display(self)
    
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
        
        poly3d.update(self)
    
    #there are 3 spin functions which spins the shape in the plane that is in their name
    def spin_xy(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        poly3d.move(self, (-1*x), (-1*y), (-1*z))

        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][0], self.points[i][1]], degree)
            point.append(self.points[i][2])

            self.points[i] = point
        
        poly3d.move(self, x, y, z)

        poly3d.update(self)
    
    def spin_yz(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        poly3d.move(self, (-1*x), (-1*y), (-1*z))

        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][1], self.points[i][2]], degree)
            self.points[i] = [self.points[i][0], point[0], point[1]]
        
        poly3d.move(self, x, y, z)

        poly3d.update(self)
    
    def spin_xz(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        poly3d.move(self, (-1*x), (-1*y), (-1*z))

        for i in range(0, len(self.points)):
            point  = rotate_manevour([self.points[i][0], self.points[i][2]], degree)
            self.points[i] = [point[0], self.points[i][1], point[1]]
        
        poly3d.move(self, x, y, z)

        poly3d.update(self)
    #the rotate functions rotate the shape around a axis that is in their name
    def rotate_z(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][0], self.points[i][1]], degree)
            point.append(self.points[i][2])

            self.points[i] = point
        

        poly3d.update(self)
    
    def rotate_x(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        for i in range(0, len(self.points)):
            point = rotate_manevour([self.points[i][1], self.points[i][2]], degree)
            self.points[i] = [self.points[i][0], point[0], point[1]]

        poly3d.update(self)
    
    def rotate_y(self, degree):
        x = poly3d.center_coor(self)[0]
        y = poly3d.center_coor(self)[1]
        z = poly3d.center_coor(self)[2]

        for i in range(0, len(self.points)):
            point  = rotate_manevour([self.points[i][0], self.points[i][2]], degree)
            self.points[i] = [point[0], self.points[i][1], point[1]]

        poly3d.update(self)

#creates an entry, essentially a one-line text box
class entry:
    def __init__(self, window, x, y, width = 144, colour = "black", text_colour = "white"):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.font = "Arial"
        self.font_size = 12
        self.font_style = None
        self.colour = colour
        self.text_colour = text_colour

        self.horizontal_scrollbar = Scrollbar(self.window.root, orient = 'horizontal')
        self.horizontal_scrollbar_x = self.x
        self.horizontal_scrollbar_thickness = self.font_size
        self.horizontal_scrollbar_y = self.y + self.horizontal_scrollbar_thickness

        self.entry = Entry(self.window.root, bg = self.colour, fg = self.text_colour, 
                            width = self.width, xscrollcommand = self.horizontal_scrollbar.set)
        
        self.horizontal_scrollbar.config(command = self.entry.xview)
    
    def display(self):
        if self.font_style != None:
            self.entry.config(font = (self.font, self.font_size, self.font_style))
        
        else:
            self.entry.config(font = (self.font, self.font_size))

        self.entry.place(x = self.x, y = self.y, width = self.width)
    
    def erase(self):
        self.entry.place_forget()
    
    def user_input(self):
        return self.entry.get()
    
    def clear(self):
        self.entry.delete(0, 'end')
    
    def insert_text(self, text):
        self.entry.insert(0, text)
    
    def display_horizontal_scrollbar(self):
        self.horizontal_scrollbar_x = self.x
        self.horizontal_scrollbar_y = self.y + self.font_size

        self.horizontal_scrollbar.place(x = self.horizontal_scrollbar_x, 
                                        y = self.horizontal_scrollbar_y, 
                                        height = self.horizontal_scrollbar_thickness,
                                        width = self.width)
    
    def erase_horizontal_scrollbar(self):
        self.horizontal_scrollbar.place_forget()
    
    def update(self):
        entry.erase(self)
        entry.display(self)

        entry.erase_horizontal_scrollbar(self)
        entry.display_horizontal_scrollbar(self)
    
    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        entry.update(self)


#used to create a 3d shape, it is made from a list of poly3d objects
class shape3d:
    def __init__(self, polygon_list):
        self.polygon_list = polygon_list
    
    def display(self):
        for x in self.polygon_list:
            x.display()
    
    def erase(self):
        for x in self.polygon_list:
            x.erase()
    
    def update(self):
        for x in self.polygon_list:
            x.erase()
            x.display()
    
    def move(self, x, y, z):
        for i in self.polygon_list:
            for j in i.points:
                j[0] += x
                j[1] += y
                j[2] += z
        
        shape3d.update(self)
    
    def center_coor(self):
        x = 0
        y = 0
        z = 0

        num_of_points = 0

        for i in self.polygon_list:
            for j in i.points:
                x += j[0]
                y += j[1]
                z += j[2]

                num_of_points += 1
        
        return [x/num_of_points, y/num_of_points, z/num_of_points]

    def rotate_x(self, degree):
        for x in self.polygon_list:
            x.rotate_x(degree)
    
    def rotate_y(self, degree):
        for x in self.polygon_list:
            x.rotate_y(degree)
    
    def rotate_z(self, degree):
        for x in self.polygon_list:
            x.rotate_z(degree)
    
    def spin_xy(self, degree):
        x = shape3d.center_coor(self)[0]
        y = shape3d.center_coor(self)[1]
        z = shape3d.center_coor(self)[2]

        shape3d.move(self, -1*x, -1*y, -1*z)

        for i in self.polygon_list:
            for j in range(0, len(i.points)):
                uneffected = i.points[j][2]
                point = rotate_manevour([i.points[j][0], i.points[j][1]], degree)
                point.append(uneffected)
                i.points[j] = point

        shape3d.move(self, x, y, z)
    
    def spin_yz(self, degree):
        x = shape3d.center_coor(self)[0]
        y = shape3d.center_coor(self)[1]
        z = shape3d.center_coor(self)[2]

        shape3d.move(self, -1*x, -1*y, -1*z)

        for i in self.polygon_list:
            for j in range(0, len(i.points)):
                uneffected = i.points[j][0]
                point = rotate_manevour([i.points[j][1], i.points[j][2]], degree)
                                
                i.points[j] = [uneffected, point[0], point[1]]

        shape3d.move(self, x, y, z)
    
    def spin_xz(self, degree):
        x = shape3d.center_coor(self)[0]
        y = shape3d.center_coor(self)[1]
        z = shape3d.center_coor(self)[2]

        shape3d.move(self, -1*x, -1*y, -1*z)

        for i in self.polygon_list:
            for j in range(0, len(i.points)):
                uneffected = i.points[j][1]
                point = rotate_manevour([i.points[j][0], i.points[j][2]], degree)
                                
                i.points[j] = [point[0], uneffected, point[1]]

        shape3d.move(self, x, y, z)

#used to create a textbox
class textbox:
    def __init__(self, window, x, y, height = 100, width = 162, colour = 'white', text_colour = 'black'):
        self.window = window
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.text_colour = text_colour
        self.font = "Arial"
        self.font_size = 12
        self.font_style = None

        self.vertical_scrollbar = Scrollbar(self.window.root, orient = 'vertical')

        self.textbox = Text(self.window.root, 
                            bg = self.colour, fg = self.text_colour,
                            yscrollcommand = self.vertical_scrollbar.set)
        
        self.vertical_scrollbar.config(command = self.textbox.yview)

        self.vertical_scrollbar_x = self.x + self.width
        self.vertical_scrollbar_y = self.y
        self.vertical_scrollbar_thickness = self.font_size
    
    def display(self):
        if self.font_style == None:
            self.textbox.config(font = (self.font, self.font_size))
        else:
            self.textbox.config(font = (self.font, self.font_size, self.font_style))

        self.textbox.place(x = self.x, y = self.y, height = self.height, width = self.width)
    
    def erase(self):
        self.textbox.place_forget()
    
    #returns what the user has written in the textbox
    def user_input(self):
        return self.textbox.get("1.0", "end-1c")
    
    #inserts some text onto the textbox
    def insert_text(self, text):
        self.textbox.insert(END, text)

    #clears user input from the textbox
    def clear(self):
        self.textbox.delete('1.0', END)
    
    def display_vertical_scrollbar(self):
        self.vertical_scrollbar_x = self.x + self.width
        self.vertical_scrollbar_y = self.y

        self.vertical_scrollbar.place(x = self.vertical_scrollbar_x,
                                    y = self.vertical_scrollbar_y, 
                                    height = self.height,
                                    width = self.vertical_scrollbar_thickness)
    
    def erase_vertical_scrollbar(self):
        self.vertical_scrollbar.place_forget()
    

    def update(self):
        textbox.erase(self)
        textbox.display(self)

        textbox.erase_vertical_scrollbar(self)
        textbox.display_vertical_scrollbar(self)
    
    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        textbox.update(self)


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
        poly3d(main_window, [[300, 300, 0], [300, 400, 0], [400, 400, 0], [400, 300, 0]], colour = 'white'), #back
        poly3d(main_window, [[300, 400, 0],[400, 400, 0],[400, 400, 100],[300, 400, 100]], colour = 'green'), #bottom
        poly3d(main_window, [[300, 300, 0], [300, 400, 0], [300, 400, 100], [300, 300, 100]], colour = 'purple'), #left
        poly3d(main_window, [[400, 300, 0], [400, 400, 0], [400, 400, 100], [400, 300, 100]], colour = 'black'), #right
        poly3d(main_window, [[300, 300, 0], [400, 300, 0], [400, 300, 100], [300, 300, 100]], colour = 'orange'), #top
        poly3d(main_window, [[300, 300, 100], [300, 400, 100], [400, 400, 100], [400, 300, 100]], colour = 'red') #front
        ]

    for x in cube:
        x.border_colour = ''

    super_cube = shape3d(cube)
    super_cube.display()

    square3d = poly3d(main_window, [[100, 300, 0], [100, 400, 0], [200, 400, 0], [200, 300, 0]], colour = 'white')
    square3d.display()
    
    super_entry = entry(main_window, x = 150, y = 150)
    super_entry.display()
    super_entry.display_horizontal_scrollbar()

    super_textbox = textbox(main_window, x = 20, y = 20, height = 50)
    super_textbox.display()
    super_textbox.display_vertical_scrollbar()

    def super_spin(p):
        super_cube.spin_xy(2)
        #super_cube.spin_xz(-2)
        super_cube.spin_yz(2)
        super_cube.move(0, 0, -2)

    main_window.keyboard_trigger("Right", lambda p: super_cube.move(10, 0, 0))
    main_window.keyboard_trigger("Left", lambda p: super_cube.move(-10, 0, 0))
    main_window.keyboard_trigger("Up", lambda p: super_cube.move(0, -10, 0))
    main_window.keyboard_trigger("Down", lambda p: super_cube.move(0, 10, 0))
    main_window.keyboard_trigger("d", lambda p: super_cube.spin_xy(1))
    main_window.keyboard_trigger("a", lambda p: super_cube.spin_xy(-1))
    main_window.keyboard_trigger('p', super_spin)


    main_window.keep_running()
