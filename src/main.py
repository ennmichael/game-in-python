#!/usr/bin/env python3.6


import sdl


if __name__ == '__main__':
    with sdl.Window(b'Title', sdl.Dimensions(640, 480)) as window, \
         window.renderer() as renderer, \
         renderer.load_texture(b'character.png') as character_texture:

        def main_callback(delta: sdl.Seconds) -> None:
            renderer.render_clear()
            renderer.render_present()

        sdl.main_loop(main_callback)
