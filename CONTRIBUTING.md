# Contributing

## How to contribute

### Issue lifecycle

  1. We use two qualifiers, 
      - "Issue Type" ("Bug", "Feature", or "Enhancement"), and
      - "Lifecycle Status" ("Needs Triage", "Assigned", "Closed").
  1. Start by labeling the issue as "Proposal" and either "Bug", "Feature", or "Enhancement"
  1. During the biweekly grooming session the issue will be either labeled "Accepted" or left as a "Proposal" or "Closed".
  1. Every issue that is in the "Assigned" stage must have an associated pull request as soon as work is started.
  1. Every issue without an associated Pull Request is a candidate to be pruned.
  1. Lifecycle is tracked by the associated pull request after work is begun.
  1. When a pull request has a final status, that status should also be added to the Issue so it can be filtered easily.

### Pull request guidelines

#### Code Review

Never review more than 400 lines of code in one sitting. If you find yourself zoning out, take a break. Never just hit 
"Approve" without a comment.

#### Branch naming

All development branches should be named for the issue in progress, e.g.

```
I-3-classical-field-analog-documentation
```

`I` stands for "Issue" and 3 is the issue number. 

#### Commit messages

Commit messages should be meaningful and use markdown format when formatting is useful. Except
for the first line they should not be a restatement of the branch name or ticket title.

The first line should be a title. Skip a line. The body should describe new features/fixes/enhancements
and their impact on the code base as a whole.

Each pull request should be linked to it's corresponding issue.

#### Branch lifecycle

Development goes like this:

  1. Pick up an issue, label it "Assigned"
  1. Ensure the issue type matches what it actually is
  1. Create a new branch from `main` 
  1. Push that (empty) branch to github with a meaningful commit message.
  1. Link your issue and branch together
  1. REBASE. EVERY. DAY. Regardless of whether or not you do actual work on your branch. Do this first thing.
  1. Do work
  1. Annotate your request with comments on areas critical to review and overall context
  1. Mark your pull request "Needs Review"
  1. Reviewer reviews, marks as "Request Changes", "Comment", or "Approved" using the pull request dialog (not issue labels)
  1. Developer addresses feedback/comments
  1. Reviewer runs tests
  1. Reviewer approves or marks "Request Changes"
  1. Once approved, developer merges.

ALWAYS BE REBASING!!!!

## Testing guidelines

Unit tests should cover units of code, and never use the `mock` library, that would make it an integration test.

Integration tests should never call external services, that's what `mock` is for.

Never write new code or touch old code without ensuring there is test coverage for the new and the old code that is 
affected by a feature or change.

Ideally you should write your tests before your write you code, but that's not a requirement.

### Code style

We use `pre-commit` hooks to install our linters as a pre-commit hook. This ensures your code is linted before it can be
committed. This is a requirement for all contributors.

When you attempt to commit and see that it fails, run `git diff` to see what changes were made/linted. If those changes
look OK to you you can just commit from there running `git add . && git commit -a`.

#### C++

##### Dependencies

Note that we use the C++23 standard. That's not available by default on all machines. C++23 requires a minimum of `g++` 11.1.0 if you're operating on linux. If you have information about `clang` please share.

In order to install support for the C++23 standard on your machine, you can use the following commands:

```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install g++-13
```

##### Style

We use the Google style guide. That is the default for the `cpplint` linter, which we also use as a pre-commit hook. You really should install it as a pre-commit hook so that there aren't lots of linter battles down the road. Steps below:

  1. Use `pip` to install the `[dev]` dependencies for this package: `python3 -m pip install .[dev]`. Note that you may need to escape the `.[dev]` part depending on your shell.
  1. Run `pre-commit install` to install those pre-commit hooks defined in ./.pre-commit-config.yaml
  1. Profit!

We will strictly follow the PEP8 guidelines and

  - 4 spaces instead of tabs
  - one space after a comma, none before
  - No additional spaces within parenthesis.
  - Any C++ code should follow the Google style guide.

### Managing Tickets

We use Github issues for this, apply and existing label based on the category of issue. E.g. "Bug", "Feature", 
"Enhancement".

Contributors meet twice a week and do 15 minute backlog grooming/triage session to filter "Proposal"s and remove them 
from the backlog.
