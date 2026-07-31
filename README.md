# kubernetes-database-migrate

Migration job that applies `pymongo` schema/index migrations to the platform's MongoDB databases (`agent`, `multiagent`), run as a Helm post-install/post-upgrade hook Job.

## Contents

- [Usage](#usage)
- [Links](#links)

## Usage

### Local development

Requires `pyenv` with the `pyenv-virtualenv` plugin, and Python 3.12 installed (`pyenv install 3.12.10`).

```bash
pyenv virtualenv 3.12.10 ai-system-database-migrate
pyenv local ai-system-database-migrate
cp .env.example .env
pip install -r requirements.txt
python src/migrate.py
```

### Adding a migration

Add a new `NNN_description.py` file under `src/migrations/<db_name>/`, exporting an `up(db)` function. Migrations run once each, in filename order, and are tracked in that database's `_migrations` collection.

### Build image locally

```bash
nerdctl build -t database-migrate:local -f Containerfile .
```

### Deployment

Deployment is fully automated via ArgoCD (managed in `kubernetes-gitops`), run as the `mongodb` chart's `migrate-job.yaml` hook.

- Push to `dev`/`staging`/`prod` → CI builds and pushes the image to the Cloudfleet registry, tagged with the branch name and commit SHA.
- The `kubernetes-gitops` repo's `helm/apps/mongodb` values are **not** auto-updated by this pipeline yet — the image tag is bumped by hand there today.

### Runtime configuration

| Variable    | Default                    | Description               |
|-------------|-----------------------------|----------------------------|
| `MONGO_URL` | `mongodb://localhost:27017` | MongoDB connection string  |

## Links

- ArgoCD: managed in `kubernetes-gitops`
- MongoDB chart: `kubernetes-gitops` (`helm/apps/mongodb`)
