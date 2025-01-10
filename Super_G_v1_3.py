#Version 1_3
#Created by Aryan Pokhrel
#Uploaded on 10/Jan/2025

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

#since the max function doesn't seem to work for negatives or 0s i have to create my own function :(
def maximum(da_list):
    if len(da_list) > 0:
        max_ = da_list[0]

        for i in range(0, len(da_list)):
            if da_list[i] > max_:
                max_ = da_list[i]
    
        return max_
    
    else:
        return da_list

def minimum(da_list):
    if len(da_list) > 0:
        min_ = da_list[0]

        for i in range(0, len(da_list)):
            if da_list[i] < min_:
                min_ = da_list[i]
    
        return min_
    
    else:
        return da_list

#returns the average of 2 numbers
def avg2(num1, num2):
    return (num1 + num2)/2

#returns a list of length n containing many copies of copy_[0] given that copy_ has only one element
def copy_n_times_if_len_1(copy_, n):
    if len(copy_) == 1:
        return_list = []

        for i in range(0, n):
            return_list.append(copy_[0])
        
        return return_list
    
    else:
        return copy_

#used to define a 3d shape given that you have the list of points, colours, border colour, and border width
def make_polygon_list(window_, points_, colours_, border_colour_, border_width_):
    return_list = []

    colours_ = copy_n_times_if_len_1(colours_, len(points_))
    border_colour_ = copy_n_times_if_len_1(border_colour_, len(points_))
    border_width_ = copy_n_times_if_len_1(border_width_, len(points_)) 

    for i in range(0, len(points_)):
        return_list.append(poly3d(window_, points_[i], colours_[i], border_colour_[i], border_width_[i]))
    
    return return_list

#used to keep track of what the maximum z-value is in a shape and how many times it pops up along with its index
class top_left_front:
    def __init__(self, index, shape, low, high):
        self.index = index
        cc = shape.center_coor()

        top_coor = [avg2(low[0], high[0]), low[1], avg2(low[2], high[2])]
        left_coor = [low[0], avg2(low[1], high[1]), avg2(low[2], high[2])]
        front_coor = [avg2(low[0], high[0]), avg2(low[1], high[1]), high[2]]

        distance_top = math.sqrt((top_coor[0] - cc[0])**2 + (top_coor[1] - cc[1])**2 + (top_coor[2] - cc[2])**2)
        distance_left = math.sqrt((left_coor[0] - cc[0])**2 + (left_coor[1] - cc[1])**2 + (left_coor[2] - cc[2])**2)
        distance_front = math.sqrt((front_coor[0] - cc[0])**2 + (front_coor[1] - cc[1])**2 + (front_coor[2] - cc[2])**2)

        self.id = minimum([distance_top, distance_left, distance_front])

#returns the id to a top_left_front object, used for the sort_polygon_list function
def return_id(record):
    return record.id

