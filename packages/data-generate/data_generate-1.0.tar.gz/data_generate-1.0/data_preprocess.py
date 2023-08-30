import numpy as np
from scipy import stats



def get_slice_window_data(data, window_len, stride):
    """ 滑窗获取数据
    :param data: ndarray
    :param window_length: 窗口长度
    :param strides: 滑动步长
    :return: 获取的滑窗数据
    """
    slice_data = []
    for i in range(0, len(data) - window_len, stride):
        slice_data.append(
            data[i:i + window_len]
        )
    return np.asarray(slice_data)

feature_names = [
    "绝对中值",
    "最大值",
    "最大绝对值",
    "最小值",
    "均值",
    "峰峰值",
    "绝对平均值",
    "均方根值",
    "方根幅值",
    "标准差",
    "峭度",
    "偏度",
    "裕度指标",
    "波形指标",
    "脉冲指标",
    "峰值指标",
    "峭度指标",
]
# 滑窗数据 -> 特征数据
def get_feature(slice_data):
    """提取 17 个 时域特征
    :param slice_data: shape 为 (m, n) 的 2D array 数据，其中，m 为样本个数， n 为样本（信号）长度
    :return: shape 为 (m, 16)  的 2D array 数据，其中，m 为样本个数。即 每个样本的16个时域特征
    """
    rows, cols = slice_data.shape
    
    # 有量纲统计量
    abs_median = np.median(np.abs(slice_data), axis=1)
    max_value = np.max(slice_data, axis=1)  # 最大值
    peak_value = np.amax(abs(slice_data), axis=1)  # 最大绝对值
    min_value = np.amin(slice_data, axis=1)  # 最小值
    mean = np.mean(slice_data, axis=1)  # 均值
    p_p_value = max_value - min_value  # 峰峰值
    abs_mean = np.mean(abs(slice_data), axis=1)  # 绝对平均值
    rms = np.sqrt(np.sum(slice_data**2, axis=1) / cols)  # 均方根值
    square_root_amplitude = (np.sum(np.sqrt(abs(slice_data)), axis=1) / cols) ** 2  # 方根幅值
    # variance = np.var(slice_data, axis=1)  # 方差
    std = np.std(slice_data, axis=1)  # 标准差
    kurtosis = stats.kurtosis(slice_data, axis=1)  # 峭度
    skewness = stats.skew(slice_data, axis=1)  # 偏度
    # mean_amplitude = np.sum(np.abs(slice_data), axis=1) / cols  # 平均幅值 == 绝对平均值
    
    # 无量纲统计量
    clearance_factor = peak_value / square_root_amplitude  # 裕度指标
    shape_factor = rms / abs_mean  # 波形指标
    impulse_factor = peak_value  / abs_mean  # 脉冲指标
    crest_factor = peak_value / rms  # 峰值指标
    kurtosis_factor = kurtosis / (rms**4)  # 峭度指标
    
    features = [abs_median, max_value, peak_value, min_value, mean, p_p_value, abs_mean, rms, square_root_amplitude, std, kurtosis, skewness,
                clearance_factor, shape_factor, impulse_factor, crest_factor, kurtosis_factor][0]
    
    return np.array(features)




