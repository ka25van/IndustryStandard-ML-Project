from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys


def test_log_and_exception():
    try:
        logging.info("Start logging")
        result=1/0
        print(result)
    except Exception as e:
        logging.debug("Exception")
        raise InsuranceException(e, sys)

if __name__== "__main__":
    try:
        test_log_and_exception()
    except Exception as e:
        print(e)
