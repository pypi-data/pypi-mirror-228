from setuptools import setup, find_packages


setup (
    name='Mensajes-JuanKaDrako',
    version='5.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license_files = ['LICENSE'] ,
    author='Juan Camilo Martínez',
    author_email='jcmartinezp06@gmail.com',
    url='',
    packages=find_packages(),
    scripts=[],
    test_suite= 'test' ,
    install_requieres=[paquete.strip() 
                       for paquete in open("requirements.txt").readlines()],
    classifiers= [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
