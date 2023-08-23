# -*- coding: utf-8 -*-
"""TOTAL PREDICTION.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b54sPgXL1UmH1FVpI3tySeAYamXwdvaO

**Importing Libraries And Modules**
"""

from google.colab import files

import pandas as pd
import numpy as np
import keras
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing import sequence
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import minmax_scale
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
import tensorflow as tf
import math
import matplotlib.pyplot as plt
import swiftxrt_clean

device_name = tf.test.gpu_device_name()
if len(device_name) > 0:
    print("Found GPU at: {}".format(device_name))
else:
    device_name = "/device:CPU:0"
    print("No GPU, using {}.".format(device_name))

"""**Cleaning Of Raw SWIFT XRT Data**"""

swiftxrt_clean.clean_file('/content/GRB_130527A.dat')

data_orig = pd.read_table('/content/GRB_130527A.dat',sep='\s+')
data_orig

from pandas import DataFrame as df

Y = df.to_numpy(data_orig)

Y

plt.figure(figsize=(16,9))
plt.errorbar(Y[:,0], Y[:,3], linestyle='none', xerr=Y[:,1], yerr=Y[:,4], marker='o',capsize=5)
plt.loglog()
plt.title("GRB050128")
plt.xlabel("t (s)")
plt.ylabel("Flux (erg/cm^2/s)")

after_burst = data_orig

after_burst = after_burst.sort_values(by=['!Time'])

after_burst

def create_batches(N,Ba_Sz,updated_after_burst):
  batches = []
  start = 0
  while(start < N) :
    if start + Ba_Sz <= N :
      after_burst_even = updated_after_burst.iloc[start:start + Ba_Sz]
      after_burst_even = after_burst_even.reset_index()
      batches.append(upsample_data(after_burst_even))
    else :
      after_burst_even = updated_after_burst.iloc[start:N]
      after_burst_even = after_burst_even.reset_index()
      batches.append(upsample_data(after_burst_even))
    start = start + Ba_Sz
  return batches

def create_data(t,f):
  updated_after_burst = pd.DataFrame()
  updated_after_burst[t] = []
  updated_after_burst[f] = []
  for i in range(after_burst.shape[0]-1) :
    start_time = after_burst[t][i]
    end_time = after_burst[t][i+1]
    start_flux = after_burst[f][i]
    end_flux = after_burst[f][i+1]
    time_upd = (end_time - start_time) / 20
    flux_upd = (end_flux - start_flux) / 20
    for j in range(19):
      new_row = {t : start_time, f : start_flux}
      updated_after_burst = updated_after_burst.append(new_row,ignore_index = True)
      start_time = start_time + time_upd
      start_flux = start_flux + flux_upd
  return updated_after_burst

def upsample_data(data):
  while(data.shape[0] < 20000) :
    data = data.append(data,ignore_index = True)
  return data

def create_sequence(dataset):
    data_sequences = []
    for index in range(len(dataset)):
        data_sequences.append(dataset[index:index+1])
    return np.asarray(data_sequences)

# Creating RNN Model Via Function Definition

def create_bilstm(units,X,Y):
    model = Sequential()

    # Input layer
    model.add(Bidirectional(
              LSTM(units = units, return_sequences=True),
              input_shape=(X.shape[0], X.shape[1])
              ))

    # Hidden layer
    model.add(Bidirectional(LSTM(units = units,return_sequences=True)))
    model.add(Bidirectional(LSTM(units = units,return_sequences=True)))
    model.add(Bidirectional(LSTM(units = units,return_sequences=True)))
    model.add(Bidirectional(LSTM(units = units)))
    layer = tf.keras.layers.Dense(1,activation = 'relu')
    model.add(layer)
    #Compile model
    model.compile(optimizer='adam',loss='mse')
    return model

units = 100

# Training Of Model Via Function Definition

def fit_model(model,X,Y):
    early_stop = tensorflow.keras.callbacks.EarlyStopping(monitor = 'val_loss',
                                               patience = 5)
    history = model.fit(X, Y, epochs = 75,
                        validation_split = 0.4,
                        batch_size =15, shuffle = True,
                        callbacks = [early_stop]
                        )
    return history

