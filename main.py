import sdl
import utils
import game
from igor import Igor


# TODO Rename the module `igor`, parhaps into player?
# TODO Handle views by just passing offset parameters all over the place


WINDOW_DIMENSIONS = sdl.Dimensions(640, 480)
TEXTURES_PATHS = [
    b'sprites/running.png'
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
            igor.update(delta)
            igor.render(renderer)
            renderer.render_present()

        game.main_loop(main_callback)

        # TODO Integrate some kind of blocks
        # TODO Make Igor interact with them (or rather, make Entity
        # interact with them later)? Primarly, make proper gravity stuff,
        # and then also proper collision checking
        # TODO Flush out a proper Entity design
