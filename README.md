# astrocloud-template
This is a template repository for Astrocloud projects. This README.md 
file should be replaced with a README.md specific to **your new project**.
In addition, in ```.astro/config.yaml```replace ```astrocloud-template``` with
the name of **your Astrocloud project**.
```
project:
  name: <my-super-cool-astrocloud-project>
```


## Recommended repo structure per deployment
Please note that there should be a **single repo per Astrocloud deployment**. Per Astronomer,
having multiple repos in a deployment creates a risk of RACE conditions. It is
acceptable and recommended to have multiple deployments within a single Astrocloud
workspace. Each team should have a single workspace containing multiple
deployments. In addition, each workspace should have a separate deployment
for dev/stg/prod.

## Creating a repo from a template
You will need **read permissions** at minimum to this repository in order to 
create a new repo from the template.

### New repo from template vs. forking
Creating a repo from a template is similar to forking a repo. There are,
however, several differences:
- a fork contains the entire commit history of the parent repo
  - a repo created from a template begins with a single commit
- commits to a fork do not appear **do not** appear in the contributions graph
  - commits to a repo created from a template **do** appear in the contributions graph
- a fork can be a way to contribute code to an existing project
  - a repo created from a template is a way to quickly begin a new project
Please refer to [this article](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) for more information about forks

