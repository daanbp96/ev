import os

def run_local() -> str:
    """Detects if the environment is local or running on a cloud platform."""
    if os.getenv("GOOGLE_CLOUD_PROJECT") or os.path.exists("/etc/google-cloud-ops-agent"):
        return False
    else:
        return True