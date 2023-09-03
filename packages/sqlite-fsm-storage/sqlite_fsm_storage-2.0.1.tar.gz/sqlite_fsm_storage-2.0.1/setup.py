from setuptools import setup


setup(
    name='sqlite_fsm_storage',
    version='2.0.1',
    author='EgorBlaze',
    author_email='blazeegor@gmail.com',
    description='SQLiteStorage is a very good FSM Storage for Telegram bots.',
    long_description='This is FSM Storage for Telegram bots on aiogram.',
    license='Apache License, Version 2.0, see LICENSE file',
    packages=['sqlite_fsm_storage'],
    install_requires=['aiogram']
)