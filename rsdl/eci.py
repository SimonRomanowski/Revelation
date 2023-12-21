from rpython.translator.tool.cbuild import ExternalCompilationInfo
from rpython.translator.platform import CompilationError
import py
import sys
import os

def get_rsdl_compilation_info():
    def ifndef(symbol, alt):
        return """
#ifndef %s
#define %s %s
#endif
        """ % (symbol, symbol, alt)

    if sys.platform == 'darwin' and 'SDL_PREFIX' not in os.environ:
        # Use SDL2.framework
        eci = ExternalCompilationInfo(
            includes = ['SDL2/SDL.h'],
            pre_include_bits=['#define SDL_MAIN_HANDLED'],
            frameworks = ['SDL2', 'Cocoa']
        )
    elif sys.platform == "win32":
        try:
            sdl_prefix = os.path.abspath(os.environ["SDL_PREFIX"])
        except KeyError:
            print "You need to provide the path to SDL using the SDL_PREFIX environment variable"
            exit(1)

        eci = ExternalCompilationInfo(
            includes = ['SDL.h'],
            include_dirs = [os.path.join(sdl_prefix, "include")],
            pre_include_bits=['#define SDL_MAIN_HANDLED'],
            link_files = [
                os.path.join(sdl_prefix, "lib", "x64", "SDL2main.lib"),
                os.path.join(sdl_prefix, "lib", "x64", "SDL2.lib")
            ],
            libraries = ["SDL2"],
            library_dirs = [os.path.join(sdl_prefix, "lib", "x64")],
        )
    else:
        config_tool = "sdl2-config"
        try:
            config_tool = os.path.abspath(os.path.join(
                os.path.abspath(os.environ["SDL_PREFIX"]),
                'bin',
                config_tool))
        except KeyError:
            pass
        eci = ExternalCompilationInfo(
            includes=['SDL.h'],
            post_include_bits=[
                "\n".join([
                    ifndef("SDL_HINT_VIDEO_X11_NET_WM_PING", '"0"'),
                    ifndef("SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK", '"0"'),
                    ifndef("SDL_RENDER_TARGETS_RESET", "SDL_LASTEVENT"),
                    ifndef("SDL_RENDER_DEVICE_RESET", "SDL_LASTEVENT"),
                    ifndef("SDL_MOUSEWHEEL_FLIPPED", "0"),
                    ifndef("SDL_MOUSEWHEEL_NORMAL", "0"),
                    ifndef("SDL_WINDOW_ALLOW_HIGHDPI", "0"),
                    ifndef("SDL_WINDOWEVENT_SIZE_CHANGED", "SDL_LASTEVENT"),
                ])
            ]
        )
        eci = eci.merge(ExternalCompilationInfo.from_config_tool(config_tool))
    return eci

def check_sdl_installation():
    from rpython.rtyper.tool import rffi_platform as platform
    platform.verify_eci(get_rsdl_compilation_info())

SDLNotInstalled = (ImportError, CompilationError)
