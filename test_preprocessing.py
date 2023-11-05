import pandas as pd


# Preprocessing function
def preprocess_data(data):
  data = data.drop('Customer', axis=1)
  data = data.drop('clli', axis=1)
  data = data.drop(['year', 'month', 'day', 'date'], axis=1)
  columns = ['rack', 'shelf', 'slot', 'port', 'ont']
  data = data.drop(columns, axis=1)
  data = data.drop('objectName', axis=1)
  data[['berDownstream', 'berUpstream']] = data[['berDownstream', 'berUpstream']].fillna(-1)
  data = data.drop('objectType', axis=1)
  data[['networkRxLevel', 'modelRxLevel', 'modemTxLevel']] = data[['networkRxLevel', 'modelRxLevel', 'modemTxLevel']].fillna(method='ffill').fillna(method='bfill')
  data[['opticalVoltage', 'modemType', 'status', 'ranged', 'distance']] = data[['opticalVoltage', 'modemType', 'status', 'ranged', 'distance']].fillna(method='ffill').fillna(method='bfill')
  median_value = data['opticalTemperature'].median()
  data['opticalTemperature'] = data['opticalTemperature'].fillna(median_value)
  data[['TMAX', 'TMIN']] = data[['TMAX', 'TMIN']].fillna(method='ffill').fillna(method='bfill')
  mean_value = data['PRCP'].mean()
  data['PRCP'] = data['PRCP'].fillna(mean_value)
  # Appplying the first Condition
  data.loc[data['PRCP'] == 0.0, 'SNOW'] = data.loc[data['PRCP'] == 0.0, 'SNOW'].fillna(0.0)
  # Applying the Second Condition
  data.loc[data['TMIN'] > 50, 'SNOW'] = data.loc[data['TMIN'] > 50, 'SNOW'].fillna(0.0)
  data = data.drop('SNOW', axis=1)
  data = data.dropna(axis=1)
  data = data.drop(['status', 'ranged', 'speedProfile'], axis=1)
  return data