from rpython.rtyper.lltypesystem import lltype, rffi
from rpython.rtyper.tool import rffi_platform as platform
from .constants import int_constants, str_constants
from .eci import get_rsdl_compilation_info
from rpython.rlib.objectmodel import we_are_translated
import py
import sys

# ------------------------------------------------------------------------------

eci = get_rsdl_compilation_info()

def external(name, args, result):
    return rffi.llexternal(name, args, result, compilation_info=eci)

# ------------------------------------------------------------------------------

RectPtr             = lltype.Ptr(lltype.ForwardReference())
WindowPtr           = rffi.COpaquePtr('SDL_Window')
RendererPtr         = rffi.COpaquePtr('SDL_Renderer')
TexturePtr          = rffi.COpaquePtr('SDL_Texture')
SurfacePtr          = lltype.Ptr(lltype.ForwardReference())
CursorPtr           = rffi.COpaquePtr('SDL_Cursor')
PixelFormatPtr      = lltype.Ptr(lltype.ForwardReference())
ColorPtr            = lltype.Ptr(lltype.ForwardReference())
PalettePtr          = lltype.Ptr(lltype.ForwardReference())
EventPtr            = lltype.Ptr(lltype.ForwardReference())
EventPtrs           = lltype.Ptr(lltype.Array(EventPtr, hints={'nolength': True}))
KeyboardEventPtr    = lltype.Ptr(lltype.ForwardReference())
TextInputEventPtr   = lltype.Ptr(lltype.ForwardReference())
MouseButtonEventPtr = lltype.Ptr(lltype.ForwardReference())
MouseMotionEventPtr = lltype.Ptr(lltype.ForwardReference())
MouseWheelEventPtr  = lltype.Ptr(lltype.ForwardReference())
WindowEventPtr      = lltype.Ptr(lltype.ForwardReference())
DropEventPtr        = lltype.Ptr(lltype.ForwardReference())
KeyPtr              = lltype.Ptr(lltype.ForwardReference())
RWopsPtr            = lltype.Ptr(lltype.ForwardReference())

# ------------------------------------------------------------------------------

class CConstants:
    _compilation_info_ = eci

def _populate_constants_configuration():
    def add_int(prefix, name):
        setattr(CConstants, name, platform.ConstantInteger(prefix+name))
    def add_cchar(prefix, name):
        setattr(CConstants, name, platform.DefinedConstantString(prefix+name))
    def add(_constants, func):
        for prefix, list in _constants.items():
            for name_or_dict in list:
                if type(name_or_dict) == dict:
                    for path, names in name_or_dict.items():
                        for name in names:
                            func(prefix, name)
                else:
                    func(prefix, name_or_dict)
    add(int_constants, add_int)
    add(str_constants, add_cchar)

_populate_constants_configuration()
globals().update(platform.configure(CConstants))
del _populate_constants_configuration  # hide it from RPython runtime code

# ------------------------------------------------------------------------------

