import sdl
import utils
import game


WINDOW_DIMENSIONS = sdl.Dimensions(640, 480)
TEXTURES_PATHS = [
    b'sprites/running.png'
]


if __name__ == '__main__':
    with sdl.destroying(sdl.Window(b'Title', WINDOW_DIMENSIONS)) as window, \
         sdl.destroying(window.renderer()) as renderer, \
         sdl.destroying(renderer.load_textures(TEXTURES_PATHS)) as textures:

        animation = game.Animation(textures[b'sprites/running.png'],
                                   frame_count=8,
                                   frame_delay=utils.Seconds(0.15),
                                   frame_width=100)

        position = 0 + 0j

        def main_callback(delta: utils.Seconds) -> None:
            global position
            position = position + delta * 100

            renderer.render_clear()
            animation.render(renderer, position)
            renderer.render_present()

        game.main_loop(main_callback)

        # TODO Make Igor move via keyboard
