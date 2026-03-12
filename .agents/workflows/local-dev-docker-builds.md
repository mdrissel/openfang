---
description: fast local docker builds and upstream PR branching strategy
---
# Local Development Docker Builds & Branching Strategy

The standard `docker compose up --build` uses production compilation profiles (LTO, 1 codegen unit), which takes a very long time. For local development, we use `docker-compose.override.yml` to speed this up.

## Prerequisites
Ensure that the `dev` branch contains the `docker-compose.override.yml` file with fast build arguments:

```yaml
services:
  openfang:
    build:
      context: .
      args:
        LTO: "false"
        CODEGEN_UNITS: "16"
```

## Creating Upstream PRs without Leaking Overrides
Since `docker-compose.override.yml` is committed to the local `dev` branch, you must ensure it does not leak into upstream pull requests.

### 1. Always branch off `upstream/main` for new PRs.
This guarantees that local development files do not accidentally enter upstream pull requests.

```bash
git fetch upstream main
git checkout upstream/main -b fix/my-new-fix
```

### 2. If you need to test the PR branch locally with fast builds:
You can pull the override file from `dev` directly into your working tree without tracking it for the PR branch.

// turbo
```bash
git checkout dev -- docker-compose.override.yml
```

To prevent accidentally committing it to the PR, add it to the local ignore list:

// turbo
```bash
echo "docker-compose.override.yml" >> .git/info/exclude
```

When you are finished testing and ready to push the PR, you can clean it from your working tree:

```bash
git rm --cached docker-compose.override.yml
git restore docker-compose.override.yml
```