class CConfig:
    _compilation_info_ = eci

    Uint8  = platform.SimpleType('Uint8',  rffi.UINT)
    Uint16 = platform.SimpleType('Uint16', rffi.UINT)
    Sint16 = platform.SimpleType('Sint16', rffi.INT)
    Uint32 = platform.SimpleType('Uint32', rffi.UINT)

    Rect             = platform.Struct('SDL_Rect',
                                    [('x', rffi.INT),
                                     ('y', rffi.INT),
                                     ('w', rffi.INT),
                                     ('h', rffi.INT)])

    Surface          = platform.Struct('SDL_Surface',
                                    [('w', rffi.INT),
                                     ('h', rffi.INT),
                                     ('format', PixelFormatPtr),
                                     ('pitch', rffi.INT),
                                     ('pixels', rffi.VOIDP)])

    PixelFormat      = platform.Struct('SDL_PixelFormat',
                                    [('format', rffi.INT),
                                     ('palette', PalettePtr),
                                     ('BitsPerPixel', rffi.INT),
                                     ('BytesPerPixel', rffi.INT),
                                     ('Rmask', rffi.INT),
                                     ('Gmask', rffi.INT),
                                     ('Bmask', rffi.INT),
                                     ('Amask', rffi.INT)])

    Color            = platform.Struct('SDL_Color',
                                     [('r', rffi.INT),
                                     ('g', rffi.INT),
                                     ('b', rffi.INT),
                                     ('a', rffi.INT)])

    Palette          = platform.Struct('SDL_Palette',
                                     [('ncolors', rffi.INT),
                                      ('colors', ColorPtr)])

    Event            = platform.Struct('SDL_Event',
                                    [('type', rffi.UINT)])

    Keysym           = platform.Struct('SDL_Keysym',
                                    [('scancode', rffi.INT),
                                     ('sym', rffi.INT),
                                     ('mod', rffi.INT)])

    KeyboardEvent    = platform.Struct('SDL_KeyboardEvent',
                                    [('type', rffi.UINT),
                                     ('state', rffi.INT),
                                     ('keysym', Keysym)])

    TextInputEvent   = platform.Struct('SDL_TextInputEvent',
                                    [('type', rffi.UINT),
                                     ('timestamp', rffi.INT),
                                     ('windowID', rffi.INT),
                                     ('text', rffi.CFixedArray(rffi.CHAR, TEXTINPUTEVENT_TEXT_SIZE))])

    MouseButtonEvent = platform.Struct('SDL_MouseButtonEvent',
                                    [('type', rffi.UINT),
                                     ('button', rffi.INT),
                                     ('state', rffi.INT),
                                     ('x', rffi.INT),
                                     ('y', rffi.INT)])

    MouseMotionEvent = platform.Struct('SDL_MouseMotionEvent',
                                    [('type', rffi.UINT),
                                     ('state', rffi.INT),
                                     ('x', rffi.INT),
                                     ('y', rffi.INT),
                                     ('xrel', rffi.INT),
                                     ('yrel', rffi.INT)])

    MouseWheelEvent  = platform.Struct('SDL_MouseWheelEvent',
                                    [('type', rffi.UINT),
                                     ('timestamp', rffi.UINT),
                                     ('windowID', rffi.UINT),
                                     ('which', rffi.UINT),
                                     ('x', rffi.INT),
                                     ('y', rffi.INT),
                                     # SDL >= 2.0.4 ('flipped', rffi.UINT)
                                    ])

    WindowEvent      = platform.Struct('SDL_WindowEvent',
                                    [('type', rffi.UINT),
                                     ('windowID', rffi.UINT),
                                     ('event', rffi.UINT),
                                     ('data1', rffi.INT),
                                     ('data2', rffi.INT)])

    DropEvent        = platform.Struct('SDL_DropEvent',
                                    [('type', rffi.UINT),
                                     ('timestamp', rffi.UINT),
                                     ('file', rffi.CCHARP)])

    QuitEvent        = platform.Struct('SDL_QuitEvent',
                                    [('type', rffi.UINT)])

    RWops = platform.Struct('SDL_RWops', [])

# ------------------------------------------------------------------------------

globals().update(platform.configure(CConfig))

# ------------------------------------------------------------------------------
# make constant number types compatible with their target fields

def _cast_constants():
    import sys
    RSDL = sys.modules[__name__]
    for prefix, list in int_constants.items():
        for name_or_dict in list:
            if type(name_or_dict) == str:
                continue
            for path, names in name_or_dict.items():
                member = RSDL
                for fragment in path:
                    if hasattr(member, 'c_' + fragment):
                        member = getattr(member, 'c_' + fragment)
                    else:
                        member = getattr(member, fragment)
                for name in names:
                    current_value = getattr(RSDL, name)
                    casted_value = rffi.cast(member, current_value)
                    setattr(RSDL, name, casted_value)

_cast_constants()
del _cast_constants  # hide it from RPython runtime code

# ------------------------------------------------------------------------------

RectPtr.TO.become(Rect)
SurfacePtr.TO.become(Surface)
PixelFormatPtr.TO.become(PixelFormat)
ColorPtr.TO.become(Color)
PalettePtr.TO.become(Palette)
EventPtr.TO.become(Event)
KeyboardEventPtr.TO.become(KeyboardEvent)
TextInputEventPtr.TO.become(TextInputEvent)
MouseButtonEventPtr.TO.become(MouseButtonEvent)
MouseMotionEventPtr.TO.become(MouseMotionEvent)
MouseWheelEventPtr.TO.become(MouseWheelEvent)
WindowEventPtr.TO.become(WindowEvent)
DropEventPtr.TO.become(DropEvent)
RWopsPtr.TO.become(RWops)

# ------------------------------------------------------------------------------

