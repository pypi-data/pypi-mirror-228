import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["Pillow>=9.0.1", "qrcode>=7.3.1"]

setuptools.setup(
    name="qrcode_img",
    version="1.0.7",
    author="Roman Andreev",
    author_email="grand-roman@yandex.ru",
    description="Generation QR Code with IMG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grand-roman/gen_qr_code_with_img",
    packages=["qrcode_img"],
    install_requires=requirements,
    python_requires=">=3.6",
    zip_safe=False,
)
