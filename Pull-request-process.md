Each component/repository (with a few exceptions) has 2 main branches, <strong>dev</strong>and <strong>master</strong>. Whenever a commit is pushed to the <strong>dev</strong>branch, Jenkins will automatically run the unit tests for the repository and if they pass, merge into <strong>master</strong>.

<strong>Features or any changes to the codebase should be done as follows:</strong>

1. Pull latest code in <strong>dev</strong> branch and create a <strong>feature branch</strong> off this.
  * Alternatively, if you want to be sure of working from a good build and don&rsquo;t mind the risk of a harder merge, branch off <strong>master</strong>.
  * If the codebase doesn&rsquo;t have a dev branch, branch off <strong>master</strong>.

2. <strong>Implement</strong> your feature (including any necessary UTs etc). Commits are cheap in git, try to split up your code into many, it makes reviewing easier as well as for saner merging.
  * If your commit fixes an existing issue #123, include the text &ldquo;fixes #123&rdquo; in at least one of your commit messages. This ensures the pull request is attached to the existing issue (<a href="http://stackoverflow.com/questions/4528869/how-do-you-attach-a-new-pull-request-to-an-existing-issue-on-github">http://stackoverflow.com/questions/4528869/how-do-you-attach-a-new-pull-request-to-an-existing-issue-on-github</a>).

3. Once complete, ensure the following <strong>checks</strong> pass (where relevant):
  * All UTs (including coverage and valgrind) pass.
  * Your code builds cleanly into a debian package on the repo server.
  * The resulting package installs cleanly using the clearwater-infrastructure script.
  * The live tests pass.

4. <strong>Push</strong> your feature branch to github.

5. Create a <strong>pull request</strong> using github, from your branch to <strong>dev</strong> (never master, unless the codebase has no dev branch).

6. <strong>Reviewer process:</strong>
  * Receive <strong>notice</strong> of review by Github email, Github notification, or by checking <a href="https://github.com/organizations/Metaswitch/dashboard/issues/assigned?direction=desc&amp;state=open">all your Metaswitch Github issues</a>.
  * Make <strong>markups</strong> as comments on the pull request (either line comments or top-level comments).
  * Make a <strong>top-level comment</strong> saying something along the lines of &ldquo;Fine; some minor comments&rdquo; or &ldquo;Some issues to address before merging&rdquo;.
  * If there are no issues, <strong>merge</strong> the pull request and <strong>close</strong> the branch. Otherwise, <strong>assign</strong> the pull request to the developer and leave this to them.

7. <strong>Developer process:</strong>
  * Await review.
  * <strong>Address</strong> code review issues on your feature branch.
  * <strong>Push</strong> your changes to the feature branch on github. This automatically updates the pull request.
  * If necessary, make a <strong>top-level comment</strong> along the lines of &ldquo;Please re-review&rdquo;, assign back to the reviewer, and repeat the above.
  * If no further review is necessary and you have the necessary privileges, <strong>merge</strong> the pull request and <strong>close</strong> the branch.  Otherwise, make a top-level comment and assign back to the reviewer as above.
