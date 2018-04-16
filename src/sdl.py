from typing import NamedTuple, Any, List, Optional
from ctypes import CDLL, byref, c_int, c_char_p, Structure
from enum import Enum
from contextlib import suppress, AbstractContextManager


class LibraryNotFound(BaseException):

    pass


class CEnum(Enum):

    def __init__(self, value: int) -> None:
        self._as_parameter_ = value


class Event(CEnum):

    QUIT = 0x100


class EventAction(CEnum):

    PEEK_EVENT = 1


def load_first_available(library_paths: List[str]) -> CDLL:
    for path in library_paths:
        with suppress(OSError):
            libsdl2 = CDLL(path)
            if libsdl2:
                return libsdl2

    raise LibraryNotFound(library_paths)


def load_libsdl2() -> CDLL:
    return load_first_available(['libSDL2-2.0.so', 'SDL2'])


def load_libsdl2_image() -> CDLL:
    return load_first_available(['libSDL2_image-2.0.so', 'SDL2_image'])


libsdl2 = load_libsdl2()
libsdl2_image = load_libsdl2_image()


def quit_requested() -> bool:
    libsdl2.SDL_PumpEvents()
    return bool(libsdl2.SDL_PeepEvents(None, 0,
                                       EventAction.PEEK_EVENT,
                                       Event.QUIT, Event.QUIT))


class Error(BaseException):

    def __init__(self) -> None:
        get_error = libsdl2.SDL_GetError
        get_error.restype = c_char_p
        super().__init__(get_error())


class Dimensions(NamedTuple):

    width: int
    height: int


class Color(NamedTuple):

    r: int
    g: int
    b: int
    a: int = 255

    @staticmethod
    def black() -> 'Color':
        return Color(0, 0, 0)

    @staticmethod
    def white() -> 'Color':
        return Color(255, 255, 255)


class Rectangle(NamedTuple):

    x: int
    y: int
    width: int
    height: int

    @property
    def _as_parameter_(self) -> Any:
        class SdlRect(Structure):

            _fields_ = [('x', c_int),
                        ('y', c_int),
                        ('w', c_int),
                        ('h', c_int)]

        return SdlRect(self.x, self.y, self.width, self.height)


class Window(AbstractContextManager):

    def __init__(self,
                 title: bytes,
                 dimensions: Dimensions) -> None:
        x = int(dimensions.width / 2)
        y = int(dimensions.height / 2)

        self.sdl_window = libsdl2.SDL_CreateWindow(title,
                                                   x, y,
                                                   dimensions.width,
                                                   dimensions.height,
                                                   0)

        if not self.sdl_window:
            raise Error

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        libsdl2.SDL_DestroyWindow(self.sdl_window)

    def renderer(self, draw_color: Optional[Color]=None) -> 'Renderer':
        return Renderer(self, draw_color)


class Renderer(AbstractContextManager):

    def __init__(self,
                 window: Window,
                 draw_color: Optional[Color]=None) -> None:
        self.sdl_renderer = libsdl2.SDL_CreateRenderer(window.sdl_window,
                                                       -1, 0)

        if not self.sdl_renderer:
            raise Error

        self.draw_color = draw_color or Color.white()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        libsdl2.SDL_DestroyRenderer(self.sdl_renderer)

    def load_texture(self, path: bytes) -> 'Texture':
        return Texture(self, path)

    def render_clear(self) -> None:
        if libsdl2.SDL_RenderClear(self.sdl_renderer) < 0:
            raise Error

    def render_present(self) -> None:
        if libsdl2.SDL_RenderPresent(self.sdl_renderer) < 0:
            raise Error

    def fill_rectangle(self, r: Rectangle) -> None:
        if libsdl2.SDL_RenderFillRect(self.sdl_renderer,
                                      byref(r._as_parameter_)) < 0:
            raise Error

    @property
    def draw_color(self) -> Color:
        r = c_int()
        g = c_int()
        b = c_int()
        a = c_int()

        if libsdl2.SDL_GetRenderDrawColor(self.sdl_renderer,
                                          byref(r),
                                          byref(g),
                                          byref(b),
                                          byref(a)) < 0:
            raise Error

        return Color(r.value, g.value, b.value, a.value)

    @draw_color.setter
    def draw_color(self, color: Color) -> None:
        if libsdl2.SDL_SetRenderDrawColor(self.sdl_renderer,
                                          color.r,
                                          color.g,
                                          color.b,
                                          color.a) < 0:
            raise Error

    def render_texture(self,
                       texture: 'Texture',
                       src: Rectangle,
                       dst: Rectangle) -> None:
        pass


class Texture(AbstractContextManager):

    def __init__(self, renderer: Renderer, path: bytes) -> None:
        self.sdl_texture = libsdl2_image.IMG_LoadTexture(renderer.sdl_renderer,
                                                         path)

        if not self.sdl_texture:
            raise Error

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        libsdl2.SDL_DestroyTexture(self.sdl_texture)
