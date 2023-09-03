from setuptools import setup, find_packages

# README.md dosyasını açıp içeriğini okuyoruz
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kubitdb',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/DeveloperKubilay/pythonkubitdb',
    license='MIT',
    author='kubilaytr',
    py_modules=['kubitdb'],
    author_email='kullanici@example.com',
    description='Python KubitDB Modülü',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
