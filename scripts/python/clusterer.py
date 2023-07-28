import json
import logging
import os
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed

import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from python_log_indenter import IndentedLoggerAdapter
from tqdm import tqdm

warnings.simplefilter("ignore")

load_dotenv()
src = os.getenv("src")

root = os.getenv("root")
sys.path.append(root + "logging/")
from gridTracking_helper import subprocess_scheduler

sys.path.append(src)
sys.path.append(src + "jmapping/selecting/")

from jmap_selector_helper import unpack_policy_group_dir

if __name__ == "__main__":

    logging.basicConfig(format="%(message)s", level=logging.INFO)
    log = IndentedLoggerAdapter(logging.getLogger(__name__))
    load_dotenv()
    root = os.getenv("root")
    src = os.getenv("src")
    JSON_PATH = os.getenv("params")
    if os.path.isfile(JSON_PATH):
        with open(JSON_PATH, "r") as f:
            params_json = json.load(f)
    else:
        print("params.json file note found!")

    dir = "data/" + params_json["Run_Name"] + f"/jmaps/"
    dir = os.path.join(root, dir)
    group_ranks = []
    for folder in os.listdir(dir):
        i = unpack_policy_group_dir(folder)
        group_ranks.append(i)

    # Metric Generator Configuratiosn
    jmap_clusterer = os.path.join(src, "tuning/graph_clustering/jmap_clusterer.py")
    coverage = params_json["coverage_filter"]

    # LOGGING
    log.info("Clustering Graph jmaps!")
    log.info(
        "--------------------------------------------------------------------------------"
    )
    log.info(f"Policy Groups in consideration: {group_ranks}")
    log.info(f"jmap Coverage Filter: {coverage}")
    log.info(
        "--------------------------------------------------------------------------------"
    )
    log.add()

    # Number of loops
    num_loops = len(group_ranks)
    # Running Grid in Parallel
    subprocesses = []
    ## GRID SEARCH PROJECTIONS
    for i in group_ranks:
        subprocesses.append(
            [
                "python",
                f"{jmap_clusterer}",
                f"-n{i}",
                "-s",
            ]
        )

    subprocess_scheduler(subprocesses, num_loops, "SUCESS: Completed JMAP Clustering.", resilient=True)

