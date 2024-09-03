import pygame
from settings import screen, WIDTH, HEIGHT, colors
from position import Position



def shade_color(color):
    return (color[0]//2, color[1]//2, color[2]//2)

BLACK = (0, 0, 0)


class Player:
    def __init__(self):
        self.viewStartX, self.viewStartY = 0, 0
        self.viewAreaWidth, self.viewAreaHeight = 10, 10
        self.eyeLevel_y = 10
        self.eyeLevel_x = 10
        self.viewAreaDepth = 10
        
        self.gameData = {}

        self.pressed_keys = set()
    
    def handle_key(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)


    def draw_layer_polygons(self, matrix, this_layers_width, this_layers_height):
        if not (isinstance(matrix, list) and isinstance(matrix[0], list) and isinstance(matrix[0][0], int)):
            raise ValueError(f"matrix must be a 2D list of integers but got {type(matrix)}")
        offsetx = (WIDTH-this_layers_width)/2
        offsety = (HEIGHT-this_layers_height)/2
        blockWidth = this_layers_width // self.viewAreaWidth
        blockHeight = this_layers_height // self.viewAreaHeight
        for i, row in enumerate(matrix[:self.viewAreaHeight]):
            for j, cel in enumerate(row[:self.viewAreaWidth]):
                if not cel: continue
                view_y = self.viewStartY + i
                view_x = self.viewStartX + j
                color = colors[cel]
                y_pos = view_y * blockHeight
                x_pos = view_x * blockWidth


                topLeftCorner = Position(offsety + y_pos, offsetx + x_pos).pair()
                topRightCorner = Position(offsety + y_pos, offsetx + x_pos + blockWidth).pair()
                bottomRightCorner = Position(offsety + y_pos + blockHeight, offsetx + x_pos + blockWidth).pair()
                bottomLeftCorner = Position(offsety + y_pos + blockHeight, offsetx + x_pos).pair()

                eyeLevelPoint = Position(self.eyeLevel_y * self.gameData["fullBlockHeight"], self.eyeLevel_x * self.gameData["fullBlockWidth"]).pair()


                if y_pos > self.eyeLevel_y * blockHeight:
                    ... # draw bottom
                    pygame.draw.polygon(screen, shade_color(color), (bottomRightCorner, bottomLeftCorner, eyeLevelPoint))
                    # draw line 
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, topLeftCorner, 1)
                else:
                    ... # draw top
                    pygame.draw.polygon(screen, shade_color(color), (topRightCorner, topLeftCorner, eyeLevelPoint))
                    # draw line 
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottomLeftCorner, 1)


                if x_pos > self.eyeLevel_x * blockWidth:
                    ... # draw right
                    pygame.draw.polygon(screen, shade_color(color), (topRightCorner, bottomRightCorner, eyeLevelPoint))
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottomRightCorner, 1)
                else:
                    ... # draw left
                    pygame.draw.polygon(screen, shade_color(color), (topLeftCorner, bottomLeftCorner, eyeLevelPoint))
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottomLeftCorner, 1)


    def draw_layer_blocks(self, matrix, this_layers_width, this_layers_height):
        offsetx = (WIDTH-this_layers_width)/2
        offsety = (HEIGHT-this_layers_height)/2
        blockWidth = this_layers_width // self.viewAreaWidth
        blockHeight = this_layers_height // self.viewAreaHeight
        for i, row in enumerate(matrix[:self.viewAreaHeight]):
            for j, cel in enumerate(row[:self.viewAreaWidth]):
                if not cel: continue
                view_y = self.viewStartY + i
                view_x = self.viewStartX + j
                color = colors[cel]
                y_pos = view_y * blockHeight
                x_pos = view_x * blockWidth

                topLeftCorner = Position(offsety + y_pos, offsetx + x_pos).pair()
                topRightCorner = Position(offsety + y_pos, offsetx + x_pos + blockWidth).pair()
                bottomRightCorner = Position(offsety + y_pos + blockHeight, offsetx + x_pos + blockWidth).pair()
                bottomLeftCorner = Position(offsety + y_pos + blockHeight, offsetx + x_pos).pair()



                pygame.draw.rect(screen, color, (offsetx + x_pos, offsety + y_pos, blockWidth, blockHeight))

                pygame.draw.line(screen, BLACK, topLeftCorner, topRightCorner, 1)
                pygame.draw.line(screen, BLACK, topRightCorner, bottomRightCorner, 1)
                pygame.draw.line(screen, BLACK, bottomRightCorner, bottomLeftCorner, 1)
                pygame.draw.line(screen, BLACK, bottomLeftCorner, topLeftCorner, 1)



    def draw_layer(self, matrix, this_layers_width, this_layers_height):
        if not (isinstance(matrix, list) and isinstance(matrix[0], list) and isinstance(matrix[0][0], int)):
            raise ValueError(f"matrix must be a 2D list of integers but got {type(matrix)}")
       
        self.draw_layer_polygons(matrix, this_layers_width, this_layers_height)
        self.draw_layer_blocks(matrix, this_layers_width, this_layers_height)

                
                



                


                

    def draw_board(self, board):
        for i in range(min(self.viewAreaDepth, len(board))-1, 0, -1):
            print(f"drawing layer {i}")
            self.draw_layer(board[i], WIDTH/i, HEIGHT/i)


    def update(self):
        # Handle continuous key presses
        if pygame.K_LEFT in self.pressed_keys:
            self.viewStartX += 1
            self.eyeLevel_x -= 1
        if pygame.K_RIGHT in self.pressed_keys:
            self.viewStartX -= 1
            self.eyeLevel_x += 1
        if pygame.K_UP in self.pressed_keys:
            self.viewStartY += 1
            self.eyeLevel_y -= 1
        if pygame.K_DOWN in self.pressed_keys:
            self.viewStartY -= 1
            self.eyeLevel_y += 1
        
        if pygame.K_a in self.pressed_keys:
            self.eyeLevel_x += 1
        if pygame.K_d in self.pressed_keys:
            self.eyeLevel_x -= 1
        if pygame.K_w in self.pressed_keys:
            self.eyeLevel_y += 1
        if pygame.K_s in self.pressed_keys:
            self.eyeLevel_y -= 1
        
        if pygame.K_SPACE in self.pressed_keys:
            self.viewAreaDepth += 1
        if pygame.K_RETURN in self.pressed_keys:
            self.viewAreaDepth -= 1