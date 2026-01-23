#!/bin/bash
 #SBATCH -p medium
#SBATCH -p gailing
#SBATCH -A gailing_legacy
 #SBATCH -q long
#SBATCH -t 48:00:00
#SBATCH -o outfile-%J
#SBATCH -e errfile-%J
#SBATCH -n 24
#SBATCH -N 1
#SBATCH --ntasks-per-socket 24
#SBATCH --job-name=structure

module purge
module load rev/21.12
module load structure/2.3.4
./runstructure

