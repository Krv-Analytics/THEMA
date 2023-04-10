import os
import argparse
import sys
import pickle
import shutil
from dotenv import load_dotenv
from projector_helper import projection_driver, projection_file_name


# Load Root directory from .env
load_dotenv()
root = os.getenv("root")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=os.path.join(
            root, "data/clean/clean_data_standard_scaled_integer-encdoding_filtered.pkl"
        ),
        help="Select location of local data set, as pulled from Mongo.",
    )

    parser.add_argument(
        "--umap",
        type=bool,
        default=True,
        help="Use UMAP algorithm to compute projection. ",
    )

    parser.add_argument(
        "-n",
        "--neighbors_list",
        type=int,
        nargs="+",
        default=[3, 5, 10, 20, 40],
        help="Insert a list of n_neighbors to grid search",
    )

    parser.add_argument(
        "-d",
        "--min_dists",
        type=float,
        nargs="+",
        default=[0, 0.01, 0.05, 0.1, 0.5, 1],
        help="Insert a list of min_dists to grid search",
    )
    parser.add_argument(
        "--clear",
        type=bool,
        default=True,
        help="Clear directory before generating files",
    )

    parser.add_argument(
        "-v",
        "--Verbose",
        default=False,
        action="store_true",
        help="If set, will print messages detailing computation and output.",
    )

    args = parser.parse_args()
    this = sys.modules[__name__]

    assert os.path.isfile(args.path), "Invalid Input Data"
    # Load Dataframe
    with open(args.path, "rb") as f:
        reference = pickle.load(f)
        df = reference["clean_data"]
    output_dir = os.path.join(root, "data/projections/UMAP/")

    # Clear contents if the directory exists
    if args.clear and os.path.isdir(output_dir):
        if args.Verbose:
            print(f"\n Removing previous projections...\n")
        shutil.rmtree(output_dir)
    # Check if output directory already exists
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if args.umap:
        # Check if output directory already exists

        projection_params = (args.min_dists, args.neighbors_list)
        if args.Verbose:
            print(f"Computing UMAP Grid Search! ")
            print(
                "--------------------------------------------------------------------------------"
            )
            print(f"Choices for n_neighbors: {args.neighbors_list}")
            print(f"Choices for m_dist: {args.min_dists}")
            print(
                "-------------------------------------------------------------------------------- \n"
            )
        projections = projection_driver(df, projection_params)

        for keys in projections.keys():
            output_file = projection_file_name(
                projector="UMAP", keys=keys, dimensions=2
            )
            output_file = os.path.join(output_dir, output_file)

            ## Output Message
            out_dir_message = "/".join(output_file.split("/")[-2:])

            ## Selecting projection to write
            projection = projections[keys]

            output = {"projection": projection, "hyperparameters": keys}
            with open(output_file, "wb") as f:
                pickle.dump(output, f)

            if args.Verbose:
                print(
                    "\n---------------------------------------------------------------------------------- \n"
                )
                print(f"Writing {keys} to {out_dir_message}")
                print(
                    "\n----------------------------------------------------------------------------------"
                )

                print(
                    "\n################################################################################## \n\n"
                )
                print(f"Finished writing UMAP Projections")

                print(
                    "\n\n##################################################################################\n"
                )
    else:
        print(
            f"UMAP is only dimensionality reduction algorithm supported at this time."
        )
        print(f"Please set `--umap` to True.")