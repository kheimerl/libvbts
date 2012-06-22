from distutils.core import setup, Extension

setup(name="libvbts",
      version="0.0.1", 
      description="VBTS Tools for supporting community networks",
      author="Kurtis Heimerl",
      author_email="kheimerl@cs.berkeley.edu",
      url="http://tier.cs.berkeley.edu",
      packages=["libvbts"],
      license='BSD',
      scripts=[],
      data_files=[
        ("/usr/local/share/yate/scripts/",['yate/VBTSMain.py', 'yate/VBTS_New_User.py'])
        ]
      )