Uint8P  = lltype.Ptr(lltype.Array(Uint8, hints={'nolength': True}))
Uint16P = lltype.Ptr(lltype.Array(Uint16, hints={'nolength': True}))
# need to add signed hint here
Sint16P = lltype.Ptr(lltype.Array(Sint16, hints={'nolength': True}))
Uint32P = lltype.Ptr(lltype.Array(Uint32, hints={'nolength': True}))

# ------------------------------------------------------------------------------

_Init            = external('SDL_Init',
                             [Uint32],
                             rffi.INT)

SetMainReady     = external('SDL_SetMainReady', [],
                            lltype.Void)

def Init(flags):
    SetMainReady()
    return _Init(flags)

Quit             = external('SDL_Quit', [],
                            lltype.Void)

CreateWindow     = external('SDL_CreateWindow',
                             [rffi.CCHARP, rffi.INT, rffi.INT, rffi.INT,
                                 rffi.INT, Uint32],
                             WindowPtr)

# Rom; Added function
DestroyWindow = external("SDL_DestroyWindow", [WindowPtr], lltype.Void)

SetWindowTitle   = external('SDL_SetWindowTitle',
                            [WindowPtr, rffi.CCHARP],
                            lltype.Void)

SetWindowFullscreen = external('SDL_SetWindowFullscreen',
                               [WindowPtr, rffi.INT],
                               rffi.INT)

# Rom; Added function
SetWindowSize = external("SDL_SetWindowSize",
                         [WindowPtr, rffi.INT, rffi.INT],
                         lltype.Void)

CreateRenderer   = external('SDL_CreateRenderer',
                             [WindowPtr, rffi.INT, Uint32],
                             RendererPtr)

SetRenderDrawColor = external('SDL_SetRenderDrawColor',
                              [RendererPtr, Uint8, Uint8, Uint8, Uint8],
                              rffi.INT)

RenderFillRect   = external('SDL_RenderFillRect',
                            [RendererPtr, RectPtr],
                            rffi.INT)

RenderCopy       = external('SDL_RenderCopy',
                            [RendererPtr, TexturePtr, RectPtr, RectPtr],
                            rffi.INT)

RenderClear      = external('SDL_RenderClear', [RendererPtr], lltype.Void)

RenderPresent    = external('SDL_RenderPresent',
                            [RendererPtr],
                            lltype.Void)

# Rom; Added function
DestroyRenderer = external("SDL_DestroyRenderer", [RendererPtr], lltype.Void)

# Rom; Added function
RenderSetLogicalSize = external("SDL_RenderSetLogicalSize",
                                [RendererPtr, rffi.INT, rffi.INT],
                                rffi.INT)

# Rendering API

CreateTexture    = external('SDL_CreateTexture',
                             [RendererPtr, Uint32, rffi.INT, rffi.INT, rffi.INT],
                             TexturePtr)

DestroyTexture   = external('SDL_DestroyTexture', [TexturePtr], lltype.Void)

UpdateTexture    = external('SDL_UpdateTexture',
                             [TexturePtr, RectPtr, rffi.VOIDP, rffi.INT],
                             rffi.INT)

LockTexture      = external('SDL_LockTexture',
                            [TexturePtr, RectPtr, rffi.VOIDPP, rffi.INTP],
                            rffi.INT)

UnlockTexture    = external('SDL_UnlockTexture',
                            [TexturePtr],
                            lltype.Void)

# Rom; Added function
SetTextureBlendMode = external("SDL_SetTextureBlendMode",
                               [TexturePtr, rffi.INT],
                               rffi.INT)

SetHint          = external('SDL_SetHint',
                            [rffi.CCHARP, rffi.CCHARP],
                            rffi.INT)
SetSwapInterval  = external('SDL_GL_SetSwapInterval',
                            [rffi.INT],
                            rffi.INT)

# Events API

EventState       = external('SDL_EventState',
                            [Uint32, rffi.INT],
                            Uint8)

WaitEvent        = external('SDL_WaitEvent',
                             [EventPtr],
                             rffi.INT)

PollEvent        = external('SDL_PollEvent',
                             [EventPtr],
                             rffi.INT)

GetModState      = external('SDL_GetModState',
                            [],
                            rffi.INT)

PeepEvents       =  external('SDL_PeepEvents',
                            [EventPtrs, rffi.INT, rffi.INT, Uint32],
                            rffi.INT)

PumpEvents       =  external('SDL_PumpEvents',
                            [],
                            lltype.Void)

StartTextInput   = external('SDL_StartTextInput', [], lltype.Void)

StopTextInput    = external('SDL_StopTextInput', [], lltype.Void)

