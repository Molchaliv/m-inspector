from PIL import Image, ImageQt

from PySide6.QtGui import QPixmap


def place_pixmap(image: Image.Image | str, size: tuple[int, int]) -> tuple[QPixmap, tuple[int, int]]:
    if isinstance(image, Image.Image):
        copy = image.copy()
    else:
        copy = Image.open(image)
    orig_size = copy.size
    copy.thumbnail(size, Image.LANCZOS)

    return QPixmap(ImageQt.ImageQt(copy)), orig_size
