

shell_box = []
shell_types = ['shell_purple', 'shell_green']
shell_amount = 10
speed_variations_left = [*range(7, 16)]
speed_variations_right = [*range(2, 8)]
shell_sizes = [*range(32, 46)]
shell_box_admin = set({})


class Enemy:

    def animate(self):
        self.is_animating = True

    def draw(self):
        self.canvas.blit(self.image, self.rect)

        # elif self.shell == 'shell_green':
        #     screen_source.blit(
        #         self.shell_green_surfaces[int(self.current_sprite)],
        #         self.shell_green_rectangles[int(self.current_sprite)]
        #     )

    # def update(self):
    #     self.current_sprite += random()
    #
    #     if self.shell == 'shell_purple':
    #
    #         if int(self.current_sprite) >= len(self.shell_purple_surfaces):
    #             self.current_sprite = 0
    #             self.is_animating = False
    #
    #         else:
    #             self.image = self.shell_purple_surfaces[int(self.current_sprite)]
    #             self.image_rect = self.shell_purple_rectangles[int(self.current_sprite)]
    #
    #     elif self.shell == 'shell_green':
    #
    #         if int(self.current_sprite) >= len(self.shell_green_surfaces):
    #             self.current_sprite = 0
    #             self.is_animating = False
    #
    #         else:
    #             self.image = self.shell_green_surfaces[int(self.current_sprite)]
    #             self.image_rect = self.shell_green_rectangles[int(self.current_sprite)]
    #
    # def move(self, direction, this_speed):
    #     if direction == 'left' and self.shell == 'shell_purple':
    #         for rect in self.shell_purple_rectangles:
    #             rect.left -= this_speed
    #
    #     elif direction == 'right' and self.shell == 'shell_purple':
    #         for rect in self.shell_purple_rectangles:
    #             rect.right += this_speed
    #
    #     if direction == 'left' and self.shell == 'shell_green':
    #         for rect in self.shell_green_rectangles:
    #             rect.left -= this_speed
    #
    #     elif direction == 'right' and self.shell == 'shell_green':
    #         for rect in self.shell_green_rectangles:
    #             rect.right += this_speed

    def resized(self, img):
        return pygame.transform.scale(img, (self.width_, self.height_))

    # TODO
    def sprite_admin(self):
        self.delay += 1
        if self.delay % 7 == 0:
            self.sprite_counter += 1
        if self.shell == 'shell_green':
            for index, each_image in enumerate(self.shells_green):
                if self.sprite_counter == index:
                    self.image = self.resized(pygame.image.load(each_image).convert_alpha())
                    self.rect = self.image.get_rect(topleft=(self.x, self.y))
                if self.sprite_counter > len(self.shells_green):
                    self.sprite_counter = 0

    def __init__(self, shell, custom_size, width_, height_, custom_xy, x, y):
        self.canvas = pygame.display.get_surface()
        self.image = None
        self.rect = None
        self.shell = shell
        self.custom_size = custom_size

        self.sizes = [*range(20, 51)]
        if self.custom_size:
            # Dimensões de escolha ou aleatórias
            self.width_ = width_
            self.height_ = height_
        else:
            self.width_ = randint(0, len(self.sizes))
            self.height_ = randint(0, len(self.sizes))

        self.custom_xy = custom_xy
        self.main_terrain_top_height = 61
        if self.custom_xy:
            self.x = x
            self.y = y
        else:
            self.x = randint(700, 1501)
            self.y = 600 - (self.height_ + self.main_terrain_top_height)

        self.shells_green = [f'shells\\green_shell_{index}_tr.gif' for index in range(1, 5)]
        self.shells_purple = [f'shells\\purple_shell_{index}_tr.gif' for index in range(1, 5)]

        self.sprite_counter = 0
        self.delay = 0

# for enemy in enemies:
    #     enemy.sprite_admin()
    #     enemy.draw()
