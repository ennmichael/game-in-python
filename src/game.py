import sdl
import utils


class Sprite(NamedTuple):

    frame_count: int
    frame_delay: Seconds
    dimensions: Dimensions


class SpriteSheet:

    def __init__(self, texture: Texture) -> None:
        self.texture = texture

    def render_sprite(self,
                      renderer: Renderer,
                      sprite: Sprite,
                      frame: int) -> None:
        width, height = self.sprite.dimensions
        src = Rectangle(frame * width, 0, width, height)
        dst = Rectangle(int(position.real), int(position.imag), width, height)
        renderer.render_texture()


class Animation:

    def __init__(self,
                 sprite_sheet: SpriteSheet,
                 sprite: Sprite) -> None:
        self.sprite_sheet = sprite_sheet
        self.change_sprite(sprite)

    def change_sprite(self, sprite: Sprite) -> None:
        self.sprite = sprite
        self.done = False
        self.start_time = current_time()

    def render(self, renderer: sdl.Renderer, position: complex) -> None:
        frame = 
        sprite_sheet.render_sprite(renderer, sprite, frame)
        
        # TODO This is where I stopped
        # What is needed next is to test the animation
        # and then implement keyboard handling
        # and then we can start implementing the game


