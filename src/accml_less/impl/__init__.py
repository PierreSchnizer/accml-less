"""Provide interface similar to Matlab middle layer

This interface will suffer from the results of the design cosiderations.

It puts together in one place

* different views
* the conversion between them

Furthermore, these conversions need to be updated e.g. after a LOCO
measurement is made

"""
import logging

logger = logging.getLogger("accml-less")
logger.error(f"{__name__}: use for convenience but not for long term development")