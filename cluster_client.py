from kubernetes import client, config


def get_k8s_api(cluster_config: dict):
    """
    Returns a Kubernetes CustomObjectsApi client
    regardless of authentication method.
    """

    if cluster_config["type"] == "kubeconfig":
        config.load_kube_config(config_file=cluster_config["kubeconfig"])
        return client.CustomObjectsApi()

    elif cluster_config["type"] == "serviceaccount":
        configuration = client.Configuration()

        configuration.host = cluster_config["server"]
        configuration.verify_ssl = True
        configuration.ssl_ca_cert = cluster_config["ca_cert"]
        configuration.api_key = {
            "authorization": f"Bearer {cluster_config['token']}"
        }

        api_client = client.ApiClient(configuration)
        return client.CustomObjectsApi(api_client)

    else:
        raise ValueError(f"Unsupported auth type: {cluster_config['type']}")
