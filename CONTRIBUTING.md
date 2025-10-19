<!-- omit in toc -->
# Contributing to Argenta

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating in it is governed by the
[Argenta Code of Conduct](https://github.com/koloideal/Argenta/blob//CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to .

---

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://argenta.readthedocs.io).

Before you ask a question, it is best to search for existing [Issues](https://github.com/koloideal/Argenta/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/koloideal/Argenta/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (cpython, pip, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

<!--
You might want to create a separate issue tag for questions and include it in this description. People should then tag their issues accordingly.

Depending on how large the project is, you may want to outsource the questioning, e.g. to Stack Overflow or Gitter. You may add additional contact and information possibilities:
- IRC
- Slack
- Gitter
- Stack Overflow tag
- Blog
- FAQ
- Roadmap
- E-Mail List
- Forum
-->

---

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://argenta.readthedocs.io). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/koloideal/Argenta/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
- Stack trace (Traceback)
- OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
- Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
- Possibly your input and the output
- Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to .
<!-- You may add a PGP key to allow the messages to be sent encrypted as well. -->

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/koloideal/Argenta/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Argenta, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://argenta.readthedocs.io) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/koloideal/Argenta/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/koloideal/Argenta/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most Argenta users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution

Unsure where to begin contributing to Argenta? You can start by looking through `good first issue` and `help wanted` issues on our GitHub repository. These are issues that are well-suited for new contributors.

To get started with your first code contribution, please follow these steps to set up your local development environment.

1.  Fork the `Argenta` repository on GitHub.
2.  Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/<YOUR_USERNAME>/Argenta.git
    cd Argenta
    ```
3.  Create and activate a Python virtual environment.
    ```bash
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```
4.  Install the project dependencies, including the development tools.
    ```bash
    pip install -e .[dev]
    ```
5.  Create a new branch for your feature or bug fix. Use a descriptive name, like `fix/login-bug` or `feat/new-widget`.
    ```bash
    git checkout -b your-new-branch-name
    ```
6.  Make your changes! Write your code, and don't forget to add or update tests for your changes.
7.  Run the test suite to ensure everything is working correctly.
    ```bash
    python -m pytest tests
    ```
8.  Commit your changes following our commit message styleguide and push them to your fork.
    ```bash
    git add .
    git commit -m "feat(widget): add the new super widget"
    git push origin your-new-branch-name
    ```
9.  Open a Pull Request from your forked branch to the `main` branch of the official Argenta repository. Provide a clear description of the problem and your solution. Include the relevant issue number if applicable.

### Improving The Documentation

Good documentation is crucial for any project. We use Sphinx to generate our documentation from source files located in the `docs/` directory. We welcome any improvements, from fixing a simple typo to writing a whole new section.

	We support documentation in two languages: Russian and English

To improve the documentation, you can follow a similar workflow as for code contributions:

1.  Ensure your development environment is set up as described in the "Your First Code Contribution" section.
2.  Navigate to the documentation directory.
    ```bash
    cd docs
    ```
3. Make the necessary changes to the **Russian** version of the documentation - ``docs/index.rst`` and ``docs/root/*``
4. To build the documentation locally and see your changes, run:
    ```bash
    make live-ru
    ```
5.  Open `127.0.0.1:8000` in your web browser to preview the generated documentation.
6.  Make your desired changes to the `.rst` or `.md` files in the `docs/source` directory.
7.  After completing the work on the Russian documentation, it is necessary to create an English translation:

	```bash
	make update-langs
	```
8.  After updating the translation template, update the necessary translation files located at ``docs/locales/en/LC_MESSAGES``
8.  Once you are happy with your changes, commit them and open a Pull Request. Use the `docs:` prefix in your commit message.

---

## Styleguides

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for our commit messages. This leads to more readable messages that are easy to follow when looking through the project history and allows for automated changelog generation.

Each commit message consists of a **header**, a **body**, and a **footer**.

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

The `<type>` must be one of the following:

*   **feat**: A new feature for the user.
*   **fix**: A bug fix for the user.
*   **docs**: Documentation only changes.
*   **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc).
*   **refactor**: A code change that neither fixes a bug nor adds a feature.
*   **perf**: A code change that improves performance.
*   **test**: Adding missing tests or correcting existing tests.
*   **chore**: Changes to the build process or auxiliary tools and libraries.

#### Examples

A simple fix:
``fix: correct typo in user authentication flow``

A new feature with a scope: 
``feat(api): add new endpoint for user profiles``

---

## Join The Project Team

We are always looking for enthusiastic and dedicated people to join our project team. If you are a regular contributor and have shown a deep understanding of the project's goals and architecture, you might be a good candidate to become a maintainer.

Active members of the community can become team members. This typically involves:

*   Consistently contributing high-quality code and documentation.
*   Helping other users by answering questions and triaging issues.
*   Reviewing Pull Requests from other contributors with constructive feedback.

If you are interested in becoming a more permanent part of the team, the best way to start is by being an active and helpful member of the community. The existing maintainers will notice your efforts and may reach out with an invitation to join the team.