CLUSTERS = {
    "cluster-test": {
        "type": "kubeconfig",
        "kubeconfig": r"C:\Users\{}\.kube\config", #local path for testing
    },
    "cluster-b": {
        "type": "kubeconfig",
        "kubeconfig": "/kubeconfigs/cluster-b.kubeconfig",
    },

    # Future (service account)
    # "cluster-c": {
    #     "type": "serviceaccount",
    #     "server": "https://api.cluster-c:6443",
    #     "token": "...",
    #     "ca_cert": "/certs/cluster-c.crt",
    # }
}

GIT_API = "https://api.github.com"
REPO_PATH = "https://github.com/ofirdinari/temp-gitops-repo.git"
CHOSEN_CLUSTER = "cluster-test"
TOKEN = ""
