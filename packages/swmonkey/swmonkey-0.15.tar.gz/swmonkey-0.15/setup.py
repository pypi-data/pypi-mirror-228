from setuptools import setup, find_packages

setup(
    name='swmonkey',
    version='0.15',
    packages=find_packages(),
    author='Li Saifei',
    author_email='waltermitty121906@gmail.com',
    description='A tool for monkey test on Linux GUI',
    entry_points={
        'console_scripts': [
            'swmonkey = swmonkey.main:swmonkey'
        ]
    },
    install_requires=[
        'pyautogui',
        'psutil',
    ]
)