#!/usr/bin/python

import agentgw
import sys

if __name__ == '__main__' :

    app = agentgw.application(sys.argv[1])
    app.run()
