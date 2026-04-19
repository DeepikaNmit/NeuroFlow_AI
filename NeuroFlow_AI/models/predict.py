import pandas as pd
import numpy as np

# Dummy prediction function (MVP)
def predict_traffic(hour, day, temp, rain, snow):
    base = 2000

    # Simple logic (can upgrade later)
    traffic = base \
        + (hour * 50) \
        + (day * 20) \
        + (temp * 5) \
        + (rain * 100) \
        + (snow * 150)

    return int(traffic)