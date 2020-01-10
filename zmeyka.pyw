
import Tkinter as Tk
import random

number_of_snakes = 2
time_step = 200
brick_size = 18
canvas_color = 'white'
outline_color = '#445566'
border_color = 'grey'
border_outline_color = 'black'
alert_color = '#cc0000'
canvas_width = 42
canvas_height = 20
snake_colors = ['orange', 'black', 'brown']
snake_controls = [["<Up>", "<Down>", "<Left>", "<Right>"],
                  ["<w>", "<s>", "<a>", "<d>"],
                  ["<y>", "<h>", "<g>", "<j>"]]
snake_start_positions = [30, 10, 20]
snake_score_value = [0, 0, 0]
snakes = []

# food global vars
food_eaten = True
food_coordinates = [0, 0]
food_rectangle = ""
food_creator_id = ""
food_color = 'yellow'


def main():
    root = Tk.Tk()
    root.title("Python is a snake!")
    frame_left = Tk.Frame(root, padx=10, pady=10, height=20)
    frame_right = Tk.Frame(root, padx=10, pady=10)
    action_button = Tk.Button(frame_left, text="Start <Enter>", width=10, height=2)
    clear_button = Tk.Button(frame_left, text="Clear <Esc>", width=10, height=2)
    pause_button = Tk.Button(frame_left, text="Pause <p>", width=10, height=2)
    header = Tk.Label(root, text="")
    footer = Tk.Label(root, text="Written by Alexander Golikov n27051538@gmail.com")
    canvas = Tk.Canvas(root, width=canvas_width*brick_size, height=canvas_height*brick_size, bg=canvas_color)

    frame_left.pack(side='left', anchor='nw')
    action_button.pack(side='top', anchor='nw')
    clear_button.pack(side='top', anchor='nw')

    score_text = []
    score_header = []
    score_label = []
    for i in range(number_of_snakes):
        score_text.append(Tk.StringVar())
        score_text[i].set(snake_score_value[i])
        score_header.append(Tk.Label(frame_left, foreground=snake_colors[i], text=snake_colors[i]))
        score_header[i].pack(side='top')
        score_label.append(Tk.Label(frame_left, foreground=snake_colors[i], textvariable=score_text[i]))
        score_label[i].pack(side='top')

    pause_button.pack(side='top', anchor='nw')

    frame_right.pack(side='right')
    header.pack(side='top')
    canvas.pack(side='top')
    footer.pack(side='top')

    # create border
    canvas.pack()
    canvas.create_rectangle(0,     0,
                            brick_size*canvas_width, brick_size*canvas_height,
                            fill=border_color)
    canvas.create_rectangle(brick_size*1,     brick_size*1,
                            brick_size*(canvas_width-1), brick_size*(canvas_height-1),
                            fill=canvas_color, outline=border_outline_color, width=1)
    canvas.focus_set()
    action_button.bind("<Button-1>", lambda event: start(event, canvas, score_text))
    canvas.bind("<Return>", lambda event: start(event, canvas, score_text))
    clear_button.bind("<Button-1>", lambda event: clear(event, canvas, score_text))
    canvas.bind("<Escape>", lambda event: clear(event, canvas, score_text))
    pause_button.bind("<Button-1>", lambda event: pause(event, canvas, pause_button))
    canvas.bind("<p>", lambda event: pause(event, canvas, pause_button))

    # debug
    # canvas.bind("<Button-1>", on_left_click)

    # schedule food creator
    root.mainloop()


def clear(event, canvas, score_text):
    canvas.after_cancel(food_creator_id)
    canvas.delete
    canvas.create_rectangle(0,     0,
                            brick_size*canvas_width, brick_size*canvas_height,
                            fill=border_color)
    canvas.create_rectangle(brick_size*1,     brick_size*1,
                            brick_size*(canvas_width-1), brick_size*(canvas_height-1),
                            fill=canvas_color, outline=border_outline_color, width=1)
    canvas.focus_set()
    global snakes, food_eaten, food_coordinates
    for snake in snakes:
        snake.coordinates = []
        canvas.after_cancel(snake.move_task)
    snakes = []
    food_coordinates = [0,0]
    food_eaten = True
    for i in range(number_of_snakes):
        snake_score_value[i] = 0
        score_text[i].set(snake_score_value[i])
    canvas.focus_set()


def pause(event, canvas, pause_button):
    for snake in snakes:
        canvas.after_cancel(snake.move_task)
    pause_button.bind("<Button-1>", lambda event: unpause(event, canvas, pause_button))
    canvas.bind("<p>", lambda event: unpause(event, canvas, pause_button))
    canvas.focus_set()

def unpause(event, canvas, pause_button):
    for snake in snakes:
        if not snake.overlap:
            snake.move_task = snake.canvas.after(time_step, snake.move)
    pause_button.bind("<Button-1>", lambda event: pause(event, canvas, pause_button))
    canvas.bind("<p>", lambda event: pause(event, canvas, pause_button))
    canvas.focus_set()



def start(event, canvas, score_text):
    global snakes

    for i in range(number_of_snakes):
        zmey = Snake(canvas, snake_start_positions[i], snake_colors[i], score_text[i], i)
        canvas.bind(snake_controls[i][0], zmey.set_direction_up)
        canvas.bind(snake_controls[i][1], zmey.set_direction_down)
        canvas.bind(snake_controls[i][2], zmey.set_direction_left)
        canvas.bind(snake_controls[i][3], zmey.set_direction_right)
        snakes.append(zmey)

    global food_creator_id
    food_creator_id = canvas.after(time_step*2, food_creator, canvas, snakes)
    canvas.focus_set()


