from setuptools import setup, find_packages

setup(
    name="snugbug",
    version="1.0",
    author="istakshaydilip",
    description="A CLI based app for Coders and students alike.",
    long_description=open("README.md").read(),
    packages=["snugbug"],
    install_requires=[
        "Flask==2.3.3",
        "Flask-SocketIO==5.3.5",
        "Flask-SQLAlchemy==3.0.5",
        "gunicorn==21.2.0",
        "eventlet==0.33.3",
        "rich==10.3.0",
        "requests",
        "websocket-client",
    ],
    entry_points={
        "console_scripts": [
            "snugbug=snugbug.main:main",
        ],
    },
)
