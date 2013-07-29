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
      install_requires=['smspdu'],
      data_files=[
        ("/usr/local/freeswitch/scripts",['freeswitch/VBTS_Parse_SMS.py',
                                          'freeswitch/VBTS_New_User.py',
                                          'freeswitch/VBTS_Send_SMS.py',
                                          'freeswitch/VBTS_Send_Empty_SMS.py',
                                          'freeswitch/VBTS_Send_SMS_Direct.py',
                                          'freeswitch/VBTS_Send_Empty_SMS_Direct.py',
                                          'freeswitch/VBTS_Wake_BTS.py',
                                          'freeswitch/VBTS_Log_SMS.py',
                                          'freeswitch/VBTS_DB_Get.py',
                                          'freeswitch/VBTS_Get_Location.py',
                                          'freeswitch/VBTS_DB_Set.py'])
        ]
      )
