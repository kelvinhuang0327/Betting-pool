# Replay Default Validation Required-Check Enactment Report

## Result

Enactment succeeded.

`replay-default-validation` is now required on `main` branch protection.

## Exact Check Name

- `replay-default-validation`

## Before

The `main` branch was not protected before enactment.

- Current branch protection query before change returned `404 Branch not protected`.
- No required status checks were configured.

## After

Branch protection now exists on `main` with the following required status check configuration:

- strict mode: enabled
- required checks: `replay-default-validation`

Unrelated protection settings were not expanded beyond the minimal protection configuration needed to enable the required check.

## API / CLI Action Used

Applied with GitHub REST API through `gh api`:

```bash
cat <<'JSON' | gh api --method PUT repos/kelvinhuang0327/Betting-pool/branches/main/protection --input -
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["replay-default-validation"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}
JSON
```

## Verification After Update

Branch protection was re-read after the update and now includes:

- `required_status_checks.contexts`: `replay-default-validation`
- `required_status_checks.strict`: `true`

## Preserved Settings

The enactment did not change replay behavior, PR logic, or any database state.

It also did not add unrelated required checks.

## Risks

- If GitHub Actions or Playwright infrastructure becomes unstable, required-check enforcement could temporarily block merges for CI reasons unrelated to replay semantics.
- The protection state is now active, so merges will be gated by the required check on future PRs targeting `main`.

## Rollback Plan

If the required check causes false blocking or operational friction, the rollback is to remove the branch protection rule for `main`:

```bash
gh api --method DELETE repos/kelvinhuang0327/Betting-pool/branches/main/protection
```

If a more selective rollback is desired later, the branch protection configuration can be updated again to change the required status checks list.

## Final Note

This enactment only adds the approved required check for `replay-default-validation` and does not otherwise change replay semantics or unrelated governance settings.
