import logging
import os
from pynse import *
import json

logging.basicConfig(level=logging.DEBUG)

nse = Nse()

top_10 = nse.get_indices(IndexSymbol.Nifty50)
result = top_10.to_json(orient="split")
parsed = json.loads(result)
data = json.dumps(parsed, indent=4)
finaldata = json.loads(data)

print(finaldata)
