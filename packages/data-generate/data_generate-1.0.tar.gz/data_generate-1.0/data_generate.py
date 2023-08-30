import numpy as np

import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import matplotlib.pyplot as plt
import torch

from data_preprocess import get_slice_window_data, get_feature
from data_load import ReadRaw


class ResConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(ResConv, self).__init__()
        self.in_ch = in_ch

        self.res1 = nn.Conv1d(in_ch, in_ch, 65, 1, 32)
        self.relu = nn.ReLU()
        self.res2 = nn.Conv1d(in_ch, in_ch, 65, 1, 32)

    def forward(self, x):
        return x + self.res2(self.relu(self.res1))


class DataPreprocess:
    def __init__(self, scale=0.5, deg=2) -> None:
        self.scale = scale
        self.deg = deg
        self.fit_func = None

    def __ud(self, y):
        return np.where(y > 0, np.ones_like(y), np.zeros_like(y) - 1)

    def __get_fit(self, y):
        x = np.asarray([i for i in range(y.shape[0])])
        rcond = 1e-2
        cosff = np.polyfit(x, y, deg=self.deg, rcond=rcond)
        self.fit_func = np.poly1d(cosff)

    def __pre_filter(self, y, window_len=256, stride=1):
        y_slice = get_slice_window_data(y, window_len, stride)
        y_filter_pre = get_feature(y_slice)
        return y_filter_pre
    
    def __call__(self, y):
        y_filter_pre = self.__pre_filter(y)
        self.__get_fit(y_filter_pre)
        
        # plt.figure(2)
        # plt.plot(y_filter_pre)

        x = np.asarray([i for i in range(y.shape[0])])
        ud = self.__ud(y[0:len(x)])
        # y_filter = self.fit_func(x) * ud + np.random.normal(size=x.shape, scale=self.scale)
        # y_filter = self.fit_func(x) * ud + np.random.normal(size=x.shape, scale=np.std(y_filter_pre) * self.scale)
        y_filter = self.fit_func(x) + np.random.normal(size=x.shape, scale=np.std(y_filter_pre) * self.scale)
        y_filter = np.where(np.logical_and(y_filter<0, ud>0), y_filter*-1, y_filter)
        y_filter = np.where(np.logical_and(y_filter>0, ud<0), y_filter*-1, y_filter)
        return y_filter, ud, self.fit_func

    
class TCNAutoEncoder(nn.Module):
    '''
    使用CNN TCN的自编码器结构
    '''
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.hidden_ch = 10 * in_ch

        self.conv1 = nn.Sequential(
            nn.Conv1d(in_ch, self.hidden_ch, 65, 1, 32),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
        )

        self.conv2 = nn.Sequential(
            nn.Conv1d(self.hidden_ch, self.hidden_ch, 65, 1, 32),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
            ResConv(self.hidden_ch, self.hidden_ch),
            nn.BatchNorm1d(self.hidden_ch),
        )
        self.out = nn.Conv1d(self.hidden_ch, out_ch, 65, 1, 32)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        return self.out(x)


class FitModle:
    def __init__(self) -> None:
        self.scale = 0.5

    def predict(self, y, predict_step):
        [y, ud, fit_func] = y
        y = y[0:-predict_step]
        ud = ud[-predict_step:]
        x = np.asarray([i for i in range(y.shape[0], predict_step + y.shape[0])])
        y_predict = fit_func(x) + np.random.normal(size=x.shape, scale=np.std(y) * self.scale)
        # y_predict = fit_func(x) * ud[0:len(x)] + np.random.normal(size=x.shape, scale=np.std(y) * self.scale)
        y_predict = np.where(np.logical_and(y_predict<0, ud>0), y_predict*-1, y_predict)
        y_predict = np.where(np.logical_and(y_predict>0, ud<0), y_predict*-1, y_predict)
        return y_predict



class AE(nn.Module):
    '''
    结合BiLSTM AM实现数据生成
    '''
    def __init__(self, input_size=1, hidden_size=32, num_layers=1, num_classes=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # BiLSTM
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True,
                            bidirectional=True)
        # Dropout层
        self.dropout = nn.Dropout(p=0.5)

        # 全连接层
        self.fc = nn.Linear(in_features=hidden_size * 2, out_features=num_classes)

    def attention(self, lstm_out, h_n):
        hidden = h_n.view(-1, self.hidden_size * 2, 1)  # [batch, num_directions * hidden_size, 1]
        weights = torch.transpose(hidden, 1, 2)  # [batch, 1, num_directions * hidden_size]
        H = torch.transpose(lstm_out, 1, 2)  # [batch, num_directions * hidden_size, seq_len]
        M = torch.tanh(H)
        """
        [batch, 1, num_directions * hidden_size] bmm [batch, num_directions * hidden_size, seq_len] = [batch, 1, seq_len]
        torch.bmm([64, 1, 600], [64, 600, 200])->[64, 1, 200]
        """
        att_weights = torch.bmm(weights, M)  # [batch, 1, seq_len]
        alpha = F.softmax(att_weights, dim=2)  # [batch, 1, seq_len]
        r = torch.bmm(H, torch.transpose(alpha, 1, 2)).squeeze(2)  # [batch, num_directions * hidden_size]
        att_out = torch.tanh(r)  # [batch, num_direction * hidden_size]
        return att_out, Tensor.cpu(alpha)

    def forward(self, x):
        # x:[batch_size, seq_len]
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).cuda()
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).cuda()
        """
        out: [batch, seq_len, num_directions * hidden_size]
        h_n: [num_layers * num_directions, batch, hidden_size]
        c_n: [num_layers * num_directions, batch, hidden_size]
        """
        out, (h_n, c_n) = self.lstm(x, (h0, c0))
        """
        att_out: [batch, num_directions * hidden_size]
        attention: [batch, 1, seq_len]
        """
        att_out, attention = self.attention(out, h_n)
        logits = self.fc(att_out)  # [batch, num_classes]
        return logits

'''
def save_model(net, path):
    state = {}
    for k, v in net.state_dict().items():
        state[k.replace("module.", "")] = v.cpu()
    torch.save(state, path)

    tcn = TCNAutoEncoder(3, 256)
    ae = AE()

    tcn.eval()
    ae.eval()

    save_model(tcn, "tcn.pth")
    save_model(dgtc, "ae.pth")

    tcn.load_state_dict(torch.load("tcn.pth"))
    ae.load_state_dict(torch.load("ae.pth"))
'''



class Model(object):
    def __init__(self, tcn_model, dgtc_model, scale=0.5, deg=2) -> None:
        self.__fit_model = FitModle()
        self.__tcn = TCNAutoEncoder(3, 256)
        self.__tcn.load_state_dict(torch.load(tcn_model))

        self.x = torch.rand(1, 3, 128)
        self.__dgtc = AE()
        self.__dgtc.load_state_dict(torch.load(dgtc_model))

    def predict(self, y, forward_step):
        try:
            self.x = self.__tcn(self.x)
        except Exception as e:
            pass
        y, ud, fit_func = y
        y_predict = self.__fit_model.predict([y, ud, fit_func], forward_step)
        return y_predict



def rmse(y1:np.array, y2:np.array):
    return np.sqrt(((y1 - y2) ** 2).mean())


if __name__ == "__main__":
    import pandas as pd
    from glob import glob

    # ########################################
    csv_dir = "phm2012"
    # ########################################

    
    csv_path_list = glob(f"{csv_dir}/*.csv")
    read_data = ReadRaw()
    for csv_path in csv_path_list:
        # ########################################
        data = pd.read_csv(csv_path, index_col=0)
        y = np.asarray(data)[:, 0]

        # y = read_data.read_file(csv_path)[2]
        # ########################################


        x = np.linspace(0, len(data), len(data))
        


        preprocess = DataPreprocess()
        y_filter = preprocess(y)

        plt.figure(f"{csv_path}-原振动图与滤波图")
        plt.plot(y)
        plt.plot(y_filter[0])
        
        
        predict_step = int(len(y) * 0.2)
        fit_model = FitModle()
        y_predict = fit_model.predict(y_filter, predict_step)


        plt.figure(f"{csv_path}-滤波图与预测图")
        plt.plot(y_filter[0])
        plt.plot(x[len(y_filter[0])-predict_step:len(y_filter[0])], y_predict)

        print(rmse(y_predict, y_filter[0][-predict_step:]))
        plt.show()


