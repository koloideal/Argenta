
<a id='changelog-1.3.0'></a>
## 1.3.0 — 2026-10-07

### Added

- A cli module that implements the ability to launch applications on Argenta, run application benchmarks on Argenta, create a boilerplate for new projects, and much more.
- A new `info` command has been added to the Argenta CLI, providing a quick overview of the installed package and runtime environment.

- A `release` CI workflow that builds the package with `uv` and publishes it to PyPI via trusted publishing (OIDC) when a GitHub release is published.

### Changed

- Refactoring the initialization order of some modules; heavy imports are now imported only when necessary, which resulted in a boost to importtime.

- Package metadata in `pyproject.toml`: PEP 639 license fields, Trove classifiers, keywords and project URLs added.
- Dependency bumps: pillow 12.1.0 → 12.2.0, urllib3 2.5.0 → 2.7.0, pygments 2.19.1 → 2.20.0.

### Removed

- The Russian version of the documentation: sources are now English-only and the gettext/`sphinx-intl` pipeline was dropped.

<a id='changelog-1.2.0'></a>
## 1.2.0 — 2026-02-07

### Added

- 100% coverage of the code base with tests
- 100% coverage with typhints
- 100% coverage of public API documentation in two languages - Russian and English
- cli attributes: highlighting valid commands, redesigned input history with auto-completion, interactive autocomplete selection menu for multiple candidates
- a metrics module that allows you to test the performance of various library units
- implementing a dependency injection pattern through an ioc container
- implementation of a context object for transferring data between handlers within a session
- adding a changelog

### Changed

- increased performance by several times (there will be real numbers in the next releases)
- reworking the internal API, highlighting different layers and reducing connectivity
- reworking the README and adding a translation for it
