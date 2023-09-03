import typer
from PIL import Image, ImageDraw
from loguru import logger


def typer_main():
    typer.run(remove_empty_space)


def remove_empty_space(
    source_path: str = typer.Argument(),
    target_path: str = typer.Argument(default='', help='path to cropped file. If not specefied - original will be replaced'),
):
    """Remove empty area in image."""
    img = Image.open(source_path)
    px = img.load()
    cropped = img.copy()

    empty_lines = count_empty_lines(px, img.width, img.height)
    img_box = (0, 0, img.width, img.height - empty_lines)
    not_empty_region = img.crop(img_box)

    # clear image
    draw = ImageDraw.Draw(cropped)
    draw.rectangle((0, 0, img.width, img.height), fill=(0, 0, 0, 0))
    # paste not empty
    cropped.paste(not_empty_region, box=(0, empty_lines, img.width, img.height))
    if target_path:
        logger.success(f'cropped image saved to: {target_path}')
        cropped.save(target_path)
    else:
        logger.success('original file replaced with cropped version')
        cropped.save(source_path)


def count_empty_lines(pixel_access, img_width, img_height):
    ans = 0
    for line_idx in range(img_height):
        current_line = img_height - line_idx - 1
        for column_idx in range(img_width):
            pixel = pixel_access[current_line, column_idx]
            if pixel != (0, 0, 0, 0):
                return ans
        ans += 1

    return ans


if __name__ == '__main__':
    typer.run(typer)
