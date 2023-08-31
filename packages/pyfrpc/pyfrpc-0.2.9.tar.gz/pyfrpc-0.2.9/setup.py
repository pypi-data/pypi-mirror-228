import os

from setuptools import setup, Extension
from distutils.command.build_ext import build_ext


PYFRPC_NOEXT = bool(int(os.environ.get('PYFRPC_NOEXT', '0')))


setup_args = dict(
    name='pyfrpc',
    version='0.2.9',
    description='Python implementation of fastrpc protocol',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vladimir Burian',
    license='MIT',
    url='https://gitlab.com/vladaburian/pyfrpc',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='frpc fastrpc',
    packages=['pyfrpc'],
    package_dir={'':'src'},
    package_data={'pyfrpc':['*.pyx']},
    install_requires=['requests'],
    extras_require={'nc': ['ipython'], 'async': ['aiohttp']},
    entry_points={
        'console_scripts': [
            'pyfrpc = pyfrpc.netcat:main',
        ],
    },
)


class cython_lazy_build_ext(build_ext):
    def run(self):
        try:
            from Cython.Build import cythonize
        except ImportError:
            print(
                "\n"
                "Error: cython module is missing. Do one of the following:\n"
                "  A) Install Cython and C toolchain to compile C extension\n"
                "     with fast encoder/decoder implementation.\n"
                "  B) Set env PYFRPC_NOEXT=1 to disable C extension and use\n"
                "     slower but pure python implementation.\n"
            )

            raise

        # Run 'cythonize' lazily
        self.extensions = cythonize(self.extensions, language_level=3)

        # Perform the build
        build_ext.run(self)


if not PYFRPC_NOEXT:
    setup_args['ext_modules'] = [Extension('pyfrpc._coding_base_c', ['src/pyfrpc/_coding_base_c.pyx'])]
    setup_args['cmdclass'] = {'build_ext': cython_lazy_build_ext}


if __name__ == "__main__":
    setup(**setup_args)
