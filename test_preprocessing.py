import pandas as pd
import numpy as np

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
  data['status'] = pd.Categorical(data['status'], ordered=True).codes
  data['ranged'] = pd.Categorical(data['ranged'], ordered=True).codes
  data['download_speed'] = data['speedProfile'].apply(lambda x: convert_speed(x.split('/')[0]))
  data['upload_speed'] = data['speedProfile'].apply(lambda x: convert_speed(x.split('/')[1]))
  # Remove the speedProfile column if needed
  data = data.drop('speedProfile', axis=1)
  data['laserBiasThreshold'] = data['laserBiasThreshold'].fillna("Tunned _policy")
  data.loc[data['laserBiasThreshold'] == "ONT Internal Policy", 'laserBiasCurrent'] = data.loc[data['laserBiasThreshold'] == "ONT Internal Policy", 'laserBiasCurrent'].fillna(0)
  data['laserBiasThreshold'] = pd.Categorical(data['laserBiasThreshold'], ordered=True).codes
  data['videoAniAgcModePlanned'] = data['videoAniAgcModePlanned'].fillna("Instance Unavailable")
  columns_to_fill = ['videoAniAgcSetting', 'videoAniOpInfoOpticalSignalLevel', 'videoAniOpInfoOpticalSignalLevelDbm', 'videoAniOpInfoRfPowerLevel']
  condition = data['videoAniAgcModePlanned'] == "Instance Unavailable"
  data.loc[condition, columns_to_fill] = data.loc[condition, columns_to_fill].fillna(0)
  data['videoAniAgcModePlanned'] = pd.Categorical(data['videoAniAgcModePlanned'], ordered=True).codes
  data['videoAniOperState'] = data['videoAniOperState'].fillna("Instance Unavailable")
  data['videoAniOperState'] = pd.Categorical(data['videoAniOperState'], ordered=True).codes
  
  columns_to_replace = ['videoAniOpInfoOpticalSignalLevel', 'videoAniOpInfoOpticalSignalLevelDbm', 'videoAniOpInfoRfPowerLevel']
  value_to_replace = "Unknown"
  replacement_value = -1
  data[columns_to_replace] = data[columns_to_replace].replace(value_to_replace, replacement_value)
  # Converting to float data type from objects
  data = data.dropna(axis=1)
  columns_to_convert = ['laserBiasCurrent', 'videoAniOpInfoOpticalSignalLevel', 'videoAniOpInfoOpticalSignalLevelDbm', 'videoAniOpInfoRfPowerLevel']

  # Replace 'Not Supported' with NaN
  data[columns_to_convert] = data[columns_to_convert].replace('Not Supported', np.nan)

  # Convert the columns to float
  data[columns_to_convert] = data[columns_to_convert].astype(float)
  
  return data