from setuptools import setup, find_packages

setup(
    name="SnapChatBot",
    version="1.0.1",
    packages=find_packages(),
    keywords=["snapchat", "bot", "snapchatbot"],
    install_requires=[
        "selenium",
        "pyvirtualdisplay"
    ],
)
