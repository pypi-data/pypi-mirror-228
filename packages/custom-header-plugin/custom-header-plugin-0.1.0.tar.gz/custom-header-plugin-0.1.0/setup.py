from setuptools import setup

setup(
    name='custom-header-plugin',  # Replace with your plugin's package name
    version='0.1.0',  # Replace with the desired version number
    description='A custom header plugin for MkDocs',
    author='abhiramp',
    author_email='abhiram.is17@bmsce.ac.in',
    url='https://github.com/yourusername/your-plugin-repo',
    packages=['test_plugin'],  # Replace with your package name
    install_requires=['mkdocs'],  # List dependencies here
)