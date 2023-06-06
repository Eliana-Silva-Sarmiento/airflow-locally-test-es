### Branching Flow Overview
- Short-lived `Feature` branches were created from the `Main` branch based on the Jira tickets.
- `Feature` branches then merged with the `Staging` branch through ***PR(Note: Don’t pull staging changes to feature branch).***
- Once all the required tasks were tested at the `Staging`, the `Feature` branch will be merged to the `Production` branch through PR.

![branching_model_diagram](https://github.com/CondeNast/astrocloud-template/blob/main/branching_model/branching_model_diagram.png)
### Branching Flow and Steps to Follow
- Each Jira issue has its own application `short-lived Feature branch` which is created from the `Main branch` with the name of that Jira ticket. `(Ex: GDE-1234 or feature/GDE-1234 or feature-GDE-1234)`

- Once the application code changes are done in the `local Feature branch`, push it to the `remote Feature branch`. Before that pull the changes from the `remote application feature branch` to get the changes made by other developers if multiple developers work on the same feature branch.
```
        $ git branch
        $ git checkout <application branch1>
        $ git pull origin <application branch1>
        # Do the code changes and then run below commands
        $ git add -A
        $ git commit -m “commit message”
        $ git pull origin <application branch1>
        $ git push origin <application branch1>
        
```

- After the code changes were tested in the Feature branch and If everything is ok at the development level then code changes migrated to the Staging branch through PR. Pr creation will trigger the `pylinting` as part of CI.

- Code changes merged to Staging once the PR has been approved. This code merge will trigger a GitHub Action which will do `staging deployment` and create a `new tag`.

- New tag having the Feature branch name as a prefix `(Ex: GDE-1234-v1.0 or feature/GDE-1234-v1.0)`

- If the Feature branch is new then the tag version would be `v1.0`. If the Feature branch is already existing with the latest tag version v1.4 then the new tag would be like `GDE-1234-v1.5`.

- Staging approved code will be pushed to the `Production branch` from the `Feature branch` through PR.

- Once PR has been created against the `Production` branch, the Github Action will be triggered and it will compare the contents of files in PR by getting the code changes in a respective Feature branch and the feature branch’s latest tag commit in the Staging branch.

- If the file content differs then the slack notification will be sent to the team’s slack channel.

- Once PR is approved and merged to `Production branch` it will trigger a Github action which will do `production deployment`.

- Once the production testing is completed and production code is fine then that application team should merge the code to the `Main` branch manually.

- If anything went wrong in the `production deployment` and decided to `rollback the current deployment` then we can trigger the `manual rollback deployment` workflow, which can deploy `Main branch` code into production environment.

### Best Practices
- Developers who are working on one particular `Jira issue` then he/she should use the corresponding Feature branch.

- If the `same developer` is working on two tickets then he/she should use the appropriate Feature branches.

- Pull the remote changes of the corresponding Feature branch before starting work on that Feature branch.

- Also before pushing local changes to the remote Feature branch, the developer should `pull the latest changes` of Feature branch to local.

- If any `code conflicts` occur in the Feature branch while pulling remote changes from the Main branch or pushing local changes to the remote Feature branch then developers should resolve those conflicts in the Feature branch itself.

- Every correction on existing code should be corrected from the Feature branch itself.

- Every fortnight Staging branch will be `refreshed` using the Main branch.

### Things to Avoid
- Don't pull changes from `staging to Feature branches` at any cost to `prevent corruption` of the Feature or Main branch from some unapproved code changes in the Staging branch.

- Before approving PR against the Main branch, the `reviewer’s comment` needs to be checked for file changes in PR. This will `prevent direct PR` against the Main branch from the feature branch.