### Creating a new repo from a template
1. Log into GitHub through Okta and go to the main page of the template repo
2. Click **Use this template**
![Use this template](https://docs.github.com/assets/cb-36544/images/help/repository/use-this-template-button.png)
3. Select the owner of the new repo from the dropdown
![Select owner](https://docs.github.com/assets/cb-23682/images/help/repository/create-repository-owner.png)
4. Enter the name of the new repo and give it a description
![Enter new repo name](https://docs.github.com/assets/cb-25139/images/help/repository/create-repository-name.png)
5. Choose the visibility of the new repo: visibility should be **Internal**
![Select visibility](https://docs.github.com/assets/cb-20877/images/help/repository/create-repository-public-private.png)
6. Click **Create repository from template**

## How to build project locally
This section outlines how to build your Astrocloud project locally.
Building a project locally requires:
- [Docker](https://www.docker.com/products/docker-desktop) to be running
- [Astro CLI](https://docs.astronomer.io/astro/install-cli) to be installed

### Start Docker containers
Run the command `astro dev start`. This will spin up three
Docker containers:
- **Postgres**: Airflow metadata database
- **Webserver**: responsible for Airflow UI
- **Scheduler**: responsible for scheduling and triggering tasks
  - **Triggerer**: responsible for running triggers and
  signaling tasks to resume if/when conditions have been met. 
  The triggerer is used for tasks running with [deferrable operators](https://docs.astronomer.io/astro/deferrable-operators)

The following output should be seen as the project builds:
```
% astro dev start
Env file ".env" found. Loading...
Sending build context to Docker daemon  10.75kB
Step 1/1 : FROM quay.io/astronomer/astro-runtime:5.0.0

# Executing 5 build triggers
---> Using cache
---> Using cache
---> Using cache
---> Using cache
---> Using cache
---> 5160cfd00623
Successfully built 5160cfd00623
Successfully tagged astro-trial_705330/airflow:latest
INFO[0000] [0/4] [postgres]: Starting
INFO[0002] [1/4] [postgres]: Started
INFO[0002] [1/4] [scheduler]: Starting
INFO[0003] [2/4] [scheduler]: Started
INFO[0003] [2/4] [webserver]: Starting
INFO[0004] [3/4] [webserver]: Started
INFO[0003] [3/4] [triggerer]: Starting
INFO[0004] [4/4] [triggerer]: Started
Airflow Webserver: http://localhost:8080
Postgres Database: localhost:5432/postgres
The default credentials are admin:admin
```

Please be aware that the default port for the Airflow webserver
is `8080` and the default port for the Airflow metadata
database is `5432`. These default ports can be changed 
by doing the following:
1. open `.astro/config.yaml`
2. specify desired webserver and/or metadata database ports
```
project:
  name: <my-astro-project-name>
webserver:
  port: 1234
postgres:
  port: 5678
```
3. run `astro dev restart`

### Access the UI
After a successful build, you can navigate to the Airflow UI by going
to `http://localhost:8080/`. Log into the UI with
`username = admin`, `password = admin`.
Once logged in, you should see the DAGs in the `dags` folder in the UI:
![Airflow UI](https://docs.astronomer.io/img/docs/sample-dag.png)

### Automated Astrocloud DAG Deployment Flow
Automation workflows are using the file `workflow_inputs.yml`, which needs to be configured based on the project requirement. Below are the CI/CD workflow files.
```
    development_deployment_caller.yml
    staging_pr_caller.yml
    staging_deployment_caller.yml
    production_pr_caller.yml
    production_deployment_caller.yml
    rollback_deployment_caller.yml
```
***You can remove the*** `branching_model` ***folder once this repo cloned for new astrocloud project***.
### development_deployment_caller.yml
- This workflow will be triggered when the `feature` branch is merged to `development` branch. This will do development environment deployment.

### staging_pr_caller.yml
- Code changes in feature branch will be merged to `staging` branch using Pull Request(PR). If the PR created against staging branch then this workflow will be triggered and code pylinting will happen.

### staging_deployment_caller.yml
- Once the PR against the `staging` branch approved and merged to staging, this workflow will be triggered and staging deployment and `tag` creation will happen.

### production_pr_caller.yml
- Staging branch code tested and certified then the PR will be created against `production` branch. 
- PR creation will trigger this workflow and file comparision happen, the `slack notification` and the `PR review` will be added if any difference in file content compare with `staging`.

### production_deployment_caller.yml
- Once the `production PR` approved and code changes merged to `production` branch, then this workflow triggered and the production deployment will be carried out.

### Production to Main Branch Syncup
- After production environment testing and everything fine in prod development team can do the `production` to `Main` branch syncup.
### rollback_deployment_caller.yml
- If anything went wrong after production deployment and team needs the `rollback` in prod environment we can trigger this workflow manually. This will deploy the previous stable code in `Main` branch to production environment.

### staging_branch_recreation_caller.yml
- Every fortnight the `staging` branch will be recreated either from `main` branch or from `production` branch based on the input provided in the `workflow_inputs.yml` file.
- This will avoid conflicts between `staging` and `production` branches due to separate commit history on them.
- staging_branch_recreation_caller workflow will be executed on `every even week Monday at 8.30 IST`.
- Before branch recreation, one tag will be created from `staging` branch for backup of the current state. Only `5 tags` will be maintained and the remaining old tags deleted on every run.

### stale_branches_deletion_caller.yml
- Unused `stale branches` will be deleted along with their `tags` on `every fortnight` based on the schedule in the workflow.
- Based on the input provided in the `workflow_inputs.yml` file, the number of days the branch has no commit will be considered.
- Branches that are having `no commits` since the day provided in the input file will be deleted.

### workflow_inputs.yml
- It is available in the root of this repo. This YAML file contains inputs for all three environment deployments(development, staging and production).

- This YAML file is mainly used to configure below four dependencies during deployment.
    1. Tardis .whl file
    2. Library repos in Dockerfile are using GitHub Token
    3. Pylinting
    4. Staging branch name
- Tardis .whl File
  - If the project has tardis dependency then we have to provide inputs as,
```  
        need_tardis_whl_file: "yes" or "no"
        tardis_repo_name: condenast/tardis
        tardis_version: "0.1.3"
```
- Pylint:
  - Pylinting inputs would be like,
```
        need_dag_pylint: "yes" or "no"
        dag_path: ./dags/*.py  or ./dags/**/*.py
```
- Library Repos in Dockerfile
```
    github_token_inside_dockerfile: "yes" or "no"
```

### Branching Model
- Feature code changes merging to staging and production branch should follow below branching model to avoid uncertified code change goes to production.

![branching_model_diagram](https://github.com/CondeNast/astrocloud-template/blob/main/branching_model/branching_model_diagram.png)

Read this documentation to know more about the [branching model](https://github.com/CondeNast/astrocloud-template/blob/main/branching_model/branching_model_document.md) 

