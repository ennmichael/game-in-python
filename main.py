import sdl
import utils
import game
import collision
from player import Igor


# TODO Handle views by just passing offset parameters all over the place


WINDOW_DIMENSIONS = sdl.Dimensions(640, 480)
TEXTURES_PATHS = [
    b'sprites/igor.png'
]


walls = [
    collision.Wall(100 + 0j, 200 + 200j)
]


def draw_walls(renderer: sdl.Renderer) -> None:
    for wall in walls:
        renderer.draw_color = sdl.Color.black()
        renderer.draw_line(wall.position, wall.position + wall.free_vector)
        renderer.draw_color = sdl.Color.white()


if __name__ == '__main__':
    with sdl.destroying(sdl.Window(b'Title', WINDOW_DIMENSIONS)) as window, \
         sdl.destroying(window.renderer()) as renderer, \
         sdl.destroying(renderer.load_textures(TEXTURES_PATHS)) as textures:

        keyboard = sdl.Keyboard()

        igor = Igor(position=0 + 0j,
                    textures=textures)

        def main_callback(delta: utils.Seconds) -> None:
            renderer.render_clear()

            if collision.will_collide(igor, walls[0], delta):
                print('Will collide')

            draw_walls(renderer)
            igor.handle_keyboard(keyboard)
            game.update_physics(igor, walls, delta)
            igor.render(renderer)
            renderer.render_present()

        game.main_loop(main_callback, fps=60)
