#%%
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from pmdarima.arima import ndiffs
from pmdarima.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tqdm import tqdm

df = pd.concat(
    map(pd.read_json, Path("data").glob("forcast_*.json")), ignore_index=True
)
df["time"] = df.apply(lambda r: datetime.fromtimestamp(r["time"]), axis=1)
df = df.sort_values(by=["time"])

temperature = df["temperature"]
temperature = temperature.fillna(temperature.mean())

train, test = train_test_split(temperature, train_size=temperature.shape[0] - 365)

print(f"training size: {train.shape[0]}")
print(f"testing size: {test.shape[0]}")


# %%
kpss_diffs = ndiffs(train, alpha=0.05, test="kpss", max_d=6)
adf_diffs = ndiffs(train, alpha=0.05, test="adf", max_d=6)
n_diffs = max(adf_diffs, kpss_diffs)

print(f"d: {n_diffs}")


# %%
model = auto_arima(
    train,
    d=n_diffs,
    seasonal=True,
    m=4,
    stepwise=True,
    suppress_warnings=True,
    max_p=6,
    trace=2,
    random_state=2020,
)

print(f"model order: {model.order}")


# %%
predictions = []
for observation in tqdm(test):
    prediction = model.predict(n_periods=1)[0]
    predictions.append(prediction)
    model.update(observation)


#%%
size = test.shape[0]
train = train[-size:]

train_index = sorted(train.index[-size:])
test_index = sorted(test.index)
fig = plt.figure(figsize=(12, 9), dpi=80)
plt.plot(train_index, train, color="black", label="Latest Training Data")
plt.plot(test_index, test, color="blue", label="Actual Observation")
plt.plot(test_index, predictions, color="green", label="Predicted Value")
plt.title(f"Last year: MSE={mean_squared_error(test, predictions):.2f}")
plt.xticks([])
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.legend(loc="lower left")
fig.savefig("static/time-series-analysis", bbox_inches="tight")
