import pygame.mouse
from pygame import Surface, Rect, Color

from robingame.animation import damping_response
from robingame.examples.gui_examples.assets import button_flash
from robingame.gui import Menu
from robingame.gui.button import Button
from robingame.image import scale_image, brighten, SpriteAnimation
from robingame.objects import Game, Group, Particle
from robingame.utils import mouse_hovering_over, random_int


class MyButton(Button):
    image: Surface
    rect: Rect  # used for collision detection
    debug_color = Color("red")

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        image_rect = self.image.get_rect()
        image_rect.center = self.rect.center
        surface.blit(self.image, image_rect)
        if debug:
            pygame.draw.rect(surface, color=self.debug_color, rect=self.rect, width=1)
            pygame.draw.rect(surface, color=self.debug_color, rect=(*self.rect.center, 2, 2))


class ButtonWithImages(MyButton):
    frame_duration = 3

    @property
    def animation_frame(self):
        return self.tick // self.frame_duration

    def __init__(self, x: int, y: int, width: int, height: int, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.image_idle = button_flash.images[-1]
        self.image_pressed = brighten(scale_image(self.image_idle.copy(), 0.9), amount=-50)
        self.image = self.image_idle

    def state_idle(self):
        self.image = self.image_idle
        super().state_idle()

    def state_focus(self):
        self.image = self.animation.play_once(self.animation_frame, repeat_frame=0)
        super().state_focus()

    def state_press(self):
        self.image = self.image_pressed
        super().state_press()

    def on_focus(self):
        super().on_focus()
        self.animation = button_flash

    def on_release(self):
        super().on_release()
        self.animation = SpriteAnimation(images=[self.image_idle])


class BouncyButton(MyButton):
    frame_duration = 3

    def __init__(self, x: int, y: int, width: int, height: int, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.image = button_flash.play(0)
        sizes = [damping_response(t) for t in range(20)]
        self.animation = button_flash
        self.animation_timer = 99
        self.physics_timer = 0
        self.amplitude = 0
        self.damping = 0.4

    def state_press(self):
        super().state_press()
        self.amplitude = -0.5
        self.physics_timer = 0  # holds the physics on "frame" 1
        # self.damping = 0.4

    def on_focus(self):
        super().on_focus()
        self.animation_timer = 0
        self.physics_timer = 0
        self.amplitude = 0.1
        # self.damping = 0.15

    def update(self):
        super().update()
        self.image = self.animation.play_once(self.animation_timer // self.frame_duration)
        scale_factor = damping_response(
            self.physics_timer, amp=self.amplitude, damping=self.damping, freq=0.2
        )
        if abs(scale_factor) > 0.005:  # prevents jittering
            self.image = scale_image(self.image.copy(), 1 + scale_factor)
        self.physics_timer += 1
        self.animation_timer += 1


class ColoredButtonEffectsExample(Game):
    """
    This is an example where the Buttons have different colours/animations for each state and
    transition.
    """

    screen_color = (50, 50, 50)
    window_width = 500
    window_height = 500

    def __init__(self):
        super().__init__()
        self.scenes = Group()
        self.particles = Group()
        self.child_groups += [self.scenes, self.particles]
        menu = Menu()
        menu.buttons.add(
            ButtonWithImages(
                x=200,
                y=100,
                width=200,
                height=100,
                text="press and hold for smoke",
                on_release=(
                    lambda button: (
                        self.particles.add(Flash(x=button.rect.centerx, y=button.rect.centery)),
                        self.particles.add(
                            Glow(x=button.rect.centerx, y=button.rect.centery) for _ in range(50)
                        ),
                    )
                ),
                on_unfocus=(lambda button: self.particles.kill()),
            ),
            BouncyButton(x=200, y=300, width=200, height=100),
        )
        self.scenes.add(menu)


class Flash(Particle):
    gravity = 0.1
    friction = 0.01
    decay = 20
    color = (150, 200, 150)
    radius = 100


class Glow(Particle):
    gravity = 0.1
    friction = 0.05
    decay = 0.1
    color = (20, 20, 20)
    radius = 50

    def __init__(self, x, y):
        super().__init__(x, y, u=random_int(-5, 5), v=random_int(-5, 5))


if __name__ == "__main__":
    ColoredButtonEffectsExample().main()
