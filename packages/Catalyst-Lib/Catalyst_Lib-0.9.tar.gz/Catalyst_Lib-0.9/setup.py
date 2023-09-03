from distutils.core import setup

setup(
    name='Catalyst_Lib',  # How you named your package folder (MyLib)
    packages=['Catalyst_Lib'],  # Chose the same as "name"
    version='0.9',  # Start with a small number and increase it with every change you make
    license='Apache License 2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='The all in one python library you need',  # Give a short description about your library
    author='Catalyst Studios',  # Type in your name
    author_email='help@catalyst-studios.cc',  # Type in your E-Mail
    url='https://github.com/Catalyst-Studio/Lib_Files',  # Provide either the link to your github or to your website
    download_url='https://github.com/Catalyst-Studio/Lib_Files/',  # I explain this later on
    keywords=["library", "easy", "allinone"],  # Keywords that define your package best
    install_requires=['requests', 'matplotlib'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
