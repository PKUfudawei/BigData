import pandas as pd


def main(excel: str):
    xl_file = pd.ExcelFile(excel)
    dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
    for t in dfs:
        if t!='TABLE_LIST':
            dfs[t].loc[:, 'affiliated_table'] = t
            
    with open('./表格信息.csv', 'w', encoding='utf-8') as f:
        dfs['TABLE_LIST'].to_csv(f, index=False, header=True)

    all_df = pd.concat([dfs[i] for i in dfs if i!='TABLE_LIST'], axis=0, ignore_index=True, join='inner')
    all_df = all_df.drop_duplicates(subset='column_code', inplace=False, ignore_index=True)

    with open('./字段含义.csv', 'w', encoding='utf-8') as f:
        all_df.to_csv(f, index=False, header=True)


if __name__ == "__main__":
    main(excel='./cbdb_codebook.xlsx')