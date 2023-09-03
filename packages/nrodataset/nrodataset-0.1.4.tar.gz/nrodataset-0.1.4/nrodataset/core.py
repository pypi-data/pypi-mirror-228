# Insert your code here.
import networkx as nx
import scipy.io as sio


def load_networks(network_type, network_size):
    if network_type[:5] != 'real-':
        file_path = f'{network_type}_{network_size}.mat'
    else:
        file_path = f'real-{network_type}.mat'
    mat = sio.loadmat(file_path)
    num_instance = mat['num_instances'][0, 0]
    isd = mat['isd'][0, 0]
    isw = mat['isw'][0, 0]
    original_networks = []
    optimized_networks = []
    for i in range(num_instance):
        ori_adj = mat['original'][0, i]['adj'][0, 0]
        if not isd:
            ori_graph = nx.from_scipy_sparse_matrix(ori_adj, create_using=nx.Graph)
        else:
            ori_graph = nx.from_scipy_sparse_matrix(ori_adj, create_using=nx.DiGraph)

        opt_adj = mat['optimized'][0, i]['adj'][0, 0]
        if not isd:
            opt_graph = nx.from_scipy_sparse_matrix(opt_adj, create_using=nx.Graph)
        else:
            opt_graph = nx.from_scipy_sparse_matrix(opt_adj, create_using=nx.DiGraph)
        original_networks.append(ori_graph)
        optimized_networks.append(opt_graph)
    res_dic = {
        'isd': isd,
        'isw': isw,
        'number_of_networks': num_instance,
        'original_networks': original_networks,
        'optimized_networks': optimized_networks,
        'network_type': network_type,
    }
    return res_dic