class Snake:

    def __init__(self, canvas, head_x, color, score_text, score_index):

        # self.coordinates is list of [x, y]
        self.coordinates = [[head_x, 7], [head_x, 8], [head_x, 9], [head_x, 10], [head_x, 11]]
        # self.coordinates is list of rectangle objects
        self.rectangles = []
        self.canvas = canvas
        self.color = color
        self.direction = "up"
        self.deaf = False
        self.score_text = score_text
        self.score_index = score_index
        self.overlap = False

        # add rectangle_object to every element of list self.bricks
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            self.rectangles.append(self.canvas.create_rectangle(brick_size*x,     brick_size*y,
                                   brick_size*(x+1), brick_size*(y+1),
                                   fill=self.color, outline=outline_color, width=1))
            # print(canvas.coords(self.rectangles[i]))

        self.move_task = self.canvas.after(time_step, self.move)

    def move(self):
        # print("move to [" + str(self.coordinates[0][0]) + ", " + str(self.coordinates[0][1]) + "] ")
        self.deaf = False
        track_step1 = self.coordinates[0][:]
        if self.direction == 'up':
            self.coordinates[0][1] -= 1
        elif self.direction == 'down':
            self.coordinates[0][1] += 1
        elif self.direction == 'left':
            self.coordinates[0][0] -= 1
        elif self.direction == 'right':
            self.coordinates[0][0] += 1
        self.canvas.coords(self.rectangles[0],
                           self.coordinates[0][0]*brick_size,
                           self.coordinates[0][1]*brick_size,
                           (self.coordinates[0][0]+1)*brick_size,
                           (self.coordinates[0][1]+1)*brick_size)

        #check food
        global food_eaten, food_coordinates, snake_score_value
        # print("self ", self.coordinates[0], "food ", food_coordinates)
        if self.coordinates[0][0] == food_coordinates[0] and self.coordinates[0][1] == food_coordinates[1]:
            self.coordinates.append(food_coordinates)
            self.rectangles.append(food_rectangle)
            # set color of eaten food to snakes color
            self.canvas.itemconfig(self.rectangles[len(self.rectangles)-1], fill=self.color)
            print(self.color + " zmey got food! Its current length is " + str(len(self.coordinates)))
            snake_score_value[self.score_index] += 1
            self.score_text.set(str(snake_score_value[self.score_index]))
            food_coordinates = [0, 0]
            food_eaten = True

        # move tail
        for i in range(1, len(self.coordinates)):
            track_step2 = self.coordinates[i][:]
            self.coordinates[i][0] = track_step1[0]
            self.coordinates[i][1] = track_step1[1]
            track_step1 = track_step2[:]
            self.canvas.coords(self.rectangles[i],
                               self.coordinates[i][0]*brick_size,
                               self.coordinates[i][1]*brick_size,
                               (self.coordinates[i][0]+1)*brick_size,
                               (self.coordinates[i][1]+1)*brick_size)

        for snake in snakes:
            for i in range(0, len(snake.coordinates)):
                if snake.coordinates[i] is not self.coordinates[0] and \
                        snake.coordinates[i][0] == self.coordinates[0][0] and \
                        snake.coordinates[i][1] == self.coordinates[0][1]:
                    self.overlap = True
                    snake.canvas.itemconfig(snake.rectangles[i], fill=alert_color)
                    self.canvas.itemconfig(self.rectangles[0], fill=alert_color)

        if not (1 <= self.coordinates[0][0] < canvas_width-1 and 1 <= self.coordinates[0][1] < canvas_height-1):
            self.overlap = True
            print('Seems that ' + self.color + ' zmey have crash! Stop! Its length is ' + str(len(self.coordinates)))
            self.canvas.itemconfig(self.rectangles[0], fill=alert_color)

        if not self.overlap:
            self.move_task = self.canvas.after(time_step, self.move)


    def set_direction_up(self, event):
        if self.direction != "down" and not self.deaf:
            self.direction = "up"
            self.deaf = True

    def set_direction_down(self, event):
        if self.direction != "up" and not self.deaf:
            self.direction = "down"
            self.deaf = True

    def set_direction_left(self, event):
        if self.direction != "right" and not self.deaf:
            self.direction = "left"
            self.deaf = True

    def set_direction_right(self, event):
        if self.direction != "left" and not self.deaf:
            self.direction = "right"
            self.deaf = True


def food_creator(canvas, snakes):
    global food_eaten, food_creator_id, food_coordinates, food_rectangle
    if food_eaten:
        while True:
            food_coordinates[0] = random.randint(1, canvas_width - 2)
            food_coordinates[1] = random.randint(1, canvas_height - 2)
            for snake in snakes:
                for coordinate in snake.coordinates:
                    if coordinate[0] == food_coordinates[0] and coordinate[1] == food_coordinates[1]:
                        continue
            break
        food_rectangle = canvas.create_rectangle(brick_size*food_coordinates[0],
                                                 brick_size*food_coordinates[1],
                                                 brick_size*(food_coordinates[0]+1),
                                                 brick_size*(food_coordinates[1]+1),
                                                 fill=food_color, outline=outline_color, width=1)
        print("New food created on ", food_coordinates, "!")

    food_eaten = False
    food_creator_id = canvas.after(time_step, food_creator, canvas, snakes)


def on_left_click(event):
    print("x=" + str(event.x) + " y=" + str(event.y))


if __name__ == '__main__':
    main()
