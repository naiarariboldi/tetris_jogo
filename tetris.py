import pygame as pg
import random
import time
from ranking_screen import ranking_screen
from ranking import RankingDB
from logger import log_error, log_info, log_warning, log_debug


class Tetris:
    def __init__(self, window_size):
        try:
            log_info("Inicializando jogo Tetris")
            self.window = pg.display.set_mode((window_size * 14, window_size * 20), pg.FULLSCREEN)
            pg.font.init()
            self.font = pg.font.SysFont("Courier New", window_size, bold=True)
            self.clock = pg.time.Clock()
            self.time = 0

            self.black = (155, 103, 168)
            self.white = (255,255,255)
            self.gray = (150,150,150)
            
            self.roxo1 = (128, 0, 128)
            self.rosa1 = (255, 182, 193)  
            self.roxo2 = (75, 0, 130)
            self.rosa2 = (255, 105, 180)
            self.roxo3 = (147, 112, 219)
            self.rosa3 = (255, 20, 147)  
            self.roxo4 = (186, 85, 211)     
            self.last_click_status = (False,False,False)

            self.starting_first_game = True
            self.show_restart_button = True
            self.board_square = window_size
            self.next_shapes_list = ["","","",""]
            self.init_random_shapes()
            self.score = 0
            self.speed = 1
            self.base_speed = 5
            self.speed_factor = 100
            self.dificuldade = "Normal"

            self.selected_form = 'shape_1'
            self.shape_pos = [4,0]
            self.shape_matrix = [[]]
            self.new_shape = True

            self.shape = {
                'shape_1': {'shape': [[1,1],[1,1]], 'color': self.rosa1},
                'shape_2': {'shape': [[0,1,0],[1,1,1]], 'color': self.roxo1},
                'shape_3': {'shape': [[1,1,1,1]], 'color': self.rosa2},
                'shape_4': {'shape': [[1,1,0],[0,1,1]], 'color': self.roxo2},
                'shape_5': {'shape': [[0,1,1],[1,1,0]], 'color': self.rosa3},
                'shape_6': {'shape': [[1,0,0],[1,1,1]], 'color': self.roxo3},
                'shape_7': {'shape': [[0,0,1],[1,1,1]], 'color': self.roxo4},
            }

            self.map = [[ '' for _ in range(10)] for _ in range(20)]

            log_info("Tetris inicializado com sucesso")
            
        except Exception as e:
            log_error("Erro na inicialização do Tetris", e)
            raise

    def clear_window(self):
        try:
            pg.draw.rect(self.window, self.black, (0,0,self.window.get_width(), self.window.get_height()))
        except Exception as e:
            log_error("Erro ao limpar a janela", e)

    def mouse_has_clicked(self, input):
        if self.last_click_status == input:
            return (False, False, False)
        left = self.last_click_status[0] == False and input[0] == True
        center = self.last_click_status[1] == False and input[1] == True
        right = self.last_click_status[2] == False and input[2] == True
        return (left, center, right)

    def board(self):
        for y in range(20):
            for x in range(10):
                pg.draw.rect(self.window, self.gray, (self.board_square*x, self.board_square*y, self.board_square, self.board_square), 1)
        pg.draw.rect(self.window, self.white, (0,0,self.board_square*10,self.board_square*20), 2)

        self.draw_shapes_in_game()

        self.text_box('Next', 10, 0, 4, 1, True)
        self.text_box('', 10, 1, 4, 13, False)
        self.draw_next_shapes()

        self.text_box('Score', 10, 14, 4, 1, True)
        self.text_box(str(self.score), 10, 15, 4, 2, False)

        self.text_box(self.dificuldade, 10, 17, 4, 1, True)
        self.text_box(str(self.speed)+'x', 10, 18, 4, 2, False)

    def text_box(self, text, x, y, width, height, fill):
        X = self.board_square * x
        Y = self.board_square * y
        W = self.board_square * width
        H = self.board_square * height
        if fill:
            pg.draw.rect(self.window, self.white, (X,Y,W,H))
            txt = self.font.render(text, True, self.black)
        else:
            pg.draw.rect(self.window, self.white, (X,Y,W,H), 1)
            txt = self.font.render(text, True, self.white)
        self.window.blit(txt, (X + W/2 - txt.get_width()/2, Y + H/2 - txt.get_height()/2))

    def new_random_shape(self):
        return 'shape_' + str(random.randint(1,7))

    def add_random_shape(self):
        for i in range(len(self.next_shapes_list)-1):
            self.next_shapes_list[i] = self.next_shapes_list[i+1]
        self.next_shapes_list[-1] = self.new_random_shape()

    def init_random_shapes(self):
        for i in range(4):
            self.next_shapes_list[i] = self.new_random_shape()

    def draw_next_shapes(self):
        for i, sh in enumerate(self.next_shapes_list):
            shape = self.shape[sh]['shape']
            color = self.shape[sh]['color']
            bx = self.board_square * 12 - (len(shape[0])/2 * self.board_square)
            by = self.board_square * 3 - (len(shape)/2 * self.board_square) + (i*3*self.board_square)
            border_color = tuple(min(c+50,255) for c in color)
            for y in range(len(shape)):
                for x in range(len(shape[0])):
                    if shape[y][x] == 1:
                        px = bx + x*self.board_square
                        py = by + y*self.board_square
                        pg.draw.rect(self.window, color, (px,py,self.board_square,self.board_square))
                        pg.draw.rect(self.window, border_color, (px,py,self.board_square,self.board_square), 1)

    def get_next_shape(self):
        try:
            self.selected_form = self.next_shapes_list[0]
            self.shape_matrix = self.shape[self.selected_form]['shape']
            self.add_random_shape()
            self.new_shape = False
            self.shape_pos = [4,0]
            log_debug(f"Nova peça: {self.selected_form}")
        except Exception as e:
            log_error("Erro ao obter próxima peça", e)

    def did_shape_collide_sideways(self):
        sx, sy = self.shape_pos
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    if self.map[sy+y][sx+x] != '':
                        return True
        return False

    def is_shape_in_the_game(self):
        sx = self.shape_pos[0]
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    if not (0 <= sx+x <= 9):
                        return False
        return True

    def rotate_shape_to_the_right(self):
        t = list(zip(*self.shape_matrix))
        self.shape_matrix = [list(r[::-1]) for r in t]

    def rotate_shape_to_the_left(self):
        t = list(zip(*self.shape_matrix))
        self.shape_matrix = [list(r) for r in t[::-1]]

    def send_shape_to_end(self):
        for _ in range(20):
            self.shape_pos[1] += 1
            sx, sy = self.shape_pos
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1:
                        try:
                            if self.map[sy+y][sx+x] != '':
                                self.shape_pos[1] -= 1
                                self.lock_shape()
                                return
                        except:
                            self.shape_pos[1] -= 1
                            self.lock_shape()
                            return

    def move(self, key):
        if key in ('a','left'):
            self.shape_pos[0] -= 1
            if not self.is_shape_in_the_game() or self.did_shape_collide_sideways():
                self.shape_pos[0] += 1
        elif key in ('d','right'):
            self.shape_pos[0] += 1
            if not self.is_shape_in_the_game() or self.did_shape_collide_sideways():
                self.shape_pos[0] -= 1
        elif key in ('s','down'):
            self.shape_pos[1] += 1
        elif key == 'q':
            self.rotate_shape_to_the_left()
            if not self.is_shape_in_the_game():
                self.rotate_shape_to_the_right()
        elif key == 'e':
            self.rotate_shape_to_the_right()
            if not self.is_shape_in_the_game():
                self.rotate_shape_to_the_left()
        elif key == 'space':
            self.send_shape_to_end()

    def get_color(self, code):
        table = {
            'r1': self.roxo1, 's1': self.rosa1, 'r2': self.roxo2, 
            's2': self.rosa2, 'r3': self.roxo3, 's3': self.rosa3, 
            'r4': self.roxo4, 'x': self.gray
        }
        return table.get(code)

    def get_color_code(self, color):
        table = {
            self.roxo1: 'r1', self.rosa1: 's1', self.roxo2: 'r2',
            self.rosa2: 's2', self.roxo3: 'r3', self.rosa3: 's3',
            self.roxo4: 'r4'
        }
        return table.get(color)

    def draw_shapes_in_game(self):
        for y in range(20):
            for x in range(10):
                if self.map[y][x] != '':
                    c = self.get_color(self.map[y][x])
                    bc = tuple(min(v+50,255) for v in c)
                    pg.draw.rect(self.window, c, (self.board_square*x,self.board_square*y,self.board_square,self.board_square))
                    pg.draw.rect(self.window, bc, (self.board_square*x,self.board_square*y,self.board_square,self.board_square), 1)

        sx, sy = self.shape_pos
        color = self.shape[self.selected_form]['color']
        bc = tuple(min(v+50,255) for v in color)
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    px = (sx+x)*self.board_square
                    py = (sy+y)*self.board_square
                    pg.draw.rect(self.window, color, (px,py,self.board_square,self.board_square))
                    pg.draw.rect(self.window, bc, (px,py,self.board_square,self.board_square), 1)

    def game_speed(self):
        self.speed = min(self.base_speed + (self.score // self.speed_factor), 50)

    def add_point(self, rows):
        for y in range(len(self.shape_matrix)):
            for x in range(len(self.shape_matrix[0])):
                if self.shape_matrix[y][x] == 1:
                    self.score += 1
        self.score += rows * 10
        self.game_speed()
        self.time = 0

    def lock_shape(self):
        try:
            sx, sy = self.shape_pos
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1:
                        self.map[sy+y][sx+x] = self.get_color_code(self.shape[self.selected_form]['color'])

            self.get_next_shape()

            completed = 0
            for y in range(20):
                if all(self.map[y][x] != '' for x in range(10)):
                    completed += 1

            self.add_point(completed)
            if completed > 0:
                log_info(f"Linhas completadas: {completed}")
                self.remove_completed_rows()
                
        except Exception as e:
            log_error("Erro ao travar peça", e)

    def game_step(self):
        try:
            self.time += 1
            if self.time == 61 - self.speed:
                self.shape_pos[1] += 1
                self.time = 0

            sx, sy = self.shape_pos
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1:
                        try:
                            if self.map[sy+y][sx+x] != '':
                                self.shape_pos[1] -= 1
                                self.lock_shape()
                                return
                        except IndexError as e:
                            log_warning("Índice fora dos limites no game_step")
                            self.shape_pos[1] -= 1
                            self.lock_shape()
                            return
        except Exception as e:
            log_error("Erro no game_step", e)

    def remove_completed_rows(self):
        completed = []
        for y in range(20):
            if all(self.map[y][x] != '' for x in range(10)):
                completed.append(y)
                for x in range(10):
                    self.map[y][x] = 'x'

        self.clear_window()
        self.board()
        pg.display.update()
        time.sleep(1)

        for row in completed:
            for x in range(10):
                self.map[row][x] = ''

        for _ in completed:
            for y in range(19, -1, -1):
                if all(self.map[y][x] == '' for x in range(10)):
                    shift = 1
                    while y - shift >= 0:
                        for x in range(10):
                            self.map[y-shift+1][x] = self.map[y-shift][x]
                        shift += 1

    def is_game_end(self):
        sx, sy = self.shape_pos
        if not self.show_restart_button:
            for y in range(len(self.shape_matrix)):
                for x in range(len(self.shape_matrix[0])):
                    if self.shape_matrix[y][x] == 1 and self.map[sy+y][sx+x] != '':
                        self.show_restart_button = True
                        self.shape_matrix = [[]]
                        return

    def restart_button(self, mouse):
        if self.show_restart_button:
            c = (200, 100, 200)
            w = self.window.get_width()/2.5
            h = w/2.5
            x = self.window.get_width()/2 - w/2
            y = self.window.get_height()/2 - h/2
            b = int(self.board_square/5)

            pos, btn, click = mouse

            if x <= pos[0] <= x+w and y <= pos[1] <= y+h:
                hc = tuple(min(v+50,255) for v in c)
                pg.draw.rect(self.window, hc, (x,y,w,h))
                if click[0]:
                    self.restart_game(True)
            else:
                pg.draw.rect(self.window, c, (x,y,w,h))

            pg.draw.rect(self.window, self.white, (x,y,w,h), b)
            t = self.font.render("Restart", True, self.black)
            self.window.blit(t, (self.window.get_width()/2 - t.get_width()/2, self.window.get_height()/2 - t.get_height()/2))

    def restart_game(self, restart=False):
        try:
            if self.starting_first_game or restart:
                if restart:
                    try:
                        db = RankingDB()
                        db.add_score(None, self.score, self.dificuldade)
                        log_info(f"Jogo finalizado - Pontuação: {self.score}, Dificuldade: {self.dificuldade}")
                    except Exception as e:
                        log_error("Erro ao salvar pontuação no ranking", e)

                self.init_random_shapes()
                self.score = 0
                self.speed = 1
                for y in range(20):
                    for x in range(10):
                        self.map[y][x] = ''
                self.show_restart_button = False
                self.starting_first_game = False
                self.get_next_shape()
                log_info("Jogo reiniciado")
                
        except Exception as e:
            log_error("Erro ao reiniciar jogo", e)


def escolher_dificuldade(window):
    try:
        fonte = pg.font.SysFont("Arial", 40)
        fonte_small = pg.font.SysFont("Arial", 25)

        while True:
            window.fill((155, 103, 168))

            titulo = fonte.render("Selecione a dificuldade", True, (117, 18, 62))
            window.blit(titulo, (100, 80))

            op1 = fonte_small.render("1 - Fácil", True, (117, 18, 62))
            op2 = fonte_small.render("2 - Normal", True, (117, 18, 62))
            op3 = fonte_small.render("3 - Difícil", True, (117, 18, 62))
            op4 = fonte_small.render("4 - Insano", True, (117, 18, 62))

            window.blit(op1, (150, 180))
            window.blit(op2, (150, 220))
            window.blit(op3, (150, 260))
            window.blit(op4, (150, 300))

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        log_info("Dificuldade selecionada: Fácil")
                        return ("Fácil", 2, 200)
                    if event.key == pg.K_2:
                        log_info("Dificuldade selecionada: Normal")
                        return ("Normal", 12, 120)
                    if event.key == pg.K_3:
                        log_info("Dificuldade selecionada: Difícil")
                        return ("Difícil", 25, 70)
                    if event.key == pg.K_4:
                        log_info("Dificuldade selecionada: Insano")
                        return ("Insano", 70, 10)
                        
    except Exception as e:
        log_error("Erro na tela de seleção de dificuldade", e)
        raise


def menu_inicial():
    try:
        pg.init()
        largura = tetris.window.get_width()
        altura = tetris.window.get_height()
        fonte = pg.font.SysFont("Arial", 50)
        fonte_small = pg.font.SysFont("Arial", 30)

        log_info("Menu inicial iniciado")

        while True:
            tetris.clear_window()

            titulo = fonte.render("TETRIS", True, (117, 18, 62))
            iniciar = fonte_small.render("ENTER - Iniciar", True, (117, 18, 62))
            sair = fonte_small.render("ESC - Sair", True, (117, 18, 62))
            rank = fonte_small.render("R - Ranking", True, (117, 18, 62))

            tetris.window.blit(titulo, (largura//2 - titulo.get_width()//2, 150))
            tetris.window.blit(iniciar, (largura//2 - iniciar.get_width()//2, 300))
            tetris.window.blit(rank, (largura//2 - rank.get_width()//2, 340))
            tetris.window.blit(sair, (largura//2 - sair.get_width()//2, 380))

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    log_info("Jogo fechado pelo usuário")
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        log_info("Iniciando novo jogo")
                        diff, base, factor = escolher_dificuldade(tetris.window)
                        tetris.dificuldade = diff
                        tetris.base_speed = base
                        tetris.speed_factor = factor
                        return
                    if event.key == pg.K_ESCAPE:
                        log_info("Jogo fechado pelo usuário")
                        pg.quit()
                        quit()
                    if event.key == pg.K_r:
                        log_info("Abrindo tela de ranking")
                        ranking_screen(tetris.window)
                        
    except Exception as e:
        log_error("Erro no menu inicial", e)
        raise


try:
    tetris = Tetris(42)
    log_info("Instância do Tetris criada com sucesso")
except Exception as e:
    log_error("Falha ao criar instância do Tetris", e)
    raise

try:
    menu_inicial()

    while True:
        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    log_info("Jogo finalizado")
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    tetris.move(pg.key.name(event.key))
                    if pg.key.name(event.key) == 'escape':
                        log_info("Jogo finalizado pelo usuário")
                        pg.quit()
                        quit()

            mouse_position = pg.mouse.get_pos()
            mouse_input = pg.mouse.get_pressed()
            mouse_click = tetris.mouse_has_clicked(mouse_input)
            mouse = (mouse_position, mouse_input, mouse_click)

            tetris.clock.tick(60)
            tetris.clear_window()

            tetris.restart_game()

            if tetris.new_shape:
                tetris.get_next_shape()

            tetris.board()
            tetris.game_step()
            tetris.is_game_end()
            tetris.restart_button(mouse)

            tetris.last_click_status = mouse_input

            pg.display.update()
            
        except Exception as e:
            log_error("Erro no loop principal do jogo", e)

except Exception as e:
    log_error("Erro fatal no jogo", e)
    pg.quit()
    raise
