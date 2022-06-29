
import pygame
from random import choice


# OBJECT DETECTION - Detectar se o cursor está no alcance do texto, p/ ser clicado
class Button:
    """
    cursor_x || onde o mouse está no canvas horizontalmente (passado p/ essa var)
    cursor_y || onde a mouse está no canvas verticalmente (passado p/ essa var)
    range_x  || topo superior <- até canto inferior -> (range disso)
    range_y  || topo superior até topo inferior (range disso)
    """

    def __init__(self, cursor_x, cursor_y, range_x, range_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.range_x = range_x
        self.range_y = range_y

    # Verificar pelo mouse em [x, y] se ele está no alcance do botão (Achar o botão = True)
    def find(self):
        if self.cursor_x in self.range_x and self.cursor_y in self.range_y:
            return True
        else:
            return ''


# Criar retângulos, principalmente para o retângulo customizado que seguirá a imagem do personagem
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cursor = pygame.math.Vector2()

    # Criação (var collision_rect)
    def new_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


# HP admin 2 - Classe p/ criar textos p/ o Canvas
class Board:

    # Fonte não usadas aqui, então "par 1" é sempre "None"
    def set_font(self):
        self.the_font = pygame.font.Font(self.font_family, self.font_size)

    # Configuração do texto
    def set_text(self):
        self.text = self.the_font.render(self.label, False, self.color)

    # Configuração do retângulo envolto ao personagem
    def set_rect(self):
        self.text_rect = self.text.get_rect(topleft=(self.x, self.y))

    # Tornar o retângulo visível p/ verificação do seu alcance com o mouse p/ uso na função "find"
    def set_rect_visibility(self):
        pygame.draw.rect(screen, self.background_color, self.text_rect)

    def draw(self):
        screen.blit(self.text, (self.x, self.y))

    def exec_main_functions(self):
        # Textos com retângulos visíveis + plano de fundo
        if self.background:
            self.set_font()
            self.set_text()
            self.set_rect()
            self.set_rect_visibility()
            self.draw()
        # Textos sem retângulos
        else:
            self.set_font()
            self.set_text()
            self.set_rect()
            self.draw()

    def __init__(self, font_family, font_size, label, color, x, y, background, background_color):
        self.font_family = font_family
        self.font_size = font_size
        self.label = label
        self.color = color
        self.x = x
        self.y = y

        self.the_font = None
        self.text = None
        self.text_rect = None

        self.background = background
        if self.background:
            self.background_color = background_color


class Landscape(pygame.sprite.Sprite):
    def draw(self, screen_source):
        screen_source.blit(self.image, (self.x, self.y))

    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image_width = self.image.get_width()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.vector = None


class Enemy:

    # "self.image" e "self.rect", definidos em "sprite_admin", são exibidos no Canvas por esta função
    def draw(self):
        self.canvas.blit(self.image, self.rect)

    # Usada na função "sprite_admin" p/ converter imagens p/ um tamanho customizado
    def resized_enemy(self, img):
        return pygame.transform.scale(img, (self.width_, self.height_))

    # Atribuição das vars das imagens e de seus retângulos com base em "self.current_sprite_index"
    # "self.delay" controla quando "self.current_sprite_index" deve mudar seu valor
    # Lógica: se "self.current_sprite_index=2", exibirá o sprite "2" do seu grupo de sprites
    # O grupo de sprites não faz movimentos uniformas, pois o atraso não é um valor único (choice)
    def sprite_admin_enemy(self):
        self.delay += 1
        if self.delay % choice([*range(2, 11)]) == 0:
            self.current_sprite_index += 1

        "LOOP REDUZIDO PARA EVITAR REPETIÇÃO DE CÓDIGO"
        for group_index, group in enumerate(range(self.groups)):
            if self.shell == self.shells_variety[group_index]:
                for index, each_image in enumerate(self.shells_images[group_index]):
                    if self.current_sprite_index == index:
                        self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
                        self.rect = self.image.get_rect(center=self.rect.center)
                    if self.current_sprite_index > len(self.shells_images[group_index]):
                        self.current_sprite_index = 0

        "CÓDIGO ANTIGO"
        # if self.shell == 'shell_green':
        #     for index, each_image in enumerate(self.shells_green):
        #         if self.current_sprite_index == index:
        #             self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
        #             self.rect = self.image.get_rect(center=self.rect.center)
        #         if self.current_sprite_index > len(self.shells_green):
        #             self.current_sprite_index = 0
        # elif self.shell == 'shell_purple':
        #     for index, each_image in enumerate(self.shells_purple):
        #         if self.current_sprite_index == index:
        #             self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
        #             self.rect = self.image.get_rect(center=self.rect.center)
        #         if self.current_sprite_index > len(self.shells_purple):
        #             self.current_sprite_index = 0

    # Pega o retângulo de cada imagem e os movimenta horizontalmente e lateralmente
    def move(self):
        self.rect.right += choice(self.go_right)
        self.rect.left -= choice(self.go_left)

    # TODO 10.1: Detecta colisão do retângulo do inimigo com o do personagem (no loop do Pygame, é usado em loop)
    def enemy_collision(self, player_rectangle):
        if self.rect.colliderect(player_rectangle):
            # print('ouch')
            pygame.draw.rect(screen, 'cyan', player_rectangle, 10)
            return True
        else:
            return ''

    def __init__(self, shell, custom_size, width_, height_, pos):
        # Acessar o canvas de forma indireta (clone da var "screen")
        self.canvas = pygame.display.get_surface()

        # "self.image" e "self.rect" devem ser criadas, pois são os elementos principais p/ uso no canvas
        # Se for usar animação, elas precisam receber algum valor, e não pode ser "None"
        # Isso é feito p/ impedir que a função que muda os sprites, gerre erro (aqui, "sprite_admin")
        # Elas recebem valores como se fosse apenas trabalhar com uma imagem estática
        self.image = pygame.image.load('shells\\green_shell_1_tr.gif').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        # Var criada SOMENTE por haver uma variedade de inimigos
        self.shell = shell

        # Vars criadas SOMENTE se quiser que o inimigo tenha tamanho variado (tamanho 2x maior que as originais)
        self.proper_width = [*range(36, 51)]
        self.proper_height = [*range(32, 41)]

        # (True) p/ dimensões customizadas VS (False) p/ dimensões escolhidas pela classe
        self.custom_size = custom_size
        if self.custom_size:
            self.width_ = width_
            self.height_ = height_
        else:
            self.width_ = choice(self.proper_width)
            self.height_ = choice(self.proper_height)

        # Lista do path das imagens (range= qtd. de imagens criadas e índices que a lista terá)
        # As imagens mudam de nome apenas nos números, p/ facilitar o uso do "list comprehension"
        self.shells_green = [f'shells\\green_shell_{index}_tr.gif' for index in range(1, 5)]
        self.shells_purple = [f'shells\\purple_shell_{index}_tr.gif' for index in range(1, 5)]

        self.shells_variety = ['shell_green', 'shell_purple']
        self.shells_images = [self.shells_green, self.shells_purple]
        self.groups = len(self.shells_variety)

        # Vars que controlam a transição dos sprites criados acima e o tempo de transição delas
        # Vars usadas majoritariamente na função "sprite_admin"
        self.current_sprite_index = 0
        self.delay = 0

        # Vars que controlam a velocidade horizontal dos inimigos no canvas
        self.go_right = [*range(2, 8)]
        self.go_left = [*range(5, 11)]


class Player(pygame.sprite.Sprite):

    # TODO 4: Vars que controlam os valores em "self.controls", usadas na função "joystick"
    def idle_right_setup(self):
        self.controls['key']['going_left'] = False
        self.controls['key']['going_right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['right'] = True

    def idle_left_setup(self):
        self.controls['key']['going_right'] = False
        self.controls['key']['going_left'] = False
        self.controls['key']['right'] = False
        self.controls['key']['left'] = True

    def walk_right_setup(self):
        self.controls['key']['right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['going_left'] = False
        self.controls['key']['going_right'] = True

    def walk_left_setup(self):
        self.controls['key']['right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['going_right'] = False
        self.controls['key']['going_left'] = True

    # TODO 5: Engatilha funções que controlam os grupos de sprites, com base no input passado
    def joystick(self):
        if event.type == pygame.KEYDOWN:

            # TODO 7
            if event.key == pygame.K_w and self.ground_interaction(rect_collision):
                self.jump(this_much=-50)

            if event.key == pygame.K_d:
                self.walk_right_setup()
            if event.key == pygame.K_a:
                self.walk_left_setup()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.idle_right_setup()
            if event.key == pygame.K_a:
                self.idle_left_setup()

    # TODO 6.1: "self.rect" controla a criação dos retângulos de todos os sprites na função "sprite_admin"
    # TODO 6.2: Nesta função, se modifica a posição desses retângulos
    def go(self, go_by):
        if self.controls['key']['going_right']:
            self.rect.right += go_by
            self.rect_cursor.right += go_by  # TODO 9.2: Como esse retângulo alcançará o retângulo da câmera a ->

        if self.controls['key']['going_left']:
            self.rect.left -= go_by
            self.rect_cursor.left -= go_by  # TODO 9.3 Como esse retângulo alcançará o retângulo da câmera a <-

    # TODO 7.2
    def jump(self, this_much):
        self.gravity = this_much

    # TODO 7.3
    def falling_speed(self, falling_speed):
        self.gravity += falling_speed

    # TODO 7.4: Move o fundo do retângulo do personagem via "self.gravity" após seu salto
    def fall(self, rect_for_collision):
        self.rect.bottom += self.gravity
        # TODO: 10.11: O retângulo do item 4 também deve seguir verticalmente, por isso ele é um parâmetro aqui
        rect_for_collision.bottom += self.gravity

    # TODO 7.5: A função "jump" muda o fundo do retângulo do personagem (para cima)
    # TODO 7.6: A função "fall" muda o fundo do retângulo do personagem (para baixo)
    # TODO 7.7: Essa função determina até onde o fundo do retângulo deve ir (armazena resultado)
    def ground_interaction(self, rect_for_collision):
        canvas_height = 600
        surface_height = 61

        if self.rect.bottom >= (canvas_height - surface_height):
            self.rect.bottom = canvas_height - surface_height
            # TODO 10.12: E aqui também, p/ não sair da tela verticalmente p/ baixo
            rect_for_collision.bottom = canvas_height - surface_height
            return True

    # TODO 3: Usada na função "sprite_admin" p/ converter imagens p/ um tamanho customizado
    def resized(self, the_image):
        return pygame.transform.scale(the_image, self.sizes)

    # TODO 2.1: Função que controla a transição dos sprites
    def sprite_admin(self):
        # Ver exemplo abaixo, acima da condição 1
        frames = {
            'idle_right': [*range(7)],
            'idle_left': [*range(7)],
            'walk_right': [*range(9)],
            'walk_left': [*range(9)],
        }

        # Lista de inteiros convertidos p/ string para uso dentro das strings do "path" de cada imagem
        # Todos começam com 1, pois o número da primeira imagem é 1 (ex: "green_shell_1_tr.gif")
        # O último índice do range = último número da imagem, -1 (ex: "green_shell_8_tr.gif") = imagem 7
        frames_str = {
            'idle_right': [str(integer) for integer in range(1, 8)],
            'idle_left': [str(integer) for integer in range(1, 8)],
            'walk_right': [str(integer) for integer in range(1, 10)],
            'walk_left': [str(integer) for integer in range(1, 10)]
        }

        self.current_sprite_index += 1

        "========== EXEMPLO =========="
        "frames['idle_right']     = [0, 1, 2, 3, 4, 5, 6]"
        "frames_str['idle_right'] = ['1', '2', '3', '4', '5', '6', '7']"
        # SUPOSIÇÃO || se "self.current_sprite_index = 3", acessa "frames_str['idle_right'][3] = '4'"
        # ENTÃO     || f"sprites/wolf_idle_right_4_tr.png" ('4' inserido ao path da string)
        if self.controls['key']['right']:
            for index in range(len(frames['idle_right'])):
                if self.current_sprite_index == frames['idle_right'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/wolf_idle_right_{frames_str['idle_right'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['idle_right']):
                    self.current_sprite_index = 0

        if self.controls['key']['left']:
            for index in range(len(frames['idle_left'])):
                if self.current_sprite_index == frames['idle_left'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/wolf_idle_left_{frames_str['idle_left'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['idle_left']):
                    self.current_sprite_index = 0

        if self.controls['key']['going_right']:
            for index in range(len(frames['walk_right'])):
                if self.current_sprite_index == frames['walk_right'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/wolf_walk_right_{frames_str['walk_right'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['walk_right']):
                    self.current_sprite_index = 0

        if self.controls['key']['going_left']:
            for index in range(len(frames['walk_left'])):
                if self.current_sprite_index == frames['walk_left'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/wolf_walk_left_{frames_str['walk_left'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['walk_left']):
                    self.current_sprite_index = 0

    def pursuer_rectangle(self, rect_for_collision, rect_zipped_range, rect_wider_range, speed):

        # Quando o retângulo customizado alcança o ponto de colisão da câmera <-, essa variação melhora a precisão
        rect_for_collision.width = choice(rect_zipped_range)

        # Impedir o retângulo customizado de ir com retângulo do jogador ->, essa variação melhora a precisão
        if self.controls['key']['going_right'] and rect_for_collision.right >= 935:
            rect_for_collision.width = choice(rect_wider_range)
            rect_for_collision.right -= speed

        # Impedir o retângulo customizado de ir com retângulo do jogador <-
        if self.controls['key']['going_left'] and rect_for_collision.left <= 215:
            rect_for_collision.left += speed

        # Deslocar o retângulo customizado p/ acompanhar retângulo do jogador ->, fora do ponto de colisão
        if self.controls['key']['going_right']:
            rect_for_collision.right += speed

        # Deslocar o retângulo customizado p/ acompanhar retângulo do jogador <-, fora do ponto de colisão
        if self.controls['key']['going_left']:
            rect_for_collision.left -= speed

        # Quando o retângulo customizado alcança o ponto de colisão da câmera ->, essa variação melhora a precisão
        if not self.controls['key']['going_right'] and rect_for_collision.right >= 935:
            rect_for_collision.width = choice(rect_zipped_range)

    # HP admin - 3
    def health_admin(self, collision_var, int_box, health_penalty):

        if collision_var:
            self.health -= health_penalty
            # print(self.health)
            int_box.label = f'{round(self.health)}'

        if self.health <= 0:
            self.health = 100

    # SCORE admin
    def score_admin(self, collision_var, player_rect, int_box, minor_score, major_score):
        if not collision_var and not self.ground_interaction(player_rect):
            self.score += major_score
        if not collision_var and self.ground_interaction(player_rect):
            if self.controls['key']['going_right'] or self.controls['key']['going_left']:
                self.score += minor_score

        int_box.label = str(round(self.score))

    def __init__(self, pos, group):
        # TODO: O personagem recebe a herança "pygame.sprite.Sprite", que é parente de "pygame.sprite.Group"
        # TODO: Essas heranças dão acesso aos atributos destas classes, dentre elas: group
        # TODO: "group" pode ser acessado via função "objeto_classe.groups()"
        # TODO: A classe vinculada (esta), só pode desenhar na classe que passa a herança (Camera.camera_draw)
        # TODO: Objetos da classe vinculada são acessados via função "objeto_câmera.sprites()"
        super().__init__(group)

        # Acessar o canvas de forma indireta (clone da var "screen")
        self.canvas = pygame.display.get_surface()

        # Tamanho do sprite do personagem, usado na função "resizer"
        self.sizes = (70, 70)

        # "self.image" e "self.rect" devem ser criadas, pois são os elementos principais p/ uso no canvas
        # Se for usar animação, elas precisam receber algum valor, e não pode ser "None"
        # Isso é feito p/ impedir que a função que muda os sprites, gerre erro (aqui, "sprite_admin")
        # Elas recebem valores como se fosse apenas trabalhar com uma imagem estática
        self.image = pygame.image.load('sprites/wolf.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        # TODO 9.1 Retângulo que colidirá com o retângulo da câmera, via classe "Camera" e função "camera_draw"
        # Ele fica no meio da tela, e também no meio de outro retângulo: o da câmera
        # Ele trabalha em conjunto com "self.camera_rect" da classe "Camera"
        # Quando o jogador move pela função "go", este retângulo move junto
        # Quando o ponto x -> desse retângulo ocupa x -> do retângulo da câmera, o cenário move
        self.rect_cursor = pygame.Rect(600, 300, 25, 25)

        # TODO 1.1: Var que controla a movimentação horizontal do personagem, e qual sprite do grupo é exibido
        # Essas chaves são alteradas constantemente entre 4 conjuntos de funções de sufixo "setup"
        # As funções que alteram essas chaves são usadas na função "joystick" com base no input dado pelo usuário
        self.controls = {
            'key': {
                'going_right': False,
                'going_left': False,
                'right': True,
                'left': False
            }
        }

        # Var que controlam a transição dos sprites criados dentro da função "sprite_admin"
        self.current_sprite_index = 0

        # TODO 7.1: Var que controla o retângulo do personagem p/ cima via funções "jump", "falling_speed", "fall"
        self.gravity = 0

        # HP admin 1
        self.health = 100
        self.score = 0


class Camera(pygame.sprite.Group):

    def camera_draw(self):
        for index, sprite in enumerate(sorted(self.sprites(), key=lambda sprite_: sprite_.rect.topleft)):
            sprite_offset = sprite.rect.topleft - self.camera_offset
            # print(index, sprite)
            # self.canvas.blit(sprite.image, sprite.rect)
            self.canvas.blit(sprite.image, sprite_offset)

    def camera_pursuer(self, target):
        self.camera_offset.x = target.rect.centerx - 600
        self.camera_offset.y = target.rect.centery - 300

    # TODO 8.4: Os parâmetros é um retângulo criado na classe "Player"
    # TODO 8.5: O retângulo se mexe junto com a superfície do jogador
    # TODO 8.6: Quando a ->/<- deste retângulo alcança a ->/<- do retângulo da câmera, o cenário se movimenta
    def camera_window(self, target_rect_left, target_rect_right):
        if target_rect_left < self.camera_rect.left:
            self.camera_rect.left = target_rect_left
        if target_rect_right > self.camera_rect.right:
            self.camera_rect.right = target_rect_right

        # TODO 8.7 O deslocamento
        self.camera_offset.x = self.camera_rect.left - self.camera_attribs['left']

    def __init__(self):
        super().__init__()

        self.canvas = pygame.display.get_surface()

        # TODO 8.1: Configuração do retângulo da câmera
        # TODO 8.2: Esse retângulo colide com um retângulo criado na classe "Player"
        # TODO 8.3: O resultado dessa colisão é o deslocamento da câmera
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.camera_attribs = {'top': 200, 'bottom': 200, 'left': 250, 'right': 250}
        top_ = self.camera_attribs['top']
        left_ = self.camera_attribs['left']
        width_ = self.canvas.get_size()[0] - (self.camera_attribs['left'] + self.camera_attribs['right'])
        height_ = self.canvas.get_size()[1] - (self.camera_attribs['top'] + self.camera_attribs['bottom'])
        self.camera_rect = pygame.Rect(left_, top_, width_, height_)

        # Centralizadores da câmera, usados na função "camera_pursuer"
        self.half_width = self.canvas.get_size()[0] // 2
        self.half_height = self.canvas.get_size()[1] // 2


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()


def scenario(label):
    if label == 'opening':
        canvas = pygame.display.get_surface().get_size()
        pygame.display.get_surface().fill('black')
        play_button = Board(None, 50, 'JOGAR', 'cyan', canvas[0] // 2, canvas[1] // 2, True, '#222222')
        play_button.exec_main_functions()


# OBJECT DETECTION
mouse = [0, 0]

camera = Camera()
main_background = Landscape('landscapes/background.png', 0, 0, camera)
hills = Landscape('landscapes/hills.png', 0, 0, camera)

# Jogador inicia em queda, mas seu retângulo principal acha o ponto de parada via função "ground_interaction"
player = Player((600, 300), camera)

# Retângulo p/ acompanhar a imagem do personagem
rect_collision = Rectangle(565, 600 - (60 + 71), 70, 70).new_rect()

# HP admin - 4
written_content = {
    'hp_label': Board(None, 40, 'Saúde: ', 'white', 10, 50, False, ''),
    'hp_label_int': Board(None, 40, str(player.health), 'yellowgreen', 125, 50, False, ''),
    'pt_label': Board(None, 40, 'Pontos: ', 'white', 10, 90, False, ''),
    'pt_label_int': Board(None, 40, str(player.score), 'orangered', 125, 90, False, '')
}

# OBJECT DETECTION (diretamente conectado a "clickable_texts")
buttons = {
    'exit': Board(None, 40, 'Voltar <-', 'yellow', 1000, 50, True, 'purple')
}

# Criação do inimigo
kind = ['shell_green', 'shell_purple']
where = [*range(1300, 5001)]
enemies = []
for number in range(100):
    enemies.append(Enemy(shell=choice(kind), custom_size=False, width_=0, height_=0, pos=(choice(where), 600 - 61)))


while True:
    screen.fill('#222222')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

        # OBJECT DETECTION - Atualização da posição do mouse em tempo real (armazenado em "mouse" fora do loop)
        if event.type == pygame.MOUSEMOTION:
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]
            # print(mouse)

        print(pygame.mouse.get_pressed()[0])

        # TODO 5: Não pode haver duas chamadas de evento, então esta função é uma extensão do evento
        player.joystick()

    # OBJECT DETECTION (criada dentro do loop, pois funciona somente após a atualização da posição na var "mouse")
    clickable_texts = {
        'exit': Button(cursor_x=mouse[0], cursor_y=mouse[1], range_x=[*range(1000, 1116)], range_y=[*range(50, 77)])
    }

    # Desenhar no CANVAS os objetos que compartilham de herança com o objeto desta classe
    camera.camera_draw()

    # Textos não clicáveis (HP admin - 5)
    for text in written_content.keys():
        written_content[text].exec_main_functions()

    # OBJECT DETECTION - Textos clicáveis
    for text in buttons.keys():
        buttons[text].exec_main_functions()

    # OBJECT DETECTION - Detecção do alcançe dos textos clicáveis
    for button in clickable_texts.keys():
        # Cursor naárea do botão & botão <- de mouse pressionado
        if clickable_texts[button].find() and pygame.mouse.get_pressed()[0]:
            pass

    # Funções que controlam todas as funções dos inimigos
    for enemy in enemies:
        enemy.sprite_admin_enemy()
        enemy.draw()
        enemy.move()

    # TODO 10.2: Para cada inimigo, verificar a colisão
    # TODO 10.3: Explicação sobre os 4 retângulos do mecanismo
    # TODO 10.4: 1. Retângulo principal    2. Retângulo cursor    3. Retângulo câmera    4. Retângulo colisão
    # TODO 10.5: Os itens 1 e 2 movem juntos via input, e ao alcançar a posição do item 3, os 3 ocupam x iguais
    # TODO 10.6: O item 2, alcançando 3, o 3 moverá a tela, e como os 3 estão juntos, eles vão embora juntos
    # TODO 10.7: O problema é que o item 1 controla colisão, mas descola do personagem ao alcançar a posição do item 3
    # TODO 10.8: Perdendo este retângulo 1, o jogador fica sem colisão, então é preciso outro, que é o item 4
    # TODO 10.9: O item 4 também segue os demais, mas quando alcança o item 3, ele é lançado em direção oposta
    # TODO 10.10: O item 4 tenta se manter na posição da imagem do personagem (a precisão não consegue ser 100%)
    for enemy in enemies:
        collision = enemy.enemy_collision(rect_collision)
        # HP admin - 6
        player.health_admin(collision, written_content['hp_label_int'], 0.25)
        # SCORE admin
        player.score_admin(collision, rect_collision, written_content['pt_label_int'], 0.001, 0.007)

    # TODO 2.2: Chamada da função
    player.sprite_admin()

    # TODO 8.8 Chamada da função
    camera.camera_window(player.rect_cursor.left, player.rect_cursor.right)
    # camera.camera_pursuer(player)

    # TODO 6.3 Chamada da função
    player.go(10)

    # TODO 7.6: Chamada das 4 funções neste grupo, mas "jump" é usada dentro da função "joystick"
    player.falling_speed(4)
    player.fall(rect_collision)
    player.ground_interaction(rect_collision)

    # Retângulos no CANVAS: ['câmera', 'do personagem que mexe a câmera', 'que segue o personagem'] (manipulado p/ isso)
    pygame.draw.rect(screen, 'black', camera.camera_rect, 1)
    pygame.draw.rect(screen, 'crimson', player.rect_cursor, 1)
    pygame.draw.rect(screen, 'blue', rect_collision, 1)

    "NÃO FUNCIONOU QUANDO O CANTO DAS TELAS X [<-, ->] ERAM PARÂMETROS (valores literais na função corrigiram isso)"
    player.pursuer_rectangle(
        rect_for_collision=rect_collision,
        rect_zipped_range=[*range(50, 71)],
        rect_wider_range=[*range(50, 101)],
        speed=10
    )

    pygame.display.update()
    clock.tick(30)
