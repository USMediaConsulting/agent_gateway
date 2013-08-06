#!/usr/bin/python

import biddergw
import sys

if __name__ == '__main__' :

    app = biddergw.application(sys.argv[1])
    app.run()
