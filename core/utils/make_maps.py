from PIL import Image


def make_maps(path: str, chunk_size: tuple[int, int], image_size: tuple[int, int] = None,
              background: tuple[int, int, int] = (255, 0, 255), output: str | None = ".\\output") -> Image.Image:

    image = Image.open(path)

    if image_size is None:
        image_size = image.size

    image = image.resize(image_size)

    rows = (image_size[0] / chunk_size[0])
    columns = (image_size[1] / chunk_size[1])

    if rows.is_integer():
        rows = int(rows)
    else:
        rows = int(rows) + 1

    if columns.is_integer():
        columns = int(columns)
    else:
        columns = int(columns) + 1

    width = rows * chunk_size[0]
    height = columns * chunk_size[1]

    background = Image.new("RGBA", (width, height), background)

    background.paste(image, (
        (background.width // 2) - (image.width // 2),
        (background.height // 2) - (image.height // 2))
    )

    if output is None:
        return background

    for x in range(0, rows):
        for y in range(0, columns):
            cropped = background.crop(
                (x * chunk_size[0], y * chunk_size[1], (x + 1) * chunk_size[0], (y + 1) * chunk_size[1])
            )
            cropped.save(f"{output}\\{x}_{y}.png")

    return background
