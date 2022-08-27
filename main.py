import pygame 
import math
pygame.init()

HEIGHT = 700
WIDTH = 1000

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0) 
AQUA = "aqua"

shapes = []

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Illustrator")

window.fill(WHITE)


class Square:
    def __init__(self, square_x, square_y, square_width, square_height):
        self.square_x = square_x
        self.square_y = square_y
        self.square_width = square_width
        self.square_height = square_height

class Circle:
    def __init__(self, circle_x, cirlce_y, circle_radius):
        self.circle_x = circle_x
        self.circle_y = cirlce_y
        self.circle_radius = circle_radius

class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True

square_button  = Button(10, 10, 50, 30)
circle_button  = Button(10, 50, 50, 30)


def buttons(window):
    pygame.draw.rect(window, BLACK, pygame.Rect(square_button.x, square_button.y, square_button.width, square_button.height))
    pygame.draw.rect(window, BLACK, pygame.Rect(circle_button.x, circle_button.y, circle_button.width, circle_button.height))


def draw_square(window, x, y, width, height): 
    color = "black"
    pygame.draw.rect(window, color, pygame.Rect(x, y, width, height))

def draw_circle(window, x, y, radius):
    pygame.draw.circle(window, AQUA, (x, y), radius)

def square_logic(mouse_x_button_down, mouse_y_button_down, mouse_x_button_up, mouse_y_button_up, delta_x, delta_y):
    if delta_x > 0 and delta_y > 0:
        shapes.append(Square(mouse_x_button_down, mouse_y_button_down, delta_x, delta_y))
    elif delta_x < 0 and delta_y < 0 :
        shapes.append(Square(mouse_x_button_up, mouse_y_button_up, abs(delta_x), abs(delta_y)))
    elif delta_x < 0 and delta_y > 0:
        shapes.append(Square(mouse_x_button_up, mouse_y_button_down, abs(delta_x), delta_y))
    elif delta_x > 0 and delta_y < 0:
        shapes.append(Square(mouse_x_button_down, mouse_y_button_up, delta_x, abs(delta_y)))
        
def square_logic_for_drag(mouse_x_button_down, mouse_y_button_down, mouse_x, mouse_y, delta_x, delta_y):
    if delta_x > 0 and delta_y > 0:
        draw_square(window, mouse_x_button_down, mouse_y_button_down, delta_x, delta_y)
    elif delta_x < 0 and delta_y < 0 :
        draw_square(window, mouse_x, mouse_y, abs(delta_x), abs(delta_y))
    elif delta_x < 0 and delta_y > 0:
        draw_square(window, mouse_x, mouse_y_button_down, abs(delta_x), delta_y)
    elif delta_x > 0 and delta_y < 0:
        draw_square(window, mouse_x_button_down, mouse_y, delta_x, abs(delta_y))

def circle_logic(delta_x, delta_y, mouse_x_button_down, mouse_y_button_down, radius):
    if delta_x > 0 and delta_y > 0:
        shapes.append(Circle(mouse_x_button_down + delta_x/2, mouse_y_button_down + delta_y/2, radius))

def circle_logic_for_drag(delta_x, delta_y, mouse_x_button_down, mouse_y_button_down, radius):
    if delta_x > 0 and delta_y > 0:
        draw_circle(window, mouse_x_button_down + delta_x/2, mouse_y_button_down + delta_y/2, radius)

def draw_previous_shapes():
    for j in  range(len(shapes)):
        if type(shapes[j]) == Square:
            draw_square(window, shapes[j].square_x, shapes[j].square_y, shapes[j].square_width, shapes[j].square_height)
        if type(shapes[j]) == Circle:
            draw_circle(window, shapes[j].circle_x, shapes[j].circle_y, shapes[j].circle_radius)

def main():
    run = True
    mouse_button_down = False
    mouse_button_up = False
    shape = "square"
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_button_down, mouse_y_button_down = pygame.mouse.get_pos()
                print(mouse_x_button_down, mouse_y_button_down)
                mouse_button_down = True
                if square_button.clicked():
                    shape = "square"
                if circle_button.clicked():
                    shape = "circle"
                
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x_button_up, mouse_y_button_up = pygame.mouse.get_pos()
                print(mouse_x_button_up, mouse_y_button_up)
                mouse_button_up = True
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z and (pygame.key.get_mods() == 64 or pygame.key.get_mods() == 128):
                    try:
                        shapes.pop(len(shapes) - 1)
                        window.fill(WHITE)
                        draw_previous_shapes()
                    except:
                        pass

        buttons(window)
        
        if mouse_button_down == True :
            if mouse_button_up == True:
                mouse_button_down = False
                mouse_button_up = False

                delta_x = mouse_x_button_up - mouse_x_button_down
                delta_y = mouse_y_button_up - mouse_y_button_down

                radius = math.sqrt(delta_x*delta_x + delta_y*delta_y) /2

                print( delta_x, delta_y)

                if shape == "square":
                    square_logic(mouse_x_button_down, mouse_y_button_down, mouse_x_button_up, mouse_y_button_up, delta_x, delta_y)
                if shape == "circle":
                    circle_logic(delta_x, delta_y, mouse_x_button_down, mouse_y_button_down, radius)
            
            else:
                window.fill(WHITE)
                buttons(window)
                draw_previous_shapes()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                delta_x = mouse_x - mouse_x_button_down
                delta_y = mouse_y - mouse_y_button_down

                radius = math.sqrt(delta_x*delta_x + delta_y*delta_y) /2

                if shape == "square":
                    square_logic_for_drag(mouse_x_button_down, mouse_y_button_down, mouse_x, mouse_y, delta_x, delta_y)
                if shape == "circle":
                    circle_logic_for_drag(delta_x, delta_y, mouse_x_button_down, mouse_y_button_down, radius)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
