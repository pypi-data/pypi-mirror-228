from distutils.core import setup

setup(name='neste-braces',
      version='1.0.0',
      description='Desciption for neste here',
      author='Ville M. Vainio',
      author_email='ville.vainio@basware.com',
      url='https://github.com/vivainio/neste',
      packages=['neste'],
      install_requires=[],
      entry_points = {
        'console_scripts': [
            'neste = neste.neste:main'
        ]
      }
     )
