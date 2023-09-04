from setuptools import setup

setup(
    name="snugbug",
    version="1.2",
    author="istakshaydilip",
    description="A CLI based app for Coders and students alike.",
    long_description = open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["snugbug"],
    install_requires=[
        "Flask==2.3.3",
        "Flask-SocketIO==5.3.5",
        "rich==13.5.2",
        "requests",
        "websocket-client",
    ],
    entry_points={
        "console_scripts": [
            "snugbug=snugbug.main:main",
        ],
    },
)
