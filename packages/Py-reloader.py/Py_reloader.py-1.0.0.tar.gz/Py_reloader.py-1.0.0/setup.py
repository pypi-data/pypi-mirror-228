from distutils.core import setup

setup(
    name="Py_reloader.py",
    version="1.0.0",
    description="""
########################################
#        WELCOME TO PY_RELOADER        #
#                                      #
#  -ENTER A FILE AND RUN               #
#  -FOR RE-RUN ONLY PRESS R            #
#  -FOR EXIT PRESS Q                   #
#                                      #
##############  BUT  WHY  ##############
#      Beacuse very easy and fast      #
#       Debugging and developing       #
#                                      #
########################################
""",
    author="CODE_BREAKER",
    author_email = 'taneymen2009@gmail.com',
    install_requires=[
        'colorama',
    ],
    packages=["."],
)