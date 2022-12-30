# loading in modules
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt


def analyze_table_relationship(output: str):
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')
    table_keys = {i: tables[i].columns.values for i in tables}
    
    neighbor = {}
    intermediate = []
    for i in table_names:
        if len(table_keys[i]) == 2:
            intermediate.append(i)
        for j in table_names:
            if i==j:
                continue
            if table_keys[i][0] in table_keys[j]:
                if i not in neighbor:
                    neighbor[i] = {j: None}
                else:
                    neighbor[i].update({j: None})
    
    for i in neighbor:
        for j in neighbor[i]:
            if table_keys[i][0] == table_keys[j][0]:
                neighbor[i][j] = '一对一'
            else:
                neighbor[i][j] = '一对多'
    
    inter_tables = set(i for i in table_keys if len(table_keys[i])==2)
    
    candidates = []
    for i in neighbor:
        for j in neighbor[i]:
            if (i in inter_tables or j in inter_tables) and neighbor[i][j] == '一对多':
                candidates.append((i, j))
    pairs = []
    for pair1 in candidates:
        for pair2 in candidates:
            if pair1[0]==pair2[1]:
                pairs.append((pair1[1], pair2[0]))
    
    df = pd.DataFrame(columns=['表一', '表二', '表间关系'])
    for i in neighbor:
        for j in neighbor[i]:
            df.loc[len(df)] = [i, j, neighbor[i][j]]
    
    for p in pairs:
        df.loc[len(df)] = [p[0], p[1], '多对多']
    
    with open(output, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False)
        

def plot_table_relationship(csv: str):
    df = pd.read_csv(csv)
    G = nx.DiGraph()
    for _, row in df.iterrows():
        if row['表间关系'] == '一对一':
            G.add_edge(row['表一'], row['表二'], color='green')
        elif row['表间关系'] == '一对多':
            G.add_edge(row['表一'], row['表二'], color='blue')
        elif row['表间关系'] == '多对多':
            G.add_edge(row['表一'], row['表二'], color='red')
            
    plt.figure(figsize=(20, 16))
    ax=plt.gca()
    nx.draw_circular(G, node_color='white', edge_color=[G.edges[i]['color'] for i in G.edges], with_labels = True, font_size=8, node_size=30, ax=ax, alpha=0.7)
    plt.savefig("table_relationship.pdf", bbox_inches='tight')
    plt.show()


def main(csv: str):
    analyze_table_relationship(output=csv)
    plot_table_relationship(csv=csv)


if __name__ == "__main__":
    main(csv='./表间关系.csv')
