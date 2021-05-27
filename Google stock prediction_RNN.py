# importing libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import tensorflow as tf

### Data Preprocessing

dataset_train = pd.read_csv("Learning_Dataset/Google_Stock_Price_Trainset.csv")

#selecting the right column (we need all the rows of column 1)
training_set = dataset_train.iloc[:,1:2].values
print(dataset_train)
print(training_set)

# Feature scaling
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

#creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []

# One month has 20 trading days and we use 3 monthly data: 60 as the number of timesteps
# Per observation (X_train) will contain stock price of last 60 days and Y_train will have stock price of that day

for i in range(60,training_set_scaled.size):
    # appending the 60 previous stock prices to the list for i
    # we need to specify the rows and simply pick the first and only column
    X_train.append(training_set_scaled[i-60:i, 0])
    # appending the 60th stock price to the list for i
    y_train.append(training_set_scaled[i, 0])
# transforming pandas lists to numpy arrays required for the RNN
X_train, y_train = np.array(X_train), np.array(y_train)
print(X_train)


# Shaping/adding new dimensions to allow adding more indicators: from 2D to 3D
# 3 input arguments
# batch_size: number of observations
# timesteps: number of columns
# input_dim: number of predictors
X_train = np.reshape(X_train, [X_train.shape[0], X_train.shape[1], 1])
#print(X_train)


### Building RNN/LSTM model
#Initializing the RNN

# independent variable is a sequence of layers: regression and no classification given the continuous output value
regressor = Sequential()

# Adding the first LSTM layer

# 3 inputs
# number of memory/LSTM units or neurons in each LSTM
# binary vb to indicate whether there will be further layers of LSTM added to the model
# input shape (automatically takes teh first dimension so the remaining only needs to be specified)
regressor.add(LSTM(units = 50, return_sequences=True, input_shape = (X_train.shape[1], 1)))

# adding Dropout regularization layers
# 1 input: amount of neurons to ignore in the layers
regressor.add(Dropout(0.2))


# Adding the second LSTM layer
# no input shape needed given that that is specified in the previous layer
regressor.add(LSTM(units = 50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding the third LSTM layer
regressor.add(LSTM(units = 50, return_sequences=True))
regressor.add(Dropout(0.2))


# Adding the forth LSTM layer
regressor.add(LSTM(units = 50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding the fifth LSTM layer
# note that this is the final LSTM layer, hence we change the binary argument to False
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))


# Adding output layer to the RNN to make a fully connected NN

# one dimensional real output
regressor.add(Dense(units = 1))


### Compiling the RNN model
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

### Training RNN model
#connecting the built regressor to the training model
regressor.fit(X_train, y_train, epochs = 120, batch_size = 32)

### Testing RNN model
dataset_test = pd.read_csv("Learning_Dataset/Google_Stock_Price_Testset.csv")
# actual stock prices
real_stock_price = dataset_test.iloc[:,1:2].values
# predicting the stock prices using X_test
# we need the original training data (vertical concatination 0, horizontal 1)
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
print(real_stock_price)

# for the consistence of the model we need to have the same scaling on the test as on the training
# for the first test day we need the previous 60 days data from train
print("First Financial day in 2021, when testing period begins",len(dataset_total)- len(dataset_test))
print("First Financial day in 2021 minus 60 days",len(dataset_total)- len(dataset_test) - 60)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values

# reshaping,normalizing the inputs
inputs = inputs.reshape(-1,1)
# no longer fitting but just transforming
inputs = sc.transform(inputs)


#storing test data as we did in teh training
X_test = []
for i in range(60,inputs.size):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
# adding extra dimension
X_test = np.reshape(X_test, [X_test.shape[0], X_test.shape[1], 1])

# obtaining predicted values
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

### Visualizing the RNN model results
plt.plot(real_stock_price, color = 'blue', label = "Real Stock Price January 2021")
plt.plot(predicted_stock_price, color = 'red', label = "Predicted Stock Price January 2021")
plt.title("Google Stock Price Prediction")
plt.xlabel("Time")
plt.ylabel("Google Stock Price")
plt.legend()
plt.show()
