---
name: assisted-pr-review
description: Assist a human reviewer through a pull request by answering review questions about the change with evidence from the code.
argument-hint: <branch> [instructions]
disable-model-invocation: true
---

# Assisted PR review

The reviewer drives; you are the reviewer's instrument. They ask questions about the change, you answer each one with **evidence**, and they sharpen the next question from your answer. The **verdict** (approve, request changes, comment) stays with the reviewer.

## 1. Load the change

The reviewer's arguments: `$ARGUMENTS`. The first word is the branch to review; the rest, when present, are the reviewer's instructions for this review, such as where the PR description and the ticket live. When the arguments are empty, ask the reviewer for the branch. The change is compared against the repository's default branch, `origin/HEAD`.

1. `git fetch` so the branches are current; when the branch exists only on the remote, review `origin/<branch>`.
2. Read the change:
   - `git diff --stat origin/HEAD...<branch>` for the changed files.
   - `git diff origin/HEAD...<branch>` for the diff.
   - `git log --format='%h %s%n%b' origin/HEAD..<branch>` for the commit history.
   - `git show <branch>:<path>` for a file's full content on the branch, when the diff alone lacks context.
3. Intent: read the PR description and the ticket from the sources named in the reviewer's instructions, using the tools available to you, then read the commit messages. When a named source is out of reach, or the intent is still unclear, ask the reviewer to paste the description.

The review reads the branch through git without checking it out, so the reviewer's working tree stays untouched.

Done when you can name every changed file and the outcome the change claims to deliver.

## 2. Map the change to review areas

Assign each changed file to one or more areas from [`QUESTIONS.md`](QUESTIONS.md): API, Public API, implementation, endpoint (new or updated), data types, database migrations, events and messages, dependencies, tests, frontend. Which APIs count as _Public_ is a convention of the repository; when nothing in the code or docs settles it, ask the reviewer.

Done when every changed file sits in at least one area.

## 3. Open the review

Give the reviewer:

1. A summary of the change in three to five lines: intent, approach, files touched by area.
2. For each area present, its questions from [`QUESTIONS.md`](QUESTIONS.md), each with a first answer:
   - **Yes / No / Partly / Can't tell**, then one or two lines of reasoning.
   - **Evidence**: `file:line` in the diff or the existing codebase. Questions about existing endpoints, types, patterns or access patterns need a search of the codebase beyond the diff (`git grep <pattern> origin/HEAD`); cite what you found, or the search that found nothing.
   - **Can't tell** when the evidence lives outside your reach (smoke-test results, production traffic, consumer repositories): name what would settle it.
3. The answers that most deserve the reviewer's attention, ranked by risk, as the suggested next questions.

Done when every question for every area present has an answer with evidence or a named gap.

## 4. Drill down

The reviewer refines a question ("which consumers call this endpoint?", "show me where the timestamp is truncated"). Answer each refined question to the same evidence bar, then propose the sharper follow-up it opens. Questions outside [`QUESTIONS.md`](QUESTIONS.md) are welcome; answer them the same way.

Continue until the reviewer reaches a verdict. When the reviewer asks for review comments, draft each one with its `file:line` target, ready for the reviewer to post on the PR.
