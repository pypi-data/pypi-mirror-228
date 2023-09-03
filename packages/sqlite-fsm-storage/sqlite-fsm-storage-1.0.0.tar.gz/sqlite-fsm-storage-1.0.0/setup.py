from setuptools import setup


setup(
    name='sqlite-fsm-storage',
    version='1.0.0',
    author='EgorBlaze',
    author_email='blazeegor@gmail.com',
    description='SQLiteStorage is a very good FSM Storage for Telegram bots.',
    license='Apache License, Version 2.0, see LICENSE file',
    packages=['sqlite-fsm-storage'],
    install_requires=['aiogram']
)