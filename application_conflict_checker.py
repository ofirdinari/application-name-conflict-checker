import requests
from kubernetes.client.exceptions import ApiException

import consts
from cluster_client import get_k8s_api

GIT_API = consts.GIT_API


def get_repo_folders(repo_url, token=None):
    """
    Returns a list of folder names in the root of the repo.
    """
    # Parse repo URL
    parts = repo_url.replace(".git", "").split("/")
    user = parts[-2]
    repo = parts[-1]

    url = f"{GIT_API}/repos/{user}/{repo}/contents/"

    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    data = r.json()
    folders = [item["name"] for item in data if item["type"] == "dir"]
    return folders

def repo_has_name_collision(repo_url: str, cluster_name: str, token=None) -> bool:
    """
    Checks if any ArgoCD Application names from this repo already exist in the cluster.
    """
    if cluster_name not in consts.CLUSTERS:
        raise ValueError(f"Unknown cluster: {cluster_name}")

    api = get_k8s_api(consts.CLUSTERS[cluster_name])

    # repo name
    repo_name = repo_url.rstrip(".git").split("/")[-1]

    # get folders from Git API
    folders = get_repo_folders(repo_url, token)

    for folder in folders:
        app_name = f"{repo_name}-{folder}"

        try:
            api.get_namespaced_custom_object(
                group="argoproj.io",
                version="v1alpha1",
                namespace="openshift-gitops",  # adjust if needed
                plural="applications",
                name=app_name
            )
            print(f"❌ Collision found: {app_name}")
            return True

        except ApiException as e:
            if e.status == 404:
                continue
            else:
                raise

    return False
