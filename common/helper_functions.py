import os

def run_local() -> str:
    """Detects if the environment is local or running on a cloud platform."""
    if os.getenv("AZURE_FUNCTIONS_ENVIRONMENT") or os.getenv("WEBSITE_INSTANCE_ID"):
        return False
    elif os.getenv("AWS_EXECUTION_ENV") or os.path.exists("/var/run/secrets/kubernetes.io"):
        return False
    elif os.getenv("GOOGLE_CLOUD_PROJECT") or os.path.exists("/etc/google-cloud-ops-agent"):
        return False
    else:
        return True