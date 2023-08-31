from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='easy_chromedriver_windows_install',
    version='0.0.1',
    license='MIT License',
    author='Luan Grabher',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='luanggcontato@gmail.com',
    keywords='chromedriver selenium webdriver',
    description=u'Download chromedriver easily on Windows',
    packages=['easy_chromedriver_windows_install'],
    install_requires=['requests']
)