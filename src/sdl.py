from typing import NamedTuple, Any, List, Optional
import ctypes
import enum
import contextlib


class LibraryNotFound(BaseException):

    pass


@enum.unique
class Event(enum.IntEnum):

    QUIT = 0x100


@enum.unique
class EventAction(enum.IntEnum):

    PEEK_EVENT = 1


@enum.unique
class Flip(enum.IntEnum):

    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2


@enum.unique
class Scancode(enum.IntEnum):

    X = 27
    Y = 28
    Z = 29
    RIGHT = 79
    LEFT = 80


def load_first_available(library_paths: List[str]) -> ctypes.CDLL:
    for path in library_paths:
        with contextlib.suppress(OSError):
            libsdl2 = ctypes.CDLL(path)
            if libsdl2:
                return libsdl2

    raise LibraryNotFound(library_paths)


def load_libsdl2() -> ctypes.CDLL:
    return load_first_available(['libSDL2-2.0.so', 'SDL2'])


def load_libsdl2_image() -> ctypes.CDLL:
    return load_first_available(['libSDL2_image-2.0.so', 'SDL2_image'])


libsdl2 = load_libsdl2()
libsdl2_image = load_libsdl2_image()


libsdl2.SDL_GetError.restype = ctypes.c_char_p
libsdl2.SDL_GetKeyboardState.restype = ctypes.POINTER(ctypes.c_uint8)


def quit_requested() -> bool:
    libsdl2.SDL_PumpEvents()
    return bool(libsdl2.SDL_PeepEvents(None, 0,
                                       EventAction.PEEK_EVENT,
                                       Event.QUIT, Event.QUIT))


class Error(BaseException):

    def __init__(self) -> None:
        super().__init__(libsdl2.SDL_GetError())


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
        class SdlRect(ctypes.Structure):

            _fields_ = [('x', ctypes.c_int),
                        ('y', ctypes.c_int),
                        ('w', ctypes.c_int),
                        ('h', ctypes.c_int)]

        return SdlRect(self.x, self.y, self.width, self.height)


class Window(contextlib.AbstractContextManager):

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


class Renderer(contextlib.AbstractContextManager):

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
                                      ctypes.byref(r._as_parameter_)) < 0:
            raise Error

    @property
    def draw_color(self) -> Color:
        r = ctypes.c_int()
        g = ctypes.c_int()
        b = ctypes.c_int()
        a = ctypes.c_int()

        if libsdl2.SDL_GetRenderDrawColor(self.sdl_renderer,
                                          ctypes.byref(r),
                                          ctypes.byref(g),
                                          ctypes.byref(b),
                                          ctypes.byref(a)) < 0:
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
                       dst: Rectangle,
                       flip: Flip=Flip.NONE) -> None:
        if libsdl2.SDL_RenderCopyEx(self.sdl_renderer,
                                    texture.sdl_texture,
                                    ctypes.byref(src._as_parameter_),
                                    ctypes.byref(dst._as_parameter_),
                                    ctypes.c_double(0),
                                    None,
                                    flip) < 0:
            raise Error


class Texture(contextlib.AbstractContextManager):

    def __init__(self, renderer: Renderer, path: bytes) -> None:
        self.sdl_texture = libsdl2_image.IMG_LoadTexture(renderer.sdl_renderer,
                                                         path)

        if not self.sdl_texture:
            raise Error

    @property
    def height(self) -> int:
        h = ctypes.c_int(0)
        if libsdl2.SDL_QueryTexture(self.sdl_texture,
                                    None, None,
                                    None, ctypes.byref(h)) < 0:
            raise Error

        return h.value

    @property
    def width(self) -> int:
        w = ctypes.c_int(0)
        if libsdl2.SDL_QueryTexture(self.sdl_texture,
                                    None, None,
                                    ctypes.byref(w), None) < 0:
            raise Error

        return w.value

    @property
    def dimensions(self) -> Dimensions:
        return Dimensions(self.width, self.height)

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        libsdl2.SDL_DestroyTexture(self.sdl_texture)


class Keyboard:

    def __init__(self) -> None:  # TODO This doesn't work
        self.keyboard_ptr = libsdl2.SDL_GetKeyboardState(None)

    def key_down(self, scancode: Scancode) -> bool:
        return bool(self.keyboard_ptr[scancode])
