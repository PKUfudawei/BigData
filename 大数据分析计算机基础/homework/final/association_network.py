import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


tables = {}
table_names = []
for f in os.listdir('./parquet'):
    table_names.append(f.split('.')[0])
    tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')
table_keys = {i: tables[i].columns.values for i in tables}


def iter_association(personids, network, edge_color, assoc_type: str='03'):
    """
    迭代寻找第n度社交关系, assoc_type=='03'表示寻找的是学术相关社交关系
    """
    if network is None:
        network = nx.Graph()
    new_personids = set()
    if len(personids)==0:
        return new_personids, network
    
    for personid in personids:
        t = tables['ASSOC_DATA'][tables['ASSOC_DATA']['c_personid']==personid]
        match_type = []
        for c in t['c_assoc_code'].values:
            match_type.append(tables['ASSOC_CODE_TYPE_REL']['c_assoc_type_id'][tables['ASSOC_CODE_TYPE_REL']['c_assoc_code']==c].values[0].startswith(assoc_type))
        t = t[match_type]
        scholar = []
        for c in t['c_assoc_code'].values:
            scholar.append(tables['ASSOC_CODE_TYPE_REL']['c_assoc_type_id'][tables['ASSOC_CODE_TYPE_REL']['c_assoc_code']==c].values[0].startswith('03'))
        t = t[scholar]
        start_name = tables['BIOG_MAIN']['c_name_chn'][tables['BIOG_MAIN']['c_personid']==personid].values[0]
        network.add_node(personid, name=start_name)
        
        for _, row in t.iterrows():
            new_personids.add(row['c_assoc_id'])
            name = tables['BIOG_MAIN']['c_name_chn'][tables['BIOG_MAIN']['c_personid']==row['c_assoc_id']].values[0]
            role = tables['ASSOC_CODES']['c_assoc_role_type'][tables['ASSOC_CODES']['c_assoc_code']==row['c_assoc_code']].values[0]
            network.add_node(row['c_assoc_id'], name=name)
            if (role=='A' or role=='M') and (personid, row['c_assoc_id']) not in network.edges:
                network.add_edge(personid, row['c_assoc_id'], color=edge_color)
            if (role=='P' or role=='M') and (row['c_assoc_id'], personid) not in network.edges:
                network.add_edge(row['c_assoc_id'], personid, color=edge_color)
              
    return new_personids, network


def plot_assocation_network(graph, name):
    """
    根据社交关系网络图, 利用Fruchterman-Reingold力导向算法定位节点, 使得节点分布尽量四散均匀, 提高观看美观度
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    
    G = graph
    labeldict = {
        node: G.nodes[node]['name'] for node in G.nodes if G.degree[node] > 1/3 * max(dict(G.degree).values())
    }
    
    plt.figure(figsize=(12, 12))
    ax = plt.gca()
    pos = nx.spring_layout(G, k=0.1)
    nx.draw(G, pos=pos, node_size=[i*10 for i in dict(G.degree).values()], edge_color=[G.edges[i]['color'] for i in G.edges], labels=labeldict, with_labels = True, ax=ax, alpha=1)
    plt.savefig(f"./images/{name}七度社交关系网络图.pdf", bbox_inches='tight')
    # plt.show()
    

def main():
    print("开始进行学术社会网络分析")
    personid = int(input("请输入历史名人的personid(如: 朱熹-3257): "))
    name = tables['BIOG_MAIN']['c_name_chn'][tables['BIOG_MAIN']['c_personid']==personid].values[0]
    new = set([personid])
    G = None
    for i, c in zip([0, 1, 2, 3, 4, 5, 6], ['red', 'green', 'darkorange', 'purple', 'DarkGray', 'hotpink', 'cyan']):
        new, G = iter_association(personids=new, network=G, edge_color=c)
        if len(new)==0:
            print(f"第{i+1}次迭代后: 已经无临近节点可遍历, 社会网络图中已有{len(G.edges)}条边")
        else:
            print(f"第{i+1}次迭代后: 有{len(new)}个临近节点可遍历, 社会网络图中已有{len(G.edges)}条边")
    
    plot_assocation_network(graph=G, name=name)
    

if __name__ == "__main__":
    main()
