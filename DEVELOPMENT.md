# Local development (frontend only)

Runs the site, celery, the websocket daemon and an HTTP-only nginx on
`http://localhost/`. No judge, no TLS, no certbot — submissions can be created
but will never be graded, which is fine for frontend work.

Requires Docker and Docker Compose. Run everything from the `dmoj/` directory.

## First run

```sh
git submodule update --init --recursive
cd dmoj
./scripts/dev_up      # env files, build, migrate, static files
./scripts/dev_seed    # languages + development dataset
```

`dev_up` copies `environment/*.env.dev` to `environment/*.env` if they don't
exist (these are gitignored), runs `scripts/initialize` to copy
`local_settings.py`, `config.js` and `uwsgi.ini` into the submodule, then starts
`site`, `celery`, `wsevent` and `nginx-dev`.

The production `nginx` and `certbot` services are deliberately **not** started:
they require the Let's Encrypt certificates for `judge.monashaps.com` and bind
ports 80/443 with a TLS-only config. `nginx-dev` (defined in
`docker-compose.dev.yml`, config in `nginx/dev.conf.d/`) replaces them.

## Day to day

```sh
alias dc='docker-compose -f docker-compose.yml -f docker-compose.dev.yml'

dc up -d site celery wsevent nginx-dev
dc restart site            # after editing Python in dmoj/repo/
./scripts/copy_static      # after editing SCSS/JS/templates assets
./scripts/manage.py shell  # or migrate, createsuperuser, ...
dc logs -f site
dc down                    # stop; add -v to also drop the database volume
```

The site code is bind-mounted from `dmoj/repo/` (the `online-judge` submodule),
so edits on disk are picked up by a `restart` — no rebuild needed. Rebuild only
when `requirements.txt` or a Dockerfile changes: `./scripts/dev_up --no-cache`.

## The seed data

`./scripts/dev_seed` loads the `navbar` and `language_small` fixtures, then runs
`manage.py seed_dev_data --wipe` (the command lives in the `online-judge`
submodule at `judge/management/commands/seed_dev_data.py`). It creates:

| | |
|---|---|
| Users | 40 (`user01`..`user40`, password `password`) plus `admin`/`password` superuser |
| Organizations | `dev-onsite`, `dev-first-year`, `dev-beginner` — overlapping membership, read by the scoreboard for badges and the in-person toggle |
| Problems | 16 (`devp01`..`devp16`), all public, all-or-nothing, ordered easiest to hardest (3 to 33 points) |
| Contests | `devcon1` Novice (default format) and `devcon2` Open (ICPC format) — 5 hours, concurrent, 14 days ago, both finished |
| Contest problems | 10 each: `devp01`–`devp10` (Novice) and `devp07`–`devp16` (Open), overlapping on `devp07`–`devp10` |
| Entrants | Split between the two divisions, nobody in both; ~5% sat out |
| Submissions | ~550: mostly across the first four hours, ~20% in the final hour, plus 120 practice submissions outside contest time |

Submissions are written pre-graded (AC or a failure verdict — no partial
scores) with test cases and source code, so scoreboards, rating graphs, user
points and problem statistics are all populated. Nothing is ever queued to a
judge.

Each entrant gets a skill level and solves from the easy end of the set
outwards, attempting a problem or two beyond it. Solve counts therefore fall
off along the problem order and the scoreboard reads as a staircase. Harder
problems also take more attempts and land later, which is what fills the final
hour.

On top of that, some runs have their deciding attempt deliberately pushed into
the final hour, weighted towards problems the entrant is marginal on (see
`LATE_FINISH_CHANCE` in the seed command). That is what makes the frozen
scoreboard at `/scoreboard/dev` worth revealing: around 20% of submissions land
in the freeze and each division has a dozen or so solves hiding behind it, so
teams genuinely move when an admin steps the reveal.

Useful flags: `--seed N` (different random data), `--users N`, `--problems N`,
`--no-rate` (skip rating calculation), `--no-admin`.

Re-seeding is destructive but scoped: `--wipe` deletes contests `devcon1`/
`devcon2`, problems starting with `devp`, and users starting with `user` —
including any of your own accounts that start with `user`.

## Gotchas

- Keep `nginx-dev` on port 80. The site derives websocket URLs from `HOST`
  without a port, so live updates break if you publish it elsewhere.
- `DEBUG=1` is set in `site.env.dev`; `ALLOWED_HOSTS` is `localhost`, so use
  `http://localhost/`, not `127.0.0.1`.
- Never commit `environment/*.env` — they are gitignored, and production values
  come from GitHub Actions secrets.
- `ninjaclasher/dmoj-base|site|celery|wsevent` also exist on Docker Hub, are
  amd64-only and are years out of date. If a build fails, `up` will happily pull
  those instead, and you get confusing errors like `ModuleNotFoundError: No
  module named 'pagedown'` plus a platform-mismatch warning on Apple Silicon.
  The dev overlay pins these services to `pull_policy: build`. If you already
  have the pulled versions, delete them:

  ```sh
  docker image rm -f ninjaclasher/dmoj-base ninjaclasher/dmoj-site \
      ninjaclasher/dmoj-celery ninjaclasher/dmoj-wsevent
  ```
