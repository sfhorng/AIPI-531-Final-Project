import argparse
import os
import subprocess
from item import ItemFeatures
from preprocess_and_split import DataPreparation
from popularity import Popularity
from replay_buffer import ReplayBuffer

def parse_args():
    parser = argparse.ArgumentParser(description='Set up before using SNQN')

    parser.add_argument('--data_directory', nargs='?',
        help='data directory for the H&M dataset')

    parser.add_argument('--num_total_sessions', nargs='?',
        help='number of total sessions, or customer IDs')
    return parser.parse_args()

def main():
    args = parse_args()
    data_directory = args.data_directory
    num_total_sessions = int(args.num_total_sessions)

    # Download data to directory
    # download_file_path = os.path.abspath(
    #   os.path.join(data_directory, '..', 'src/download.sh'))
    # subprocess.call([download_file_path, data_directory])

    item_features = ItemFeatures(data_directory)

    #Retrieve item properties df
    item_properties_df = item_features.create_df()

    # Create sorted events
    data_preparation = DataPreparation(data_directory)

    # Retrieve total number of items for statistics dictionary
    num_total_items, item_encoder, item_ids_from_events = data_preparation.preprocess(num_total_sessions, item_properties_df)

    # Split sorted events into training, validation, and test sessions
    data_preparation.split()

    # Create item features
    item_features.create_features(item_properties_df, item_encoder, item_ids_from_events)
    
    # Create popularity dictionary
    popularity = Popularity(data_directory)
    popularity.create()

    # Create replay buffer
    replay_buffer = ReplayBuffer(data_directory)
    replay_buffer.create(num_total_items)

if __name__ == '__main__':
    main()