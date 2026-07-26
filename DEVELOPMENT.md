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
