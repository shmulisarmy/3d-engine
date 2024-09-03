import pygame
from settings import screen, WIDTH, HEIGHT, colors
from position import Position



def shade_color(color):
    return (color[0]//2, color[1]//2, color[2]//2)

BLACK = (0, 0, 0)


class Player:
    def __init__(self):
        self.view_start_x, self.view_start_y = 0, 0
        self.viewAreaWidth, self.viewAreaHeight = 10, 10
        self.eyeLevel_y = 10
        self.eye_level_x = 10
        self.view_area_depth = 10
        
        self.game_data = {}

        self.pressed_keys = set()
    
    def handle_key(self, event):
        """handles the keyboard events\n
            by placing them or removing them from pressed_keys
            wich gets used in update()"""
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)


    def draw_layer_polygons(self, matrix, this_layers_width, this_layers_height):
        """gets drawn under the blocks starting from the layer furthest away"""
        if not (isinstance(matrix, list) and isinstance(matrix[0], list) and isinstance(matrix[0][0], int)):
            raise ValueError(f"matrix must be a 2D list of integers but got {type(matrix)}")
        offsetx = (WIDTH-this_layers_width)/2
        offsety = (HEIGHT-this_layers_height)/2
        block_width = this_layers_width // self.viewAreaWidth
        blockHeight = this_layers_height // self.viewAreaHeight
        for i, row in enumerate(matrix[:self.viewAreaHeight]):
            for j, cel in enumerate(row[:self.viewAreaWidth]):
                if not cel: continue
                view_y = self.view_start_y + i
                view_x = self.view_start_x + j
                color = colors[cel]
                y_pos = view_y * blockHeight
                x_pos = view_x * block_width


                top_left_corner = Position(offsety + y_pos, offsetx + x_pos).pair()
                top_right_corner = Position(offsety + y_pos, offsetx + x_pos + block_width).pair()
                bottom_right_corner = Position(offsety + y_pos + blockHeight, offsetx + x_pos + block_width).pair()
                bottom_left_corner = Position(offsety + y_pos + blockHeight, offsetx + x_pos).pair()

                eyeLevelPoint = Position(self.eyeLevel_y * self.game_data["full_block_height"], self.eye_level_x * self.game_data["fullblock_width"]).pair()


                if y_pos > self.eyeLevel_y * blockHeight:
                    pygame.draw.polygon(screen, shade_color(color), (bottom_right_corner, bottom_left_corner, eyeLevelPoint))
                    # draw line 
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, top_left_corner, 1)
                else:
                    pygame.draw.polygon(screen, shade_color(color), (top_right_corner, top_left_corner, eyeLevelPoint))
                    # draw line 
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottom_left_corner, 1)


                if x_pos > self.eye_level_x * block_width:
                    pygame.draw.polygon(screen, shade_color(color), (top_right_corner, bottom_right_corner, eyeLevelPoint))
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottom_right_corner, 1)
                else:
                    pygame.draw.polygon(screen, shade_color(color), (top_left_corner, bottom_left_corner, eyeLevelPoint))
                    pygame.draw.line(screen, BLACK, eyeLevelPoint, bottom_left_corner, 1)


    def draw_layer_blocks(self, matrix, this_layers_width, this_layers_height):
        """gets drawn over the polygons starting from the layer furthest away"""
        offsetx = (WIDTH-this_layers_width)/2
        offsety = (HEIGHT-this_layers_height)/2
        block_width = this_layers_width // self.viewAreaWidth
        blockHeight = this_layers_height // self.viewAreaHeight
        for i, row in enumerate(matrix[:self.viewAreaHeight]):
            for j, cel in enumerate(row[:self.viewAreaWidth]):
                if not cel: continue
                view_y = self.view_start_y + i
                view_x = self.view_start_x + j
                color = colors[cel]
                y_pos = view_y * blockHeight
                x_pos = view_x * block_width

                top_left_corner = Position(offsety + y_pos, offsetx + x_pos).pair()
                top_right_corner = Position(offsety + y_pos, offsetx + x_pos + block_width).pair()
                bottom_right_corner = Position(offsety + y_pos + blockHeight, offsetx + x_pos + block_width).pair()
                bottom_left_corner = Position(offsety + y_pos + blockHeight, offsetx + x_pos).pair()



                pygame.draw.rect(screen, color, (offsetx + x_pos, offsety + y_pos, block_width, blockHeight))

                pygame.draw.line(screen, BLACK, top_left_corner, top_right_corner, 1)
                pygame.draw.line(screen, BLACK, top_right_corner, bottom_right_corner, 1)
                pygame.draw.line(screen, BLACK, bottom_right_corner, bottom_left_corner, 1)
                pygame.draw.line(screen, BLACK, bottom_left_corner, top_left_corner, 1)



    def draw_layer(self, matrix, this_layers_width, this_layers_height):
        if not (isinstance(matrix, list) and isinstance(matrix[0], list) and isinstance(matrix[0][0], int)):
            raise ValueError(f"matrix must be a 2D list of integers but got {type(matrix)}")
       
        self.draw_layer_polygons(matrix, this_layers_width, this_layers_height)
        self.draw_layer_blocks(matrix, this_layers_width, this_layers_height)

                
                



                


                

    def draw_board(self, board):
        for i in range(min(self.view_area_depth, len(board))-1, 0, -1):
            print(f"drawing layer {i}")
            self.draw_layer(board[i], WIDTH/i, HEIGHT/i)


    def update(self):
        """gets these keys from the handle_key() method"""
        # Handle continuous key presses
        if pygame.K__left in self.pressed_keys:
            self.view_start_x += 1
            self.eye_level_x -= 1
        if pygame.K__right in self.pressed_keys:
            self.view_start_x -= 1
            self.eye_level_x += 1
        if pygame.K_UP in self.pressed_keys:
            self.view_start_y += 1
            self.eyeLevel_y -= 1
        if pygame.K_DOWN in self.pressed_keys:
            self.view_start_y -= 1
            self.eyeLevel_y += 1
        
        if pygame.K_a in self.pressed_keys:
            self.eye_level_x += 1
        if pygame.K_d in self.pressed_keys:
            self.eye_level_x -= 1
        if pygame.K_w in self.pressed_keys:
            self.eyeLevel_y += 1
        if pygame.K_s in self.pressed_keys:
            self.eyeLevel_y -= 1
        
        if pygame.K_SPACE in self.pressed_keys:
            self.view_area_depth += 1
        if pygame.K_RETURN in self.pressed_keys:
            self.view_area_depth -= 1