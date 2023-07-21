# Dataset generation scripts using SLURM

To run the script and check if it is in queue:
```bash
$ sbatch slurm_job_generate_dataset_v0.sh
$ sbatch slurm_job_generate_dataset_v1.sh
$ squeue -u $USER
```

If the script has been interrupted, you can recover the generation from an existing file:
```bash
$ sbatch slurm_job_recover_dataset_v0.sh
$ sbatch slurm_job_recover_dataset_v1.sh
$ squeue -u $USER
```

To stop the script from running:
```bash
$ scancel JOB_ID
```