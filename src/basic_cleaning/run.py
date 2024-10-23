#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

# DO NOT MODIFY
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

# DO NOT MODIFY
def go(args):
    
    logger.info('Starting wandb run.')
    run = wandb.init(
        project = 'nyc_airbnb',
        group = 'basic_cleaning',
        job_type="basic_cleaning" 
    )
    run.config.update(args)
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info('Fetching raw dataset.')
    local_path = wandb.use_artifact('sample.csv:latest').file()
    df = pd.read_csv(local_path)
    
    # EDA with arguments passed into the step
    logger.info('Cleaning data.')
    idx = df['price'].between(float(args.min_price), float(args.max_price))
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    # TODO: add code to fix the issue happened when testing the model
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save the cleaned data
    logger.info('Saving and exporting cleaned data.')
    df.to_csv('clean_sample.csv', index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type = args.output_type,
        description = args.output_description
    )
    artifact.add_file('clean_sample.csv')
    run.log_artifact(artifact)
    
# TODO: In the code below, fill in the data type for each argumemt. The data type should be str, float or int. 
# TODO: In the code below, fill in a description for each argument. The description should be a string.
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download raw dataset from W&B, clean it based on the specified price range, and export the cleaned dataset as an artifact.")
  
    parser.add_argument(
        "--input_artifact", 
        type = str,
        help = 'The input artifact containing the raw dataset.',
        required = True
    )
    """
    This is the reference for the dataset needing to be cleaned.
    """

    parser.add_argument(
        "--output_artifact", 
        type = str,
        help = 'The name for the output artifact after cleaning.',
        required = True
    )
    """
    This is the reference that will be used to save the cleaned dataset.
    """

    parser.add_argument(
        "--output_type", 
        type = str,
        help = 'The type for the output artifact, such as "csv."',
        required = True
    )
    """
    This defines the format of the cleaned dataset.
    """

    parser.add_argument(
        "--output_description", 
        type = str,
        help = 'A description of the output artifact.',
        required = True
    )
    """
    This provides details about the cleaned dataset for future reference.
    """

    parser.add_argument(
        "--min_price", 
        type = float,
        help = 'The minimum price to consider when cleaning data.',
        required = True
    )
    """
    Values below this threshold will be removed from the dataset.
    """

    parser.add_argument(
        "--max_price",
        type = float,
        help = 'The maximum price to consider when cleaning data.',
        required = True
    )
    """
    Values above this threshold will be removed from the dataset.
    """

    args = parser.parse_args()

    go(args)
