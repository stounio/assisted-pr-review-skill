# Assisted Pull Request Review Skill

The reviewer drives the review by asking questions about the change and refining them to dig into specific aspects; the agent answers each question with evidence from the diff and the codebase. The verdict stays with the reviewer.

## Contents

- [`skills/assisted-pr-review/SKILL.md`](skills/assisted-pr-review/SKILL.md): the review flow.
- [`skills/assisted-pr-review/QUESTIONS.md`](skills/assisted-pr-review/QUESTIONS.md): the typical review questions, grouped by the area a change touches (API, Public API, implementation, endpoints, data types, database migrations, events and messages, dependencies, tests, frontend).

## Install (Claude Code)

Link the skill into your personal skills folder:

```bash
ln -s "$(pwd)/skills/assisted-pr-review" ~/.claude/skills/assisted-pr-review
```

Or copy it into a repository's `.claude/skills/` to share it with that project.

## Use

From a clone of the repository under review, run:

```
/assisted-pr-review <branch>
```

`<branch>` is the branch of the pull request under review. For example:

```
/assisted-pr-review feature/new-endpoint
```

The skill uses only git, so it works wherever the repository is hosted. It reads the branch without checking it out.

Once it is running, refine your questions: "which consumers call the updated endpoint?", "is there already a type for this?".

### Pointing the agent at more sources

Anything after the branch is passed to the agent as instructions. Use it to name where the PR description and the ticket live, so the agent reads the intent from them instead of relying on commit messages:

```
/assisted-pr-review <branch> review the changes introduced in this branch for <repository>. The PR <PR number> on <repository host> contains the description for the change. The ticket <ticket reference> on <tracking application> contains the description for the targeted outcome.
```

The agent reaches those sources with whatever tools it has access to (a CLI or connector for the repository host or tracking application). When it can't reach one, paste the description instead.

### Invocation

Automatic invocation is disabled: `disable-model-invocation: true` in `SKILL.md` keeps the skill out of the agent's context until you run `/assisted-pr-review`. Asking "help me review this branch" without the command will not load it.

## Extending the questions

Add questions to `QUESTIONS.md` under the matching area, or add a new area heading. The skill picks them up without other changes.
