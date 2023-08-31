## Генерация QR Code по картинке

### https://pypi.org/project/qrcode-img/

 
## Пример работы

```
from path import Path
from qrcode_img import QRCode

text = 'Hello'

path_to_download = Path().joinpath("example", "11.png")
path_to_save = Path().joinpath("example", "1example.png")


qrcode = QRCode(text)

qrcode.gen_qr_code(path_to_download, path_to_save)
```
