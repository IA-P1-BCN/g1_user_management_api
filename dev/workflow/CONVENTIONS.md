# Workflow

How work is specified (Spec-Driven Development with OpenSpec) and how it is tracked (GitHub Project board, Scrum). The split follows the [OpenSpec ↔ Jira mapping](https://www.rushis.com/mapping-openspec-to-jira-sdd-without-abandoning-your-backlog/) (Strategy D, "What/How separation"), translated to GitHub and sized for a small team: **the board coordinates delivery; the spec defines behaviour. If the two disagree, trust the spec.**

## Spec-Driven Development with OpenSpec

[OpenSpec](https://openspec.io) keeps a living spec in the repo under `openspec/`. **No implementation before the spec for that change is approved** — the spec is the contract, the code is provenance.

Lifecycle of a change:

1. **Propose** — `openspec/changes/<change-id>/` gets:
   - `proposal.md` — why, what changes, which capabilities; **header carries `Refs #<story>`**
   - `spec/` — delta specs per capability: what the system **SHALL** do; requirements + Given/When/Then scenarios. This is the behavioral source of truth.
   - `tasks.md` — numbered implementation checklist (stays in git; never mirrored as board issues)
   - `design.md` — only when the change needs technical context (ADRs belong in `docs/adr/` per `docs/dev/agents/domain.md`)
2. **Review** — the proposal is discussed like code (PR or issue), revised, and approved **before implementation starts**. Fixing prose after code exists is expensive.
3. **Implement** — work through `tasks.md` in order using TDD (`docs/dev/backend/CONVENTIONS.md`); check off tasks in the same commit that completes them (conventional commit, `docs/dev/git/CONVENTIONS.md`).
4. **Archive** — `openspec archive` merges the deltas into `openspec/specs/<capability>/`; story moves to Done; the PR links both. **Archived change folders are never deleted** — they are the audit trail.

### OpenSpec ↔ GitHub mapping (Strategy D, small team)

| Artifact | Lives in | Rule |
|---|---|---|
| Epic (business outcome) | **Milestone** | Groups several changes; corresponds to no single repo file |
| Story | **Issue labelled `story`** | **Exactly one** `openspec/changes/<id>/` folder, linked from the story body |
| Detailed behaviour (SHALL, Given/When/Then) | Delta spec in git | Story carries only short stakeholder ACs — the spec is the detailed version |
| `tasks.md` items | git only | **Never** mirrored as `task` sub-issues (one sub-issue per checkbox is an anti-pattern) |
| Genuine sub-pieces | Issue labelled `task`, sub-issue of the story | Only when a piece could **ship, test, and demo on its own** |
| Capability (`openspec/specs/<domain>/`) | Issue **label** (one per domain) | Not an epic; epics never close if they hold living specs |
| Status, sprint, assignee, estimate | Board only | Nothing of this is mirrored in OpenSpec |

### Sizing a change

- A change is describable in **one sentence starting with a verb** — if you need "and", split it.
- More than **~15 tasks** or **~5 requirements** → split into multiple changes.
- Promote a requirement to its own story only if it could ship, test, and demo independently.
- Small fixes that don't change behaviour need no change folder — a plain issue and a PR are fine.

## GitHub Project Board (Scrum)

A GitHub Project (board view) with a **Status** field. Classic-Jira hierarchy mapped onto GitHub:

| Jira concept | GitHub implementation |
|---|---|
| Epic | **Milestone** (one per epic, with a target date) |
| Story | Issue labelled **`story`**, attached to the epic's milestone, linking its change folder |
| Subtask | Issue labelled **`task`**, sub-issue of its story — only for independently shippable pieces |

### Columns (Status)

| Column | Meaning | Change lifecycle |
|---|---|---|
| **Backlog** | Pending items not yet committed to a sprint | — |
| **Sprint Backlog** | Items selected for the current sprint | Change folder created; proposal reviewed → implementation under way (`tasks.md`) |
| **In Review** | Under code review (PR open) | `tasks.md` complete, PR open |
| **Testing** | Being tested for quality (ACs verified, TDD tests green) | PR approved, verifying against spec scenarios |
| **Blocked** | Not moving: missing approval, missing info, or a dependency — the blocker is named in a comment | — |
| **Ready for Deployment** | Done and waiting for release/integration | Merged, awaiting release |
| **Hell** | Entered the sprint but not finished due to complexity | — |
| **Done** | Shipped; ACs met, merged to `main` | Archived: deltas merged into `openspec/specs/` |

> **The Hell rule**: get tasks out of *Hell* fast. A task that sits there for **three sprints** means the problem is the **estimation**, not the task — re-estimate or split it.

### Story format (Scrum)

```
As a <role>, I want <goal> so that <benefit>.

## Acceptance criteria
- [ ] <short stakeholder bullet>
- [ ] <short stakeholder bullet>

**Spec:** openspec/changes/<change-id>/ (SHALL requirements + Given/When/Then scenarios)
```

- ACs on the story are **short stakeholder bullets**; the detailed Given/When/Then lives in the delta spec — a story body as behavioral source of truth is an anti-pattern. Each spec scenario maps to at least one test (TDD).
- A story only enters **Sprint Backlog** after estimation; a story without ACs and a spec link cannot be estimated.
- **Definition of Done**: spec scenarios pass as tests, CI green, PR approved (1 approval, `docs/dev/git/CONVENTIONS.md`), change archived, merged to `main`.

### What stays off the board

`tasks.md` checkboxes, `design.md` contents (link only), detailed Given/When/Then scenarios (summarize as AC bullets). What must be on it: the story, concise ACs, the link to the change folder, status/assignee/sprint.

### Anti-patterns

- One `task` sub-issue per `tasks.md` checkbox
- Story body as the behavioral source of truth
- A milestone (epic) for every small change
- Missing story ↔ change-folder links (both directions)
- Requirements that live only on the board, never in a spec
- Deleting archived change folders
- Mirroring status or estimates into OpenSpec files

### Bootstrap commands

Once the GitHub repo exists (see `docs/dev/agents/issue-tracker.md`):

```bash
gh label create story --description "Scrum story" --color 0e8a16
gh label create task  --description "Independently shippable sub-piece of a story" --color 5319e7
```

Create the Project manually (or via GraphQL), add the **Status** single-select field with the eight columns above, then connect the repo so issues auto-appear. Use the smallest integration that works — no status-mirroring automation.
