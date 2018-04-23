import sdl
import utils
import game
from player import Igor


# TODO Handle views by just passing offset parameters all over the place


WINDOW_DIMENSIONS = sdl.Dimensions(640, 480)
TEXTURES_PATHS = [
    b'sprites/igor.png'
]


if __name__ == '__main__':
    with sdl.destroying(sdl.Window(b'Title', WINDOW_DIMENSIONS)) as window, \
         sdl.destroying(window.renderer()) as renderer, \
         sdl.destroying(renderer.load_textures(TEXTURES_PATHS)) as textures:

        keyboard = sdl.Keyboard()

        igor = Igor(position=0 + 0j,
                    textures=textures)

        def main_callback(delta: utils.Seconds) -> None:
            renderer.render_clear()
            igor.handle_keyboard(keyboard)
            game.update_physics(igor, delta)
            print(igor.sprite.__class__.__name__)
            igor.render(renderer)
            renderer.render_present()

        game.main_loop(main_callback)
