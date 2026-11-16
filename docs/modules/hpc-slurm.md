---
type: rule
state: current
updated: 2026-11-16
area: modules
applies: opt-in: hpc
summary: "Cluster runs: --slurm and friends, per-job resources in one file, transfer-node fetches, offline compute nodes"
---

# HPC and SLURM

## Decision

**Submission flags** on every verb that can run as a batch job:

- `--slurm` re-serialises the same command (minus `--slurm`) into an sbatch job; resources come
  from `orchestration/configs/slurm_jobs.yaml`, overridable per run with `--slurm-time`,
  `--slurm-mem`, `--slurm-cpus`, `--slurm-qos`, `--slurm-partition`;
- `--dry-run` prints the job instead of submitting it;
- with `--chain`, prerequisite steps run **locally** and only the requested step is submitted.

**Resources** (`slurm_jobs.yaml`): one entry per job key, `<source>.<step>` (or
`<source>.<step>.<phase>`), plus keys for non-source jobs such as assembly; each with time,
memory, CPUs and, where the cluster needs them, QOS and partition.

**Scripts** in `orchestration/scripts/`: SLURM wrappers for maintenance and for fetching on a
transfer node, writing logs to `log/<kind>/<name>/` (documented in `LOGGING.md`). Submit from the
repository root; create the log directory first.

**Networks.** Where compute nodes have no internet:

- large downloads run on the transfer node (a wrapper script), and the result is checked with
  `data summary`;
- small files may go through an HTTP proxy if one is configured; a downloader that ignores proxy
  variables needs a source-level override that uses a proxy-aware client;
- the agent instructions state the constraints.

**Scratch** for large temporary files is a project-level directory (overridable by an environment
variable, pointed at node-local disk when available), not `/tmp`.

## Why

Without a resource file, every submission repeats guesses; without a stated network rule, a
download job fails hours in on a node without internet.

## How

The HPC option adds `slurm_jobs.yaml`, `orchestration/scripts/LOGGING.md` and the network
section of `AGENTS.md`.

## Per-project choices

- The cluster's partitions and QOS names, the transfer node, the proxy.

## Checked by

`--dry-run` in tests of the submission path.
