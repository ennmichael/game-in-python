import sdl
import utils
import game
from player import Wolfram


# TODO Handle views by just passing offset parameters all over the place


WINDOW_DIMENSIONS = sdl.Dimensions(640, 480)
TEXTURES_PATHS = [
    b'sprites/igor.png'
]


solid_boxes = [
    sdl.Rectangle(200 + 300j, sdl.Dimensions(1000, 10)),
    sdl.Rectangle(500 + 100j, sdl.Dimensions(10, 1000)),
]


if __name__ == '__main__':
    with sdl.destroying(sdl.Window(b'Title', WINDOW_DIMENSIONS)) as window, \
         sdl.destroying(window.renderer()) as renderer, \
         sdl.destroying(renderer.load_textures(TEXTURES_PATHS)) as textures:

        keyboard = sdl.Keyboard()

        wolfram = Wolfram(position=300 + 0j,
                          textures=textures)

        def main_callback(delta: utils.Seconds) -> None:
            print(wolfram.position)

            renderer.render_clear()

            for box in solid_boxes:
                renderer.draw_color = sdl.Color.black()
                renderer.fill_rectangle(wolfram.checkbox)
                renderer.fill_rectangle(box)
                renderer.draw_color = sdl.Color.white()

            wolfram.handle_keyboard(keyboard)
            wolfram.update_physics(solid_boxes, delta)
            wolfram.render(renderer)
            renderer.render_present()

        game.main_loop(main_callback, fps=60)
