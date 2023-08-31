from setuptools import setup

setup(
    name="SnapChatBot",
    version="1.0.3",
    include_package_data=True,
    python_requires=">=3.11",
    keywords=["snapchat", "bot", "snapchatbot"],
    install_requires=[
        "selenium",
        "pyvirtualdisplay"
    ],
)
