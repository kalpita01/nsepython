import logging
import os
from pynse import *
import json
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

nse = Nse()

nifty_50 = nse.get_indices(IndexSymbol.NiftyBank)
result = nifty_50.to_json(orient="split")
parsed = json.loads(result)
data = json.dumps(parsed, indent=4)
finaldata = json.loads(data)
print(finaldata)