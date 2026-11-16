# SLURM logging

Where SLURM's output goes for each kind of job, relative to the project root. Submit from the
project root, and create the log directory first (`log/` is git-ignored).

| Job | Submitted by | Log directory |
|---|---|---|
| Pipeline steps (`--slurm`) | the CLI | `log/<domain>/<source>/` |
| Scripts in this folder | `sbatch orchestration/scripts/<name>.sh` | `log/maintenance/<name>/` |
