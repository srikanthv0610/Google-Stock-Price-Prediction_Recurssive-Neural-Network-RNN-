# Google Stock Price Prediction using Recurssive Neural Network (RNN):
 To predict the price of the Google stock, we use Deep Learning, Recurrent Neural Networks with Long Short-Term Memory(LSTM) layers.
 
 # Introduction:
 
 In Quantitative finance, predicting the stock price with high accuracy is a very important and difficult task. Although, it is imposiible to exactly 
estimate the stock prices, it is possible to make accurate predictions by using the past stock prices (Theory behind Brownian Motions). We analyse the upward and downward treds
in the past and use this as an indicator to predict the future prices. Long Short-Term Memory (LSTM) is a more sophisticated version of RNN which addresses the Vanishing Gradient Problem that RNNs often suffer from.

For this project, we use the past 5 years [Google stock price data](https://github.com/srikanthv0610/Google-Stock-Price-Prediction_Recurssive-Neural-Network-RNN-/tree/main/Dataset) in the time period of 2016-2020. The goal is to predict the upward or downward trend in the stock price of Google for January 2021.

![Image](https://github.com/srikanthv0610/Google-Stock-Price-Prediction_Recurssive-Neural-Network-RNN-/blob/main/Plots/Google%20Stock%20Price%20Development.png)

# Results:

![Image2](https://github.com/srikanthv0610/Google-Stock-Price-Prediction_Recurssive-Neural-Network-RNN-/blob/main/Plots/Figure_1.png)

Comparing the real and predicted Google stock values that are generated using RNN model, for the first month of 2021. RNN based on 5 LSTMs was able to properly predict all upward and downward trends as we see that the red line corresponding to the predicted stock prices follows the same pattern as the blue line which corresponds the real stock prices.


