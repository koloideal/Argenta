# Security Policy

The Argenta team takes security seriously. We appreciate your efforts to responsibly disclose your findings, and we will make every effort to acknowledge your contributions.

## Supported Versions

This table shows the versions of Argenta that are currently supported with security updates.

| Version | Supported       |
|---------|-----------------|
| 1.3.x   | ✅              |
| < 1.3   | ❌               |

Only the latest minor release line receives security updates. When a new minor version is published, all older release lines stop receiving security fixes — please upgrade to the newest release to stay supported.

## Reporting a Vulnerability

If you believe you have found a security vulnerability in Argenta, please report it to us through one of the following methods:

- **Email**: Send a detailed report to `kolo.is.main@gmail.com`.
- **GitHub Security Advisories**: You can create a new security advisory directly in the Argenta repository: [open a private advisory](https://github.com/koloideal/Argenta/security/advisories/new).

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

To help us understand and resolve the issue quickly, please include the following information in your report:

- A clear and descriptive title.
- The affected version(s) of Argenta.
- A detailed description of the vulnerability.
- Step-by-step instructions to reproduce the issue (a Proof-of-Concept).
- The potential impact of the vulnerability.
- Any suggested mitigations or fixes, if you have any.

You can expect a response from us within 48 hours to acknowledge receipt of your report.

## Disclosure Process

1.  Upon receiving a vulnerability report, we will assign it to a team member and begin our investigation.
2.  We will confirm the vulnerability and determine its severity.
3.  We will work on a patch to address the issue.
4.  Once the patch is ready, we will coordinate with you to schedule a release and a public disclosure. We prefer to disclose vulnerabilities through a GitHub Security Advisory.
5.  We will credit you for your discovery in the advisory, unless you prefer to remain anonymous.

## Secrets Management

- CI workflows use only the ephemeral, per-run `GITHUB_TOKEN`, scoped to the minimum permissions required by each job.
- Long-lived credentials are stored exclusively as GitHub Actions secrets (currently `SCORECARD_TOKEN`, a fine-grained PAT with `Administration: read`, and the PyPI publish token).
- Secrets are never committed to the repository and are not exposed to pull requests from forks.
- PATs are rotated at least on their expiration date and revoked immediately if suspected to be compromised.

## Vulnerability Management Policy

- **Dependencies (SCA)**: every pull request runs `uv audit` against the locked dependency tree; releases are not cut with known critical or high-severity vulnerabilities in dependencies. Dependabot alerts are triaged and fixed before the next release whenever possible.
- **Static analysis (SAST)**: CodeQL runs on every pull request and is a required status check — a change that introduces new CodeQL findings cannot be merged. Findings are remediated before release; suppressions require a written justification in the pull request.
- **Workflows**: all GitHub Actions workflows are linted by Zizmor on every pull request.

## Verifying Releases

Release artifacts are published to [PyPI](https://pypi.org/project/argenta/) by [@koloideal](https://github.com/koloideal) via the automated `release.yml` GitHub Actions workflow.

To verify the integrity of a downloaded artifact, compare its SHA-256 digest with the digest published by PyPI:

```bash
pip download argenta --no-deps -d /tmp/argenta
sha256sum /tmp/argenta/argenta-*.whl
curl -s https://pypi.org/pypi/argenta/json | python3 -c "import json,sys; [print(f['filename'], f['digests']['sha256']) for f in json.load(sys.stdin)['urls']]"
```

The digests listed by PyPI for the release files must match the local `sha256sum` output.

## Security Best Practices

As a user of Argenta, we recommend the following best practices to keep your application secure:

- Always use the latest version of Argenta.
- Regularly scan your project's dependencies for known vulnerabilities.
- If your application handles sensitive data, ensure it is stored and transmitted securely.

## Bug Bounty Program

Currently, we do not have a formal bug bounty program. However, we deeply appreciate the work of security researchers and may offer non-monetary recognition for significant contributions.
