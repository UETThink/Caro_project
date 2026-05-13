import pygame 
import source.utils as utils

pygame.init()

# A class for the interface menu buttons
class Button():
    def __init__(self, image, x_pos, y_pos, text_input, font_size):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.button_font = pygame.font.SysFont("arial", font_size)
        self.text = self.button_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)
        
    def checkMousePos(self, pos):
        return pos[0] in range(self.rect.left, self.rect.right) and\
             pos[1] in range(self.rect.top, self.rect.bottom)

    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and\
            pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.button_font.render(self.text_input, True, 'yellow')
        else:
            self.text = self.button_font.render(self.text_input, True, "white")
            
    def draw(self, surface):
        self.update(surface)
        self.changeColor(pygame.mouse.get_pos())
        pygame.display.update()


class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.SIZE = 540 #size of the board image
        self.PIECE = 32 #size of the single pieces
        self.N = 15
        self.MARGIN = 23
        self.GRID = (self.SIZE - 2 * self.MARGIN) / (self.N-1)
        self.bg = pygame.image.load('../assets/board.jpg')
        self.bg = pygame.transform.scale(self.bg, (540, 540))
        self.black_piece = pygame.image.load('../assets/black_piece.png')
        self.black_piece = pygame.transform.scale(self.black_piece, (self.PIECE, self.PIECE))
        self.white_piece = pygame.image.load('../assets/white_piece.png')
        self.white_piece = pygame.transform.scale(self.white_piece, (self.PIECE, self.PIECE))
        self.button_img = pygame.image.load('../assets/button.png')
        self.button_img = pygame.transform.scale(self.button_img, (150, 60))

    def drawBoard(self, board):
        '''
        Draw the board every time the game is refreshed
        '''
        # draw the background
        self.screen.blit(self.bg, (self.MARGIN, self.MARGIN))

        for i in range(self.N):
            for j in range(self.N):
                pos_x, pos_y = utils.pos_map2pixel(i, j)
                if board[i][j] == 1:
                    self.screen.blit(self.black_piece, (pos_x, pos_y))
                elif board[i][j] == -1:
                    self.screen.blit(self.white_piece, (pos_x, pos_y))

    def drawResult(self, tie=False):
        '''
        Draw result when the game ends
        '''
        # Create font
        my_font = pygame.font.SysFont("arial", 30)
        # render text
        if tie:
            label = my_font.render("It's a tie!", True, (255, 255, 255))
        else:
            label = my_font.render("You lost!", True, (255, 255, 255))
        # create a rectangular object for the text surface object
        textRect = label.get_rect()
        # set the center coordinate of the text surface object
        textRect.center = (750, 200)
        self.screen.blit(label, textRect)

        # Restart button
        restart_button = Button(self.button_img, 750, 300, "Restart", 20)
        restart_button.draw(self.screen)
        # Exit button
        exit_button = Button(self.button_img, 750, 380, "Exit", 20)
        exit_button.draw(self.screen)

    def restartChoice(self, mouse_pos):
        # Restart button
        restart_button = Button(self.button_img, 750, 300, "Restart", 20)
        if restart_button.checkMousePos(mouse_pos):
            main()
        # Exit button
        exit_button = Button(self.button_img, 750, 380, "Exit", 20)
        if exit_button.checkMousePos(mouse_pos):
            pygame.quit()


def main():
    from source.gomoku import *

    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Gomoku")
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    ai = GomokuAI()
    ai.firstMove()
    interface = Interface(screen)
    move_counter = 1

    while True:
        interface.drawBoard(ai.boardMap)
        pygame.display.flip()

        # AI makes the move
        if ai.turn == 0:
            ai.emptyCells -= 1
            ai.turn = 1
            move_counter += 1
            move_i, move_j = ai_move(ai)
            print(f'AI plays at {move_i}, {move_j}')
            print(f'Empty cells left: {ai.emptyCells}')
            ai.setState(move_i, move_j, 1)
            ai.emptyCells -= 1
            result = ai.checkResult()
            check_results(interface, result)
            interface.drawBoard(ai.boardMap)
            pygame.display.flip()

        # Human makes the move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN\
                    and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                human_move = check_human_move(ai, mouse_pos)
                if human_move:
                    move_counter += 1
                    ai.turn = 0
                    print(f'Human plays at {human_move[0]}, {human_move[1]}')
                    print(f'Empty cells left: {ai.emptyCells}')
                    result = ai.checkResult()
                    check_results(interface, result)
                    if result != None:
                        interface.drawBoard(ai.boardMap)
                        pygame.display.flip()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN\
                                        and pygame.mouse.get_pressed()[0]:
                                    mouse_pos = pygame.mouse.get_pos()
                                    interface.restartChoice(mouse_pos)

        clock.tick(60)

if __name__ == "__main__":
    main()
