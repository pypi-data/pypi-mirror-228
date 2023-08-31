from setuptools import setup

setup(
    name='CaptchaGenerator',
    version='1.1.6',
    license='MIT',
    long_description = "<a href='https://github.com/Sepehr0Day/CaptchaGenerator'>Documents is Available on Github</a>",
    long_description_content_type = "text/markdown",
    description='A library for captcha generator for Telegram bots',
    author='Sepehr0Day',
    author_email='sphrz2324@gmail.com',
    packages=['CaptchaGenerator'],
    install_requires=[
        'Pillow',
        'colorama',
        'gTTS'
    ],
)
