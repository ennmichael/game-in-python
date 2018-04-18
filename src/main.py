#!/usr/bin/env python3.6


import sdl
import game
import utils


if __name__ == '__main__':
    with sdl.Window(b'Title', sdl.Dimensions(640, 480)) as window, \
         window.renderer() as renderer, \
         renderer.load_texture(b'sprites/running.png') as running:

        keyboard = sdl.Keyboard()

        animation = game.Animation(running,
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
