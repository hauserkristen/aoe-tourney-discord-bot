# External imports
import os
import json
from pathlib import Path
import pandas as pd


def aggregate_json(json_directory: str, output_json: str):
    json_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(json_directory) for f in filenames if Path(f).suffix == '.json']

    agg_dict = {}
    common_keys = ['drafted', 'played', 'won']
    for jf in json_files:
        # Read json
        with open(jf, 'r') as f:
            data_dict = json.load(f)

        # Join dictionaries
        for bracket, b_dict in data_dict.items():
            if bracket not in agg_dict.keys():
                agg_dict[bracket] = b_dict
            else:
                for round, r_dict in b_dict.items():
                    if round not in agg_dict[bracket].keys():
                        agg_dict[bracket][round] = r_dict
                    else:
                        for k in common_keys:
                            if k in r_dict.keys():
                                if k not in agg_dict[bracket][round].keys():
                                    agg_dict[bracket][round][k] = r_dict[k]
                                else:
                                    if k == 'drafted':
                                        for civ, count in r_dict[k].items():
                                            if civ not in agg_dict[bracket][round][k].keys():
                                                agg_dict[bracket][round][k][civ] = count
                                            else:
                                                agg_dict[bracket][round][k][civ] += count
                                    else:
                                        # Additional map key
                                        for map, m_dict in r_dict[k].items():
                                            if map not in agg_dict[bracket][round][k].keys():
                                                agg_dict[bracket][round][k][map] = m_dict
                                            else:
                                                for civ, count in m_dict.items():
                                                    if civ not in agg_dict[bracket][round][k][map].keys():
                                                        agg_dict[bracket][round][k][map][civ] = count
                                                    else:
                                                        agg_dict[bracket][round][k][map][civ] += count
        print('Done with {}...'.format(jf))

    # Write output 
    with open(output_json, 'w') as outfile:
        json.dump(agg_dict, outfile, indent=4, sort_keys=True)

def generate_round_data(output_json, output_csv):
    # Load data
    with open(output_json, 'r') as f:
        data_dict = json.load(f)

    # Convert to pandas df
    entries = []
    for bracket, b_dict in data_dict.items():
        for round, r_dict in b_dict.items():
            for key, k_dict in r_dict.items():
                if key == 'drafted':
                    for civ, count in k_dict.items():
                        entries.append([bracket, round, key, 'All', civ, count])
                else:
                    for map, m_dict in k_dict.items():
                        for civ, count in m_dict.items():
                            entries.append([bracket, round, key, map, civ, count])
    df = pd.DataFrame(entries, columns=['Bracket', 'Round', 'Type', 'Map', 'Civ', 'Count'])

    # Get data across all brackets
    all_df = df.groupby(['Type', 'Map', 'Civ']).agg({'Count': ['sum']})
    all_df.reset_index()
    print(all_df)

    # Save whole df to file
    df.to_csv(output_csv, index=False)

def main(): 
    directory = 'temp\\Round_4_Stats'
    output_json = 'temp\\agg_02172022.json'
    output_csv = 'temp\\agg_02172022.csv'

    aggregate_json(directory, output_json)
    generate_round_data(output_json, output_csv)

if __name__ == '__main__':
    main()