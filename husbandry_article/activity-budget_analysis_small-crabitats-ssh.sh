#!/bin/bash
#SBATCH --job-name=crabs-activity                  # job name
#SBATCH --partition=cpu                            # partition (queue)
#SBATCH --constraint="GenuineIntel-6-79"           # request nodes with AVX2 support
#SBATCH --nodes=1                                  # node count
#SBATCH --mem=8G                                   # total memory per node
#SBATCH --time=0-5:00:00                           # total run time limit (DD-HH:MM:SS)
python activity-budget_small-crabitats.py