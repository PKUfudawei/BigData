import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def plot_person_migration(personid: int):
    """
    根据c_personid为索引画出相关人物的生平迁移路线图, 不以姓名为索引是因为繁体且可能重名
    """
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')

    G = nx.DiGraph()
    df = tables['BIOG_ADDR_DATA'][tables['BIOG_ADDR_DATA']['c_personid']==personid]
    df = df.sort_values(by="c_sequence", inplace=False, ascending=True)
    addrs = df['c_addr_id'].values
    for i in range(len(addrs)):
        G.add_node(tables['ADDRESSES'][tables['ADDRESSES']['c_addr_id']==addrs[i]]['c_name_chn'].values[0],
            x = tables['ADDRESSES'][tables['ADDRESSES']['c_addr_id']==addrs[i]]['x_coord'].values[0],
            y = tables['ADDRESSES'][tables['ADDRESSES']['c_addr_id']==addrs[i]]['y_coord'].values[0]
        )
        if i<len(addrs)-1:
            G.add_edge(
                tables['ADDRESSES'][tables['ADDRESSES']['c_addr_id']==addrs[i]]['c_name_chn'].values[0],
                tables['ADDRESSES'][tables['ADDRESSES']['c_addr_id']==addrs[i+1]]['c_name_chn'].values[0]
            )
    G.remove_edges_from(nx.selfloop_edges(G))
    name = tables['BIOG_MAIN']['c_name_chn'][tables['BIOG_MAIN']['c_personid']==personid].values[0]
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 12))
    ax=plt.gca()
    nx.draw(G, pos={k: (G.nodes[k]['x'], G.nodes[k]['y']) for k in G.nodes}, ax=ax, node_color='lightgreen', edge_color='red', with_labels = True, font_size=18, node_size=100)
    plt.savefig(f"./images/{name}迁移路线.pdf", bbox_inches='tight')
    # plt.show()
    print(f"已将{name}的生平迁移路线储存到./images/{name}迁移路线.pdf中")
    

def main():
    print("开始绘画历史人物迁移地图")
    personid = int(input("请输入待查询人物编号(例: 苏轼-3767): "))
    plot_person_migration(personid=personid)

if __name__ == "__main__":
    main()