"""
The __main__ module lets the user start the ingress from the command line
"""
from typing import List

import os, sys

from ixoncdkingress.webserver.servlet import Servlet
from ixoncdkingress.webserver.config import Config
from ixoncdkingress.webserver import wsgi

def main(argv: List[str]) -> int:
    """
    Parses the arguments and runs the provider
    """
    del argv # Configuration goes via environment

    config = Config.from_environ(os.environ)
    servlet = Servlet(config)

    try:
        wsgi.run_server(config, servlet)
        return 0
    except KeyboardInterrupt:
        ...

    return 0

if '__main__' == __name__: # pragma: no cover
    sys.exit(main(sys.argv[1:]))