def train_model(batches,B,t,f):
  # Training And Predicting For Each Batch

  preds = []

  for b in range(B) :
    batch = batches[b]
    X = batch[t]
    Y = batch[f]
    X = create_sequence(X)
    Y = Y[-X.shape[0]:]
    print('Model Training / Batch Number : {}'.format(b+1))
    model_b = create_bilstm(units,X,Y)
    histor = fit_model(model_b,X,Y)
    pr = model_b.predict(X)
    for x in pr :
      preds.append(x)
  return preds

def time_seq(batches,B,t):
  time_predict = []
  for b in range(B) :
    for i in range(len(batches[b])):
      val = (batches[b][t][i])
      time_predict.append(val)
  return time_predict

"""**DATA PREPROCESSING**"""

after_burst['!Time'] = (after_burst['!Time']) / 10**2

b = after_burst['Flux'].min()
b

after_burst['Flux'] = np.log(after_burst['Flux'] / b) + 1

a = after_burst['Fluxpos'].min()

after_burst['Fluxpos'] = np.log(after_burst['Fluxpos'] / a) + 1

"""**FLUX TIME PREDICTION**"""

flux_time_upd_data = create_data('!Time','Flux')

# Input for Number Of Data Points In Each Batch

Ba_Sz = int(input())

N = flux_time_upd_data.shape[0]

batches_flux_time = create_batches(N,Ba_Sz,flux_time_upd_data)

B = len(batches_flux_time)

with tf.device(device_name):
  flux_preds = train_model(batches_flux_time,B,'!Time','Flux')

"""**Re Organising and Plotting of Data**"""

batches_flux_time

fl = []
ti = []
for batch in batches_flux_time :
  for f in batch['Flux']:
    fl.append(f)
  for t in batch['!Time']:
    ti.append(t)

Flux_std = np.std(fl)
Time_std = np.std(ti)

Flux_std

Time_std

time_predict = time_seq(batches_flux_time,len(batches_flux_time),'!Time')

time_predict = np.array(time_predict)
X_new , idx = np.unique(time_predict,return_index = True)
Y_new = [flux_preds[i] for i in idx]

X_new.shape

Y_new = np.array(Y_new)

Y_new.shape

plt.scatter(after_burst['!Time'],after_burst['Flux'])
plt.plot(X_new,Y_new[:,0],color='orange',  linestyle = (0,(0.1,2)),
    dash_capstyle = 'round', linewidth=7)
plt.xscale('log')
plt.yscale('log')
plt.xlabel("t (s)")
plt.ylabel("Flux (erg/cm^2/s)")
plt.legend(['Original Points','Predicted Points'])
plt.title("Flux vs Time Prediction for Break Bump (with double break) GRB 070129")

Y_new_std = np.std(Y_new)
Y_new_std

X = pd.DataFrame()
X['!Time'] = X_new

X['Flux'] = Y_new

Y_new[4250:]

X = df.to_numpy(X)

Y_temp = Y

Y_temp

Y_temp[:,0] = Y_temp[:,0] / 100

Y_temp[:,3] = np.log(Y_temp[:,3] / np.min(Y_temp[:,3])) + 1
Y_temp[:,4] = np.log(Y_temp[:,4] / np.min(Y_temp[:,4])) + 1

Y_temp

type(Y_temp)

Y_df = pd.DataFrame(Y_temp)
Y_df

data_orig

error_calculation_x = data_orig.loc[1:,:]

error_calculation_x

error_calculation_x['Flux'][1]

error_calculation_x['!Time'] = error_calculation_x['!Time'] / 100

error_calculation_x

flux_predict = batches_flux_time[0]['!Time']
flux_predict[19]

import math
idx = -1
j = 1
bania =  257.968
err_bania = 10000.00
for i in flux_predict:
  if abs(bania-i) < err_bania:
    idx = j
    err_bania = abs(bania-i)
  j += 1
print(idx)

print(flux_predict[573][])

y_init = [flux_predict[i] for i in idx]
y_init[0]

Y_new

print(Y_new)