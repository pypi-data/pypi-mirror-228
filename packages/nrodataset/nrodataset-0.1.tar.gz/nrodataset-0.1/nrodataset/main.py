from scipy.io import loadmat


def load_networks(network_type, network_size):
    if network_type[:5] != 'real-':
        file_path = f'synthetic_networks_{network_size}.mat'
    else:
        file_path = f'real-{network_type}.mat'
    data = loadmat(file_path)
    # 进行数据处理和转换
    return data
