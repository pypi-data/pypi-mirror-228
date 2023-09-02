from pygame.color import Color
import glob
from pathlib import Path

import pygame
from pygame import Surface

from robingame.utils import limit_value


def init_display() -> Surface:
    """
    Make sure the pygame display is initialised (required for loading images).
    If the display already exists, return it. If not, generate a new 1x1 pixel display.

    Returns:
        the pygame display
    """
    if not pygame.display.get_init():
        pygame.display.init()
        return pygame.display.set_mode((1, 1))
    else:
        return pygame.display.get_surface()


def load_image(filename: str | Path, colorkey: Color | int = None) -> Surface:
    """
    Load an image. Abstracts away some of the pygame pitfalls.

    Args:
        filename: path to the image file
        colorkey: sets the color to treat as transparent (like the green in greenscreen).
            if `-1` is passed, then the color of the top-left pixel will be used.

    Returns:
        the loaded image
    """
    init_display()
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        print("Unable to load image:", filename)
        raise

    # colorkey needs to be set before .convert_alpha() is called, because Surfaces with a
    # per-pixel transparency (i.e. after convert_alpha) ignore colorkey.
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    image = image.convert_alpha()
    return image


def not_empty(surface: Surface) -> bool:
    """
    Check if a surface has any non-zero pixels. `Surface.get_bounding_rect()` returns the
    smallest rectangle on the surface containing data. If the surface is empty, it will return
    Rect(0, 0, 0, 0), for which `any` returns False.
    """
    return any(surface.get_bounding_rect())


def empty_image(*args, **kwargs) -> Surface:
    """
    Generate an empty Surface with `.convert_alpha()` already called.

    Returns:
        an empty Surface
    """
    img = Surface(*args, **kwargs).convert_alpha()
    img.fill((0, 0, 0, 0))
    return img


def relative_folder(current_file: str, folder: str) -> Path:
    return Path(current_file).parent.absolute() / folder


def pad_alpha(colour_tuple: Color | tuple) -> Color:
    """
    Add the 4th (alpha) channel to a length 3 color tuple.
    By default it sets the new alpha channel to full opacity (255).

    Args:
        colour_tuple:

    Returns:
        a colour
    """
    if len(colour_tuple) == 3:
        # if no alpha channel supplied, assume it's full opacity
        return (*colour_tuple, 255)
    elif len(colour_tuple) == 4:
        return colour_tuple
    else:
        raise Exception("bogus colour, man")


def brighten_color(color: Color | tuple, amount: int) -> Color:
    """
    Increase all channels to brighten a colour.
    Does not allow values greater than 255.

    Args:
        color: the input colour
        amount: how much to increase each channel

    Returns:
        the output colour
    """
    color = Color(color)
    r = limit_value(color.r + amount, between=(0, 255))
    g = limit_value(color.g + amount, between=(0, 255))
    b = limit_value(color.b + amount, between=(0, 255))
    return Color(r, g, b, color.a)


def brighten(image: Surface, amount: int):
    """
    Use `brighten_color` to brighten all pixels in an image by `amount`. \

    Args:
        image: the input image
        amount: how much to increase brightness
    """
    width, height = image.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_image = image.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = image.get_at((x, y))[:]
            new_color = brighten_color(color, amount)
            if new_color:
                new_image.set_at((x, y), pygame.Color(*new_color))
            else:
                new_image.set_at((x, y), pygame.Color(*color))

    return new_image


def scale_image(image: Surface, scale: float) -> Surface:
    """
    Return a scaled copy of an image.

    Args:
        image: input image
        scale: factor by which to scale image

    Returns:
        output image
    """
    width, height = image.get_rect().size
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image


def scale_images(images: [Surface], scale: float) -> [Surface]:
    """
    Apply `scale_image` to a list of images.
    """
    return [scale_image(image, scale) for image in images]


def flip_image(image: Surface, flip_x: bool = False, flip_y: bool = False) -> Surface:
    """
    Return a flipped copy of an image.

    Args:
        image: input image
        flip_x: flip horizontally
        flip_y: flip vertically

    Returns:
        output image
    """
    return pygame.transform.flip(image, bool(flip_x), bool(flip_y))


def flip_images(images: [Surface], flip_x: bool = False, flip_y: bool = False):
    """
    Apply `flip_image` to a list of images.
    """
    return [flip_image(image, flip_x, flip_y) for image in images]


def recolor_image(surface: Surface, color_mapping: dict) -> Surface:
    """
    Return a recolored copy of an image.

    Args:
        surface: input image
        color_mapping: dictionary of old colors (keys) to new colors (values).
            Unfortunately they have to be RGB tuples, not pygame Colors, because Color is an
            unhashable type...

    Returns:
        output image
    """
    # make sure the colourmap has alpha channel on all colours
    color_mapping = {pad_alpha(k): pad_alpha(v) for k, v in color_mapping.items()}
    width, height = surface.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_surface = surface.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = surface.get_at((x, y))[:]
            new_color = color_mapping.get(color)
            if new_color:
                new_surface.set_at((x, y), pygame.Color(*new_color))
            else:
                new_surface.set_at((x, y), pygame.Color(*color))

    return new_surface


def recolor_images(images: [Surface], colormap: dict) -> [Surface]:
    """
    Apply `recolor_image` to a list of images.
    """
    return [recolor_image(image, colormap) for image in images]


def load_spritesheet(
    filename: Path | str,
    image_size: (int, int) = None,
    colorkey: Color = None,
    num_images: int = 0,
) -> [Surface]:
    """
    Load the image file. Don't call this until pygame.display has been initiated. Split the
    spritesheet into images and return a list of images.

    If image_size is None, load the whole spritesheet as one sprite.

    Args:
        filename: path to the spritesheet file
        image_size: size of the individual frames of the spritesheet (in pixels)
        colorkey: used to set transparency (see `load_image`)
        num_images: can be used to limit the number of frames loaded (default = load all)

    Returns:
        a list of images
    """
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"Couldn't find {filename}")
    sheet = load_image(filename=filename.as_posix(), colorkey=colorkey)

    if image_size:
        width, height = image_size
        num_horizontal = sheet.get_rect().width // width
        num_vertical = sheet.get_rect().height // height
        rects = [
            pygame.Rect((width * i, height * j, width, height))
            for j in range(num_vertical)
            for i in range(num_horizontal)
        ]
        images = [sheet.subsurface(rect) for rect in rects]
        images = list(filter(not_empty, images))
        if num_images:
            images = images[:num_images]
    else:
        images = [sheet]
    return images


def load_image_sequence(
    pattern: Path | str,
    colorkey: Color = None,
    num_images: int = 0,
) -> [Surface]:
    """
    Load a sequence of images.

    Args:
        pattern: glob pattern for the image sequence. E.g. if your folder of image contains
            `"example1.png", "example2.png"`, etc, then your pattern should be `"example*.png"`
        colorkey: used to recolor images (see `load_image`)
        num_images: used to limit how many images are loaded (default = load all images that
            match the pattern)

    Returns:
        a list of images
    """
    pattern = Path(pattern).as_posix()
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"Couldn't find any images matching pattern '{pattern}'")
    images = [load_image(file, colorkey) for file in files]
    if num_images:
        images = images[:num_images]
    return images
