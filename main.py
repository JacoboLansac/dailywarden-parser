import numpy as np
import pandas as pd
import argparse
from tabulate import tabulate


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-nr', '--number-of-rows', default=10, type=int)
    args = parser.parse_args()

    with open("email", 'r') as f:
        textdata = f.read()

    lines = textdata.split("\n")
    info = [line for line in lines if ('\t' not in line) and (line != '') and ('Contest' not in line)]

    df = pd.DataFrame(np.array(info).reshape(-1, 6), columns=['Platform', 'Sponsor', 'Pot', 'Sloc', 'Starts', 'Ends'])

    # Processing text columns into numeric stuff
    df['pot_preprocessed'] = df['Pot'].str.extract('.*\$(\d+,\d+).*')
    df['pot_usd'] = df['pot_preprocessed'].str.replace(',','').astype(float)
    df['sloc'] = df['Sloc'].str.replace(',','').replace('N/A', np.nan).astype(float)
    df['usdc_per_solc'] = df['pot_usd'] / df['sloc']
    df['Ends'] = df['Ends'].str.replace('⏰', '')
    df['Starts'] = df['Starts'].str.extract('(\d+ \w+)')
    df['Ends'] = df['Ends'].str.extract('(\d+ \w+)')
    df.drop_duplicates(subset=['Platform', 'Sponsor'], inplace=True)

    # Sorting and displaying
    df.sort_values(by='usdc_per_solc', ascending=False, inplace=True)
    df['Sponsor'] = df['Sponsor'].str.slice(0, 40)

    print(f"Best payouts per SLOC:")
    display_table = df[['Platform', 'Sponsor', 'sloc', 'usdc_per_solc', 'pot_usd', 'Starts', 'Ends']].head(args.number_of_rows)
    print(tabulate(display_table, headers='keys', tablefmt='psql'))
