from plugins.utilities.vault import vault_instance
from typing import Dict


def get_dbt_token() -> str:
    return vault_instance.get_secret("dbt_cloud_api_token")


def get_dbt_account_id() -> str:
    return vault_instance.get_secret("dbt_cloud_account_id")


def get_dbt_message(message: str) -> Dict[str, str]:
    return {'cause': message}


def get_dbt_api_link(job_id: str, account_id: str) -> str:
    return f'accounts/{account_id}/jobs/{job_id}/run/'


def get_dbt_api_link_for_run(account_id: str) -> str:
    return f'accounts/{account_id}/runs/'


def get_dbt_job_id(project_name: str, env: str) -> str:
    return vault_instance.get_secret(f"dbt_cloud_{project_name}_{env}_job_id")


def get_dbt_endpoint_from_xcom(key: str, task_ids: str) -> str:
    account_id = get_dbt_account_id()
    dbt_api_link = get_dbt_api_link_for_run(account_id=account_id)
    return dbt_api_link + f"{{{{ ti.xcom_pull(key={key},task_ids={task_ids}) }}}}"