ShowCursor       = external('SDL_ShowCursor', [rffi.INT], rffi.INT)

CreateCursor     = external('SDL_CreateCursor',
                            [Uint8P, Uint8P,
                             rffi.INT, rffi.INT,
                             rffi.INT, rffi.INT],
                            CursorPtr)

SetCursor       = external('SDL_SetCursor', [CursorPtr], lltype.Void)

FreeCursor       = external('SDL_FreeCursor', [CursorPtr], lltype.Void)

Flip             = external('SDL_Flip',
                             [SurfacePtr],
                             rffi.INT)

GetClipboardText = external('SDL_GetClipboardText',
                            [],
                            rffi.CCHARP)
SetClipboardText = external('SDL_SetClipboardText',
                            [rffi.CCHARP],
                            rffi.INT)
HasClipboardText = external('SDL_HasClipboardText',
                            [],
                            rffi.INT)

# Surface API

CreateRGBSurface = external('SDL_CreateRGBSurface',
                             [Uint32, rffi.INT, rffi.INT, rffi.INT,
                              Uint32, Uint32, Uint32, Uint32],
                             SurfacePtr)

CreateRGBSurfaceFrom = external('SDL_CreateRGBSurfaceFrom',
                                [rffi.VOIDP, rffi.INT, rffi.INT, rffi.INT, rffi.INT,
                                 Uint32, Uint32, Uint32, Uint32],
                                SurfacePtr)

LockSurface      = external('SDL_LockSurface',
                             [SurfacePtr],
                             rffi.INT)

UnlockSurface    = external('SDL_UnlockSurface',
                             [SurfacePtr],
                             lltype.Void)

FreeSurface      = external('SDL_FreeSurface',
                             [SurfacePtr],
                             lltype.Void)

SetSurfaceAlphaMod = external('SDL_SetSurfaceAlphaMod',
                             [SurfacePtr, Uint8],
                             rffi.INT)

SetSurfaceBlendMode = external('SDL_SetSurfaceBlendMode',
                             [SurfacePtr, rffi.INT],
                             rffi.INT)

FillRect         = external('SDL_FillRect',
                             [SurfacePtr, RectPtr, Uint32],
                             rffi.INT)

BlitSurface      = external('SDL_UpperBlit',
                             [SurfacePtr, RectPtr, SurfacePtr,  RectPtr],
                             rffi.INT)

SetColorKey      = external('SDL_SetColorKey',
                            [SurfacePtr, Uint32, Uint32],
                            rffi.INT)

SetPaletteColors = external('SDL_SetPaletteColors',
                            [PalettePtr, ColorPtr, rffi.INT, rffi.INT],
                            rffi.INT)

GetTicks         = external('SDL_GetTicks',
                            [],
                            Uint32)

Delay            = external('SDL_Delay',
                            [Uint32],
                            lltype.Void)

UpdateRect       = external('SDL_UpdateRect',
                            [SurfacePtr, rffi.INT, rffi.INT, rffi.INT],
                            lltype.Void)

# PixelFormats API

AllocFormat      = external('SDL_AllocFormat', [Uint32], PixelFormatPtr)

FreeFormat       = external('SDL_FreeFormat', [PixelFormatPtr], lltype.Void)

MapRGB           = external('SDL_MapRGB',
                             [PixelFormatPtr, Uint8, Uint8,  Uint8],
                             Uint32)

GetRGB           = external('SDL_GetRGB',
                             [Uint32, PixelFormatPtr, Uint8P, Uint8P, Uint8P],
                             lltype.Void)

GetRGBA          = external('SDL_GetRGBA',
                             [Uint32, PixelFormatPtr, Uint8P, Uint8P,
                             Uint8P, Uint8P],
                             lltype.Void)

GetKeyName       = external('SDL_GetKeyName',
                            [rffi.INT],
                            rffi.CCHARP)

# Rect API

UnionRect        = external('SDL_UnionRect',
                            [RectPtr, RectPtr, RectPtr],
                            lltype.Void)

IntersectRect    = external('SDL_IntersectRect',
                            [RectPtr, RectPtr, RectPtr],
                            rffi.INT)

# Miscellaneous

_GetError        = external('SDL_GetError',
                            [],
                            rffi.CCHARP)

def GetError():
    return rffi.charp2str(_GetError())

RWFromFile       = external('SDL_RWFromFile',
                            [rffi.CCHARP, rffi.CCHARP],
                            RWopsPtr)

# ------------------------------------------------------------------------------
