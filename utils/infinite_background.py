import pygame


class InfiniteBackground:
    def __init__(
        self,
        image_path,
        screen,
        camera,
        screen_height=0,
        scale=1,
        repeat_x=True,
        repeat_y=False,
    ):
        original = pygame.image.load(image_path).convert()
        if screen_height > 0:
            scale = screen_height / original.get_height()

        self.image = pygame.transform.scale(
            original, (original.get_width() * scale, original.get_height() * scale)
        )

        self.w = self.image.get_width()
        self.h = self.image.get_height()

        self.repeat_x = repeat_x
        self.repeat_y = repeat_y

        self.index_x = 0
        self.index_y = 0

        self.debug = False

        self.screen = screen
        self.camera_offset = camera.offset

    def draw(self):
        screen_w, screen_h = self.screen.get_size()

        if self.repeat_x:
            start_x = int(self.camera_offset.x // self.w) - 1
            end_x = start_x + screen_w // self.w + 3
        else:
            start_x = end_x = 0

        if self.repeat_y:
            start_y = int(self.camera_offset.y // self.h) - 1
            end_y = start_y + screen_h // self.h + 3
        else:
            start_y = end_y = 0

        self.index_x = self.camera_offset.x / self.w
        self.index_y = self.camera_offset.y / self.h

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                pos_x = x * self.w - self.camera_offset.x
                pos_y = y * self.h - self.camera_offset.y
                self.screen.blit(self.image, (pos_x, pos_y))

                if self.debug:
                    pygame.draw.line(
                        self.screen,
                        (255, 0, 0),
                        (pos_x, pos_y),
                        (pos_x, pos_y + self.h),
                        2,
                    )
