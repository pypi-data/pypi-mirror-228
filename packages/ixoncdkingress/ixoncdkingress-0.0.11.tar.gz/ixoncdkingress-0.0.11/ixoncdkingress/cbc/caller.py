"""
Functions for finding and calling CBC functions.
"""
from typing import Any

import importlib
import sys

from ixoncdkingress.cbc.context import CbcContext
from ixoncdkingress.types import FunctionLocation, FunctionArguments
from ixoncdkingress.utils import handle_exception
from ixoncdkingress.webserver.config import Config
from ixoncdkingress.webserver.response import Response

def call_cbc( #pylint: disable=inconsistent-return-statements
        config: Config, context: CbcContext,
        function_location: FunctionLocation,
        function_kwargs: FunctionArguments,
        response: Response
    ) -> Any:
    """
    Finds, loads and calls the function specified in the body. The content_type specifies the
    format of the body.
    """

    # Get the specified module
    sys.path.insert(0, config.cbc_path)
    module = importlib.import_module(function_location[0])
    if config.production_mode is False:
        try:
            module = importlib.reload(module)
        except ImportError as error:
            handle_exception(error, response)
            return
    del sys.path[0]

    # Get the specified function
    if hasattr(module, function_location[1]):
        function = getattr(module, function_location[1])

        # Check if it's exposed
        if getattr(function, 'exposed', False):
            return function(context, **function_kwargs)

    return f"Not found, function '{'.'.join(function_location)}' does not exist or is not exposed"
