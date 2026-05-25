from PIL import Image, ImageSequence
from rpa_pdf.converters.base import BaseConverter


class ImageConverter(BaseConverter):
    def convert(self, input_file_path: str, output_file_path: str | None = None) -> None:
        try:
            image = Image.open(input_file_path)

            images = []
            for page in ImageSequence.Iterator(image):
                page = page.convert("RGB")
                images.append(page)
            if len(images) == 1:
                images[0].save(output_file_path)
            else:
                images[0].save(output_file_path, save_all=True, append_images=images[1:])

        except Exception as ex:
            raise ex
