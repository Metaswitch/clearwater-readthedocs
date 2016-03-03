Pull Request Process
====================

Dev and master branches
-----------------------

Each component/repository (with a few exceptions) has 2 main branches,
``dev`` and ``master``. Whenever a commit is pushed to the ``dev``
branch, Jenkins will automatically run the unit tests for the repository
and if they pass, merge into master\`.

Development process
-------------------

Features or any changes to the codebase should be done as follows:

1. Pull the latest code in the ``dev`` branch and create a feature
   branch off this.

   -  Alternatively, if you want to be sure of working from a good build
      and don't mind the risk of a harder merge, branch off ``master``.
   -  If the codebase doesn't have a dev branch, branch off ``master``.

2. Implement your feature (including any necessary UTs etc). Commits are
   cheap in git, try to split up your code into many, it makes reviewing
   easier as well as for saner merging.

   -  If your commit fixes an existing issue #123, include the text
      "fixes #123" in at least one of your commit messages. This ensures
      the pull request is `attached to the existing
      issue <http://stackoverflow.com/questions/4528869/how-do-you-attach-a-new-pull-request-to-an-existing-issue-on-github</a>>`__.

3. Once complete, ensure the following check pass (where relevant):

   -  All UTs (including coverage and valgrind) pass.
   -  Your code builds cleanly into a Debian package on the repo server.
   -  The resulting package installs cleanly using the
      clearwater-infrastructure script.
   -  The live tests pass.

4. Push your feature branch to GitHub.

5. Create a pull request using GitHub, from your branch to ``dev``
   (never ``master``, unless the codebase has no dev branch).

6. Await review.

   -  Address code review issues on your feature branch.
   -  Push your changes to the feature branch on GitHub. This
      automatically updates the pull request.
   -  If necessary, make a top-level comment along the lines "Please
      re-review", assign back to the reviewer, and repeat the above.
   -  If no further review is necessary and you have the necessary
      privileges, merge the pull request and close the branch.
      Otherwise, make a top-level comment and assign back to the
      reviewer as above.

Reviewer process:
-----------------

-  Receive notice of review by GitHub email, GitHub notification, or by
   checking `all your Metaswitch GitHub
   issues <https://github.com/organizations/Metaswitch/dashboard/issues/assigned?direction=desc&state=open>`__.
-  Make comments on the pull request (either line comments or top-level
   comments).
-  Make a top-level comment saying something along the lines of "Fine;
   some minor comments" or "Some issues to address before merging".
-  If there are no issues, merge the pull request and close the branch.
   Otherwise, assign the pull request to the developer and leave this to
   them.

