# Git Conventions

Three rules that work together: structured commits feed the generated changelog, and the protected `main` branch is the only road to production.

## Conventional Commits

Every commit follows [Conventional Commits v1.0](https://www.conventionalcommits.org/). The changelog automation below parses them — a bad commit type silently disappears from `CHANGELOG.md`.

```
<type>(<scope>)!: <imperative summary ≤ 72 chars, lowercase, no period>

<optional body, wrapped at 100 chars>

<optional footers: Closes #12, BREAKING CHANGE: ...>
```

| Type | Use for | CHANGELOG section |
|---|---|---|
| `feat` | new user-facing feature | Added |
| `fix` | user-facing bug fix | Fixed |
| `perf` | performance improvement | Changed |
| `refactor` / `test` / `build` / `ci` / `chore` / `style` / `docs` | internal, tests, deps, pipeline, tooling, formatting, docs | — (docs → Docs) |

- Breaking change: `!` after type/scope **plus** a `BREAKING CHANGE:` footer.
- Stories/subtasks are referenced with `Refs #<n>` / `Closes #<n>` footers.
- Body explains what and why; the diff already shows how.

## Branch Protection: `main`

`main` is always deployable.

1. **No direct pushes** — PRs only, admins included; force pushes and deletions blocked.
2. **1 approval required** before merge, from someone other than the author.
3. **Stale approvals dismissed** on new pushes; all PR conversations resolved before merge.
4. **Status checks required** once CI lands (see `docs/dev/workflow/CI_CD.md`): lint, type-check, tests.
5. Prefer **linear history**: squash or rebase merges.

Setup via **Settings → Branches → Add branch ruleset**, or once the GitHub remote exists:

```bash
gh api -X PUT repos/{owner}/{repo}/branches/main/protection \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  -f allow_force_pushes=false -f allow_deletions=false \
  -f enforce_admins=true
```

Reviewer rules: PRs for `feat`/`fix` without tests are rejected (see TDD, `docs/dev/backend/CONVENTIONS.md`); hand-edited `CHANGELOG.md` in a PR is rejected (it is generated).

## CHANGELOG Automation

`CHANGELOG.md` is **generated, never hand-edited**. [git-cliff](https://git-cliff.org) regenerates it on every merge to `main` from the conventional-commit history.

`.github/workflows/changelog.yml`:

```yaml
name: changelog
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0          # full history is required
      - name: Generate changelog
        uses: orhun/git-cliff-action@v4
        with:
          config: cliff.toml
          args: --verbose
        env:
          OUTPUT: CHANGELOG.md
          GITHUB_REPO: ${{ github.repository }}
      - name: Commit updated changelog
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add CHANGELOG.md
          git diff --cached --quiet || git commit -m "docs(changelog): update changelog"
          git push
```

`cliff.toml` groups by commit type per the table above (`feat → Added`, `fix → Fixed`, `perf → Changed`, `docs → Docs`) in Keep a Changelog format.

Flow: conventional commit → PR (1 approval, checks green) → merge to `main` → workflow regenerates `CHANGELOG.md` → bot commits it back.

Alternatives if git-cliff is ever dropped: release-please (also versions + releases), python-semantic-release (Python-native).
