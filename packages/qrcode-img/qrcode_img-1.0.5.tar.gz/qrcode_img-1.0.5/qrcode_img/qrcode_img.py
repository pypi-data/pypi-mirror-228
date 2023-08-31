from io import BytesIO

import qrcode
from path import Path
from PIL import Image, ImageDraw


class QRCode:
    BLACK_LINE = (0, 0, 0, 230)
    WHITE_LINE_BEFORE = (255, 255, 255, 50)
    WHITE_LINE_AFTER = (255, 255, 255, 230)

    def __init__(self, text: str, coeff: int = 10) -> None:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data(text)
        qr.make(fit=True)
        self.__img = qr.get_matrix()
        self.__coeff = coeff
        self.__coeff_small = round(self.__coeff / 3)
        self.__length_qr = len(self.__img) * self.__coeff
        self.__back_im = Image.new(
            "RGBA", (self.__length_qr, self.__length_qr), (0, 0, 0, 0)
        )
        self.__idraw = ImageDraw.Draw(self.__back_im, "RGBA")
        self.__bytes_io = BytesIO()
        self.__background = None

    def save_qr_code(self, path_to_save: Path = None) -> bool:
        if self.__background is None:
            return False
        self.__background.save(path_to_save)
        return True

    def gen_qr_code(self, path_to_download: Path) -> BytesIO | None:
        try:
            self.__background = (
                Image.open(path_to_download)
                .resize((self.__length_qr, self.__length_qr))
                .convert("RGBA")
            )
        except:
            return None

        self.__background = self.__get_qr_code_with_img(self.__background)

        self.__background.save(self.__bytes_io, format="PNG")
        return self.__bytes_io

    def __get_qr_code_with_img(self, background):
        x = 0
        y = 0
        for string in self.__img:
            for i in string:
                fill = self.BLACK_LINE if i else self.WHITE_LINE_AFTER
                self.__idraw.rectangle(
                    (
                        x + self.__coeff_small,
                        y + self.__coeff_small,
                        x + self.__coeff - self.__coeff_small,
                        y + self.__coeff - self.__coeff_small,
                    ),
                    fill=fill,
                )
                x += self.__coeff
            x = 0
            y += self.__coeff

        operations = (
            (
                (0, 0, self.__coeff * 9, self.__coeff * 9),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 9,
                    0,
                    self.__length_qr,
                    self.__coeff * 9,
                ),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (
                    0,
                    self.__length_qr - self.__coeff * 9,
                    self.__coeff * 9,
                    self.__length_qr,
                ),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 9,
                    self.__length_qr - self.__coeff * 6,
                    self.__length_qr - self.__coeff * 6,
                ),
                self.WHITE_LINE_BEFORE,
            ),
            (
                (self.__coeff, self.__coeff, self.__coeff * 8, self.__coeff * 2),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff,
                    self.__length_qr - self.__coeff,
                    self.__coeff * 2,
                ),
                self.BLACK_LINE,
            ),
            (
                (self.__coeff, self.__coeff * 7, self.__coeff * 8, self.__coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff * 7,
                    self.__length_qr - self.__coeff,
                    self.__coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff,
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff * 8,
                    self.__length_qr - self.__coeff * 7,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff,
                    self.__length_qr - self.__coeff * 2,
                    self.__coeff * 8,
                    self.__length_qr - self.__coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 8,
                    self.__length_qr - self.__coeff * 8,
                    self.__length_qr - self.__coeff * 7,
                    self.__length_qr - self.__coeff * 7,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff * 3,
                    self.__coeff * 3,
                    self.__coeff * 6,
                    self.__coeff * 6,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 6,
                    self.__coeff * 3,
                    self.__length_qr - self.__coeff * 3,
                    self.__coeff * 6,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff * 3,
                    self.__length_qr - self.__coeff * 6,
                    self.__coeff * 6,
                    self.__length_qr - self.__coeff * 3,
                ),
                self.BLACK_LINE,
            ),
            (
                (self.__coeff, self.__coeff, self.__coeff * 2, self.__coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (self.__coeff * 7, self.__coeff, self.__coeff * 8, self.__coeff * 8),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 2,
                    self.__coeff,
                    self.__length_qr - self.__coeff,
                    self.__coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff,
                    self.__length_qr - self.__coeff * 7,
                    self.__coeff * 8,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff,
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff * 2,
                    self.__length_qr - self.__coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__coeff * 7,
                    self.__length_qr - self.__coeff * 8,
                    self.__coeff * 8,
                    self.__length_qr - self.__coeff,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 9,
                    self.__length_qr - self.__coeff * 5,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 6,
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 5,
                    self.__length_qr - self.__coeff * 5,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 6,
                    self.__length_qr - self.__coeff * 9,
                ),
                self.BLACK_LINE,
            ),
            (
                (
                    self.__length_qr - self.__coeff * 10,
                    self.__length_qr - self.__coeff * 6,
                    self.__length_qr - self.__coeff * 6,
                    self.__length_qr - self.__coeff * 5,
                ),
                self.BLACK_LINE,
            ),
        )

        for xy, fill in operations:
            self.__idraw.rectangle(
                xy,
                fill=fill,
            )

        background.paste(self.__back_im, (0, 0), self.__back_im)
        return background
