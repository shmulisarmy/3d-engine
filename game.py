import pygame
from settings import screen, WIDTH, HEIGHT, FPS, BLACK, board

import sys



class Game:
    running = True
    full_block_height = HEIGHT // len(board)
    fullblock_width = WIDTH // len(board[0])
    from player import Player
    plr = Player()
    plr.game_data["full_block_height"] = full_block_height
    plr.game_data["fullblock_width"] = fullblock_width

    @staticmethod
    def frame_logic():
        for event in pygame.event.get():
            event: pygame.event.Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            Game.plr.handle_key(event)

        Game.plr.update()

    @staticmethod
    def frame_graphics():
        screen.fill(BLACK)
        Game.plr.draw_board(board)
        pygame.display.flip()


    @staticmethod
    def frame():
        Game.frame_logic()
        Game.frame_graphics()

    @staticmethod
    def run():
        while Game.running:
            Game.frame()
            pygame.time.Clock().tick(FPS)