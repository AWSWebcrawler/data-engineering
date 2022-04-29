import logging
from datetime import date

file = 'G:\GitHub\ProjektSS22\General\crawler\log\log_output\log' + str(date.today()) + '.log'
fmtstr = " %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
datestr = "%m/%d/%Y %I:%M:%S %p "
logging.basicConfig(filename=file,
                    level=logging.INFO,
                    filemode='a',
                    format=fmtstr,
                    datefmt=datestr)
