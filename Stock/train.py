import torch
import torch.nn as nn
import numpy as np
import pandas as pd


csvdata = pd.read_csv('new.csv', usecols=[0])


data = csvdata.iloc[:, 0]


X = data[:-1]
y = data[1:]


X_tensor = torch.Tensor(X.values)
y_tensor = torch.Tensor(y.values)


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

# 初始化模型
input_size = 1
hidden_size = 100
output_size = 1
model = LSTMModel(input_size, hidden_size, output_size)


criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


epochs = 100000
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = criterion(outputs, y_tensor.view(-1, 1))  # 需要将 y_tensor 调整为二维张量
    loss.backward()
    optimizer.step()
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item()}')
        torch.save(model.state_dict(), 'model10.pth')




