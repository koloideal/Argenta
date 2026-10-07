.. _root_contributing:

Contributing to the Project
===========================

.. default-role:: code

First of all, thank you for taking the time to contribute! ❤️

We welcome and appreciate any contribution. Please read the relevant section before getting started. This will make it easier for maintainers and make the process smoother for everyone. The community is looking forward to your ideas! 🎉

.. note::

   If you like the project but don't have time to actively contribute, you can support us in other ways:

*   Star the project on GitHub.
*   Write about the project on Twitter or other social media.
*   Reference the project in your repository's `README`.
*   Mention the project at meetups and tell your friends and colleagues about it.

.. _contents:

Contents
--------

* :ref:`Code of Conduct <code-of-conduct>`
* :ref:`I Have a Question <i-have-a-question>`
* :ref:`I Want to Contribute <i-want-to-contribute>`
* :ref:`Reporting Bugs <reporting-bugs>`
* :ref:`Suggesting Enhancements <suggesting-enhancements>`
* :ref:`Your First Code Contribution <your-first-code-contribution>`
* :ref:`Improving Documentation <improving-documentation>`
* :ref:`Style Guides <styleguide>`
* :ref:`Join the Project Team <join-the-project-team>`

.. _code-of-conduct:

Code of Conduct
---------------

This project and all its participants are governed by the :ref:`Argenta Code of Conduct <root_code_of_conduct>`. By participating, you are expected to uphold this code. Please report unacceptable behavior.

-----

.. _i-have-a-question:

I Have a Question
-----------------

.. note::

   Before asking a question, please check the `documentation <https://argenta.wiki>`_.

Search for an answer in existing `Issues <https://github.com/koloideal/Argenta/issues>`_. If you found a similar question but still need clarification, you can comment on it. We also recommend searching the internet for an answer.

If you can't find an answer, create a new `Issue <https://github.com/koloideal/Argenta/issues/new>`_ and provide as much context as possible, including project and platform versions.

We will address your issue as soon as possible.

-----

.. _i-want-to-contribute:

I Want to Contribute
--------------------

.. rubric:: Legal Notice

.. note::

   By contributing to this project, you confirm that you are the author of 100% of the content, have the necessary rights to it, and agree that it may be distributed under the project's license.

.. _reporting-bugs:

Reporting Bugs
--------------

.. rubric:: Before Submitting a Bug Report

A good bug report shouldn't require others to extract additional information from you. Please investigate thoroughly, gather information, and describe the problem in detail. This will help us fix it as quickly as possible.

* Make sure you are using the latest version.
* Make sure the issue is actually a bug and not caused by, for example, using incompatible environment versions. Read the `documentation <https://argenta.wiki>`_ and, if you need support, check out the :ref:`I Have a Question <i-have-a-question>` section.
* Check if there is already a report about your bug in the `tracker <https://github.com/koloideal/Argenta/issues?q=label%3Abug>`_.
* Also search the internet (including `Stack Overflow`) to see if the issue has been discussed outside of `GitHub`.
* Collect information about the bug:
    *   Stack trace.
    *   OS, platform, and version (Windows, Linux, macOS, x86, ARM).
    *   Version of interpreter, compiler, SDK, runtime environment, package manager, etc.
    *   Input data and output received.
    *   Can you reliably reproduce the issue? Does it reproduce on older versions?

.. rubric:: How Do I Submit a Good Bug Report?

.. note::

   Never report security issues, vulnerabilities, or bugs with sensitive information in the public tracker. Use email for this purpose.

We use `GitHub Issues` to track bugs. If you encounter a problem:

* Open a new `Issue <https://github.com/koloideal/Argenta/issues/new>`_. At this stage, you don't need to assign labels to it.
* Explain the expected and actual behavior.
* Provide as much context as possible and describe **reproduction steps** so the issue can be recreated. It's best to isolate it and create a minimal test case.
* Provide the information you collected in the previous section.

Once the issue is created:

* The project team will assign an appropriate label to the issue.
* A team member will try to reproduce the issue. If there are no steps or they don't lead to the result, the team will ask you to provide them and mark the issue as `needs-repro`. Such issues will not be addressed until the problem is reproduced.
* If the issue is reproduced, it will be marked as `needs-fix` (and possibly with other labels, such as `critical`), after which :ref:`anyone willing <your-first-code-contribution>` can take it on.

-----

.. _suggesting-enhancements:

Suggesting Enhancements
-----------------------

This section will help you submit an enhancement suggestion for `Argenta`, **including both new features and minor improvements**. Following these guidelines will help maintainers and the community better understand your idea.

.. rubric:: Before Submitting an Enhancement Suggestion

* Make sure you are using the latest version.
* Carefully read the `documentation <https://argenta.wiki>`_ and make sure the proposed functionality is not already implemented (perhaps through configuration).
* Perform a `search <https://github.com/koloideal/Argenta/issues>`_ to check if this enhancement has been suggested before. If so, add a comment to the existing issue.
* Determine if your idea fits the scope and goals of the project. You will need to convincingly demonstrate its value. We want to see features that will be useful to most users. If your idea targets a narrow audience, consider creating a plugin.

.. rubric:: How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked in `GitHub Issues <https://github.com/koloideal/Argenta/issues>`_.

* Use a **clear and descriptive title** to identify the suggestion.
* Provide a **step-by-step and detailed description** of the proposed enhancement.
* **Describe the current behavior** and **explain what you expected to see instead** and why. You can also mention which alternatives don't work for you.
* **Attach screenshots or videos** that help demonstrate the steps or point to the part the suggestion relates to.
* **Explain why this enhancement would be useful** to most `Argenta` users. You can also point to other projects that have solved this problem and could serve as inspiration.

-----

.. _your-first-code-contribution:

Your First Code Contribution
----------------------------

Don't know where to start? Look at issues labeled `good first issue` and `help wanted` in our `GitHub` repository. They are well-suited for beginners.

To get started, set up a local development environment by following these steps.

#. Fork the ``Argenta`` repository on ``GitHub``.
#. Clone your fork to your local machine:

   .. code-block:: bash

      git clone https://github.com/<YOUR_USERNAME>/Argenta.git
      cd Argenta

#. Create and activate a virtual environment.

   .. code-block:: bash

      # For macOS/Linux
      python3 -m venv .venv
      source .venv/bin/activate

      # For Windows
      python -m venv .venv
      .venv\Scripts\activate

#. Install project dependencies, including development tools.

   .. code-block:: bash

      pip install -e .[dev]

#. Create a new branch for your feature or fix. Use a descriptive name, such as `fix/login-bug` or `feat/new-widget`.

   .. code-block:: bash

      git switch -c your-new-branch-name

#. Make your changes. Write code and don't forget to add or update tests.
#. Run tests to make sure everything works correctly.

   .. code-block:: bash

      python -m pytest tests

#. Commit following :ref:`our style guide <styleguide>` and push the changes to your fork.

   .. code-block:: bash

      git add .
      git commit -m "feat(widget): add the new super widget"
      git push origin your-new-branch-name

#. Open a `Pull Request` from your branch to the `main` branch of the official repository. Provide a clear description of the problem and your solution. Include the related issue number if there is one.

-----

.. _improving-documentation:

Improving Documentation
-----------------------

Good documentation is crucial. We use `Sphinx` to generate it from source files in the `docs/` directory. We welcome any improvements: from fixing a typo to writing a new section.

.. important::

    To encapsulate various commands needed for setting up and running the project, we use ``just``, which also appears in various examples in the documentation, so we recommend you `install it <https://github.com/casey/just#installation>`_

To improve documentation, you can follow a process similar to contributing code:

#. Make sure your development environment is set up as described in the :ref:`Your First Code Contribution <your-first-code-contribution>` section.
#. Navigate to the documentation directory.

   .. code-block:: bash

      cd docs

#. Make changes to the documentation (`docs/index.rst` and/or `docs/root/*`).
#. To build the documentation locally in auto-rebuild mode and see the changes, run:

   .. code-block:: bash

      just live

#. Open `127.0.0.1:8000` in your browser to preview the generated documentation.
#. When the changes are ready, commit and open a `Pull Request`. Use the `docs:` prefix in the commit message.

-----

.. _styleguide:

Style Guides
------------

.. _commits_messages:

**Commit Messages**

We follow the `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`_ specification. This makes the project history more readable and allows automatic changelog generation.

Each commit message consists of a **header**, **body**, and **footer**.

.. code-block:: text

   <type>(<scope>): <subject>

   [optional body]

   [optional footer]

``<type>`` must be one of the following:

* **feat**: A new feature for the user.
* **fix**: A bug fix for the user.
* **docs**: Documentation changes only.
* **style**: Changes that don't affect the meaning of the code (whitespace, formatting, etc.).
* **refactor**: A code change that neither fixes a bug nor adds a feature.
* **perf**: A code change that improves performance.
* **test**: Adding missing tests or correcting existing tests.
* **chore**: Changes to the build process or auxiliary tools and libraries.

.. rubric:: Examples

Simple fix: ``fix: correct typo in user authentication flow``

New feature with scope: ``feat(api): add new endpoint for user profiles``

-----

.. _join-the-project-team:

Join the Project Team
---------------------

We are always looking for enthusiasts to join the team. If you are a regular contributor and have demonstrated a deep understanding of the project's goals and architecture, you may be a good candidate for a maintainer role.

Active community members can become team members. This typically includes:

*   Consistent contributions of quality code and documentation.
*   Helping other users with their questions and issues.
*   Reviewing `Pull Requests` from other contributors with constructive feedback.

If you are interested in becoming a permanent team member, the best way is to be an active and helpful community contributor. Existing maintainers will notice your efforts and may reach out to you.

