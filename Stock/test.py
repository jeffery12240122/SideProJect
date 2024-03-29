import torch
import torch.nn as nn
import numpy as np
import pandas as pd


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, input):
        lstm_out, _ = self.lstm(input.view(len(input), 1, -1))
        output = self.fc(lstm_out.view(len(input), -1))
        return output


input_size = 1
hidden_size = 100
output_size = 1


model = LSTMModel(input_size, hidden_size, output_size)


model.load_state_dict(torch.load('model.pth'))


csvdata = pd.read_csv('new.csv', usecols=[0])


data = csvdata.iloc[:, 0]
X = data[-1:] 
y = data[1:]


X_tensor = torch.Tensor(X.values)
y_tensor = torch.Tensor(y.values)

with torch.no_grad():

    pred_index = X_tensor.view(1, 1, 1)

    predictions = []
    for i in range(20):

        pred = model(pred_index)

        predictions.append(pred.item())

        pred_index = pred.view(1, 1, 1)


print("Predictions:", predictions)
