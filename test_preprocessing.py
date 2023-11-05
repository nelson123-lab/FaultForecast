import pandas as pd

"""Function to convert the speedProfile to Upload and Downlaod data"""
def convert_speed(speed):
  if speed.endswith("M"):
    speed = float(speed.replace('M', ''))
  elif speed.endswith("K"):
    speed = float(speed.replace("K", ''))
    speed /= 1000
  else:
    speed = float(speed.replace('G', ''))
    speed *= 1000
  return speed

"""Preproecessing the test data inorder to pass into the model."""
def test_data_convertion(data):
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
  data['status'] = pd.Categorical(data['status'], ordered=True).codes
  data['ranged'] = pd.Categorical(data['ranged'], ordered=True).codes
  data['download_speed'] = data['speedProfile'].apply(lambda x: convert_speed(x.split('/')[0]))
  data['upload_speed'] = data['speedProfile'].apply(lambda x: convert_speed(x.split('/')[1]))
  # Remove the speedProfile column if needed
  data = data.drop('speedProfile', axis=1)
  return data