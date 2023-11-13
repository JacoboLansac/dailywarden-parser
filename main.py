import numpy as np
import pandas as pd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-nr', '--number-of-rows', default=10, type=int)
    args = parser.parse_args()

    with open("email", 'r') as f:
        textdata = f.read()

    lines = textdata.split("\n")
    info = [line for line in lines if ('\t' not in line) and (line != '') and ('Contest' not in line)]

    df = pd.DataFrame(np.array(info).reshape(-1, 6), columns=['Platform', 'Sponsor', 'Pot', 'Sloc', 'Starts', 'Ends'])

    df['pot_preprocessed'] = df['Pot'].str.extract('.*\$(\d+,\d+).*')
    df['pot_usd'] = df['pot_preprocessed'].str.replace(',','').astype(float)

    df['sloc'] = df['Sloc'].str.replace(',','').replace('N/A', np.nan).astype(float)
    df['usdc_per_solc'] = df['pot_usd'] / df['sloc']

    df.sort_values(by='usdc_per_solc', ascending=False, inplace=True)
    df.drop_duplicates(subset=['Platform', 'Sponsor'], inplace=True)

    print(f"Best payouts per SLOC:")
    for i, row in df.head(args.number_of_rows).iterrows():
        print(row)

    # print(df[['Platform', 'Sponsor', 'sloc', 'usdc_per_solc', 'pot_usd']].head(args.number_of_rows))
