#!/usr/bin/env python3.6


import sdl
import game
import utils


if __name__ == '__main__':
    with sdl.Window(b'Title', sdl.Dimensions(640, 480)) as window, \
         window.renderer() as renderer:

        x = 0.

        def main_callback(delta: utils.Seconds) -> None:
            global x

            x += delta * 50

            renderer.draw_color = sdl.Color.white()
            renderer.render_clear()
            renderer.draw_color = sdl.Color.black()
            renderer.render_present()

        game.main_loop(main_callback)
