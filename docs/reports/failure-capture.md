# Failed-run capture, GHA-Dynamics, last 40 runs (2026-10-29)

| Count | Category | Workflow | Step | Owner | Fingerprint |
|---|---|---|---|---|---|
| 12 | cancelled | Build and Deploy | - | human | `621667a05fda` |
| 4 | log-unavailable | Build and Deploy | Install PAC CLI | platform | `eae8f9388687` |
| 3 | log-unavailable | Build and Deploy | Pack Solution | platform | `e1fdeafde899` |
| 2 | cancelled | Build and Deploy | Checkout repository | human | `bffe2a567cb4` |
| 2 | log-unavailable | Build and Deploy | Resolve solution matrix | platform | `eaf7f5b15e41` |
| 2 | log-unavailable | Build and Deploy | - | platform | `d686023b6982` |
| 2 | log-unavailable | Build and Deploy | Checkout repository | platform | `3672dc87fa31` |
| 1 | stalled-run | Build and Deploy | - | workflow | `50176c01f4ed` |
| 1 | log-unavailable | Build and Deploy | Deploy all solutions → FRS | platform | `1103ffc04624` |
| 1 | log-unavailable | Build and Deploy | Set up job | platform | `32bf34a48e38` |
| 1 | log-unavailable | Build and Deploy | Commit source + write pipeline-context.json + push | platform | `8205ca3dc15a` |
| 1 | log-unavailable | Build and Deploy | Reveille | platform | `84f42e8c1baf` |
| 1 | log-unavailable | Build and Deploy | Checkout calling repo | platform | `41cc9753e257` |

## What this tells us

- Most non-cancelled failures show **no log**: GitHub returns HTTP 410 for expired run logs, so after-the-fact triage is impossible. Capture must happen at failure time (`failure-triage.yml`).
- One run is classified `stalled-run`: it lasted about 30 days, most likely waiting on an environment approval (inferred from the duration, not confirmed from logs). Nothing bounds that today; `stale-run-reaper.yml` is the proposed guard.
- Cancellations dominate the history. Check whether `cancel-in-progress` is cancelling deploys mid-flight.