#sorts the polygon_list so that the top-most, left-most, and front-most shapes appear first so that the shape looks and behaves normally.
def sort_polygon_list(polygon_list):
    return_list = []
    max_list_length = len(polygon_list)

    x_coor = []
    y_coor = []
    z_coor = []

    for shape in polygon_list:
        for points in shape.points:
            x_coor.append(points[0])
            y_coor.append(points[1])
            z_coor.append(points[2])
    
    low = [minimum(x_coor), minimum(y_coor), minimum(z_coor)]
    high = [maximum(x_coor), maximum(y_coor), maximum(z_coor)]

    projection_cube_list = []

    for i in range(0, max_list_length):
        projection_cube_list.append(top_left_front(i, polygon_list[i], low, high))
    
    projection_cube_list = sorted(projection_cube_list, reverse = True, key = return_id)
    
    for j in range(0, max_list_length):
        return_list.append(polygon_list[projection_cube_list[j].index])

    return return_list
                

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
        self.displayed = False
    
    #used to both display and initilase the polygon and polygon variable
    def display(self):
        self.polygon = self.window.window.create_polygon(self.points, 
                                                        fill=self.colour, 
                                                        outline = self.border_colour, 
                                                        width=self.border_width)
        self.displayed = True
    #hides the polygon from the window
    def erase(self):
        self.window.window.delete(self.polygon)
        self.displayed = False
    
    #updates the info regarding the polygon
    def update(self):
        if self.displayed == True:
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
        
        self.displayed = False

    #displays and initiliases the oval and the oval variable
    def display(self):
        self.oval = self.window.window.create_oval(self.points, 
                                                    fill = self.colour, 
                                                    outline = self.border_colour, 
                                                    width = self.border_width)

        self.displayed = True

    #removes the oval from the screen
    def erase(self):
        self.window.window.delete(self.oval)
        self.displayed = False

    #updates the information regarding the oval, also includes the oval onto the screen
    def update(self):
        if self.displayed == True:
            oval.erase(self)
            oval.display(self)

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

        self.displayed = False

    #displays the image onto the screen
    def display(self):
        self.image.place(x = self.x, y = self.y)
        self.displayed = True
    
    #removes the image from the screen
    def erase(self):
        self.image.place_forget()
        self.displayed = False

    #updates the data surrounding the image and display the image
    def update(self):
        if self.displayed == True:
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
        
        self.displayed = False
    
    #displays the text onto the screen and also setsup the font for the text
    def display(self):
        if (self.font_style != None):
            self.text.config(font = (self.font, self.font_size, self.font_style))
        else:
            self.text.config(font = (self.font, self.font_size))

        self.text.place(x = self.x, y = self.y)

        self.displayed = True
    
    #removes the text from the screen
    def erase(self):
        self.text.place_forget()
        self.displayed = False
    
    #updates the information surrounding the text and displays the text onto the screen
    def update(self):
        if self.displayed == True:
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
        
        self.displayed = False
    
    def display(self):
        if (self.font_style != None):
            self.button.config(font = (self.font, self.font_size, self.font_style))
        
        else:
            self.button.config(font = (self.font, self.font_size))

        self.button.place(x = self.x, y = self.y)

        self.displayed = True
    
    def erase(self):
        self.button.place_forget()
        self.displayed = False
    
    def update(self):
        if self.displayed == True:
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

        self.displayed = False
    
    #displays the web image
    def display(self):
        self.image.place(x = self.x, y = self.y)
        self.displayed = True

    #removes the web image from the window
    def erase(self):
        self.image.place_forget()
        self.displayed = False

    #updates the information regarding the image
    def update(self):
        if self.displayed == True:
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

        self.displayed = False

        self.id = id

    def display(self):
        self.usable_points = []

        for x in self.points:
            self.usable_points.append(squish_3d_to_2d(x))
        
        self.polygon = polygon(self.window, 
                                self.usable_points, 
                                colour = self.colour, 
                                border_colour = self.border_colour, 
                                border_width = self.border_width)
        
        self.displayed = True
        
        self.polygon.display()

    def erase(self):
        self.polygon.erase()
        self.displayed = False
    
    def update(self):
        if self.displayed == True:
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

        self.displayed, self.horizontal_scrollbar_displayed = False, False
    
    def display(self):
        if self.font_style != None:
            self.entry.config(font = (self.font, self.font_size, self.font_style))
        
        else:
            self.entry.config(font = (self.font, self.font_size))

        self.entry.place(x = self.x, y = self.y, width = self.width)

        self.displayed = True
    
    def erase(self):
        self.entry.place_forget()
        self.displayed = False
    
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
        
        self.horizontal_scrollbar_displayed = True
    
    def erase_horizontal_scrollbar(self):
        self.horizontal_scrollbar.place_forget()
        self.horizontal_scrollbar_displayed = False
    
    def update(self):
        if self.displayed == True:
            entry.erase(self)
            entry.display(self)

        if self.horizontal_scrollbar_displayed == True:
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

        self.displayed = False
    
    def display(self):
        self.polygon_list = sort_polygon_list(self.polygon_list)

        for x in self.polygon_list:
            x.display()

        self.displayed = True

    def erase(self):
        for x in self.polygon_list:
            x.erase()

        self.displayed = False
    
    def update(self):
        if self.displayed == True:
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
        
        self.polygon_list = sort_polygon_list(self.polygon_list)

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
        
        self.polygon_list = sort_polygon_list(self.polygon_list)

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
        
        self.polygon_list = sort_polygon_list(self.polygon_list)

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
        
        self.displayed = False
        
        self.vertical_scrollbar.config(command = self.textbox.yview)

        self.vertical_scrollbar_x = self.x + self.width
        self.vertical_scrollbar_y = self.y
        self.vertical_scrollbar_thickness = self.font_size

        self.vertical_scrollbar_displayed = False
    
    def display(self):
        if self.font_style == None:
            self.textbox.config(font = (self.font, self.font_size))
        else:
            self.textbox.config(font = (self.font, self.font_size, self.font_style))

        self.textbox.place(x = self.x, y = self.y, height = self.height, width = self.width)

        self.vertical_scrollbar_displayed = True
    
    def erase(self):
        self.textbox.place_forget()
        self.displayed = False
    
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
        
        self.vertical_scrollbar_displayed = True
    
    def erase_vertical_scrollbar(self):
        self.vertical_scrollbar.place_forget()
        self.vertical_scrollbar_displayed = False

    def update(self):
        if self.displayed == True:
            textbox.erase(self)
            textbox.display(self)

        if self.vertical_scrollbar_displayed == True:
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

    rhombus.move(100,0)

    txt = text(main_window, text = "Hello", x = 100, y = 200)
    txt.move(100,100)

    butt = button(main_window, x = 200, y = 200, function = lambda: rhombus.rotate(10))
    butt.display()
    butt.move(-90, -100)

    #web_img = online_image(main_window, x = 300, y = 200, link = "https://upload.wikimedia.org/wikipedia/commons/a/a0/Bill_Gates_2018.jpg")
    #web_img.display()
    #web_img.move(100, 0)

    square3d = poly3d(main_window, [[100, 300, 0], [100, 400, 0], [200, 400, 0], [200, 300, 0]], colour = 'white')
    square3d.display()
    
    super_entry = entry(main_window, x = 150, y = 150)
    super_entry.display()
    super_entry.display_horizontal_scrollbar()

    super_textbox = textbox(main_window, x = 20, y = 20, height = 50)
    super_textbox.display()
    super_textbox.display_vertical_scrollbar()

    #cube
    cube = [
        poly3d(main_window, [[300, 300, 0], [300, 400, 0], [400, 400, 0], [400, 300, 0]], colour = 'white'), #back
        poly3d(main_window, [[300, 400, 0],[400, 400, 0],[400, 400, 100],[300, 400, 100]], colour = 'green'), #bottom
        poly3d(main_window, [[300, 300, 0], [300, 400, 0], [300, 400, 100], [300, 300, 100]], colour = 'purple'), #left
        poly3d(main_window, [[400, 300, 0], [400, 400, 0], [400, 400, 100], [400, 300, 100]], colour = 'yellow'), #right
        poly3d(main_window, [[300, 300, 0], [400, 300, 0], [400, 300, 100], [300, 300, 100]], colour = 'orange'), #top
        poly3d(main_window, [[300, 300, 100], [300, 400, 100], [400, 400, 100], [400, 300, 100]], colour = 'red') #front
        ]
    
    super_cube = shape3d(cube)
    super_cube.display()

    #pyramid
    pyramid_points = [
        [[200, 200, 0],[100, 300, 0],[200, 300, 0]],
        [[200, 200, 0],[200, 200, 100],[100, 300, 0]],
        [[100, 300, 0],[200, 200, 100],[200, 300, 0]],
        [[200, 300, 0],[200, 200, 100],[200, 200, 0]]
    ]

    pyramid_colour = ["red", 'green', 'white', 'yellow']

    pyramid = shape3d(make_polygon_list(main_window, pyramid_points, pyramid_colour, ['black'], [1]))
    pyramid.move(220, -100, 0)
    pyramid.display()

    def super_spin(p):
        super_cube.spin_yz(5)
        pyramid.spin_yz(5)

    main_window.keyboard_trigger("Right", lambda p: super_cube.move(10, 0, 0))
    main_window.keyboard_trigger("Left", lambda p: super_cube.move(-10, 0, 0))
    main_window.keyboard_trigger("Up", lambda p: super_cube.move(0, -10, 0))
    main_window.keyboard_trigger("Down", lambda p: super_cube.move(0, 10, 0))
    main_window.keyboard_trigger('p', super_spin)
    
    main_window.keep_running()