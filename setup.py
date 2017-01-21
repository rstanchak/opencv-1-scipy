#!/usr/bin/env python

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.misc_util import get_numpy_include_dirs
    from pkgconfig import pkgconfig

    pk = pkgconfig('opencv')
    
    config = Configuration('opencv',parent_package,top_path)
    cflags = pk['Cflags']
    libs = pk['Libs']
    cflags = cflags.replace('-I','')
    include_dirs = cflags.split(' ')
    ldflags = libs.split(' ')
    libdirs = []
    libs = []
    print ldflags
    for ld in ldflags:
        if ld.startswith('-L'):
            libdirs.append( ld.replace('-L','') )
        elif ld.startswith('-l'):
            libs.append( ld.replace('-l', '') )

    include_dirs += get_numpy_include_dirs() 
    include_dirs.append( 'src' )
    config.add_extension('_opencv',
            ['src/opencv.i', 
            'src/cv_typemaps.cpp'],
            include_dirs=include_dirs,
            library_dirs=libdirs,
            libraries=libs,
            extra_compile_args=["-ggdb"],
            swig_opts=["-c++"]
            )
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
