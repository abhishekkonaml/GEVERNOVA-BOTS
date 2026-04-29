import subprocess
import sys
from urllib.parse import quote
# repo_url="https://github.apps.gevernova.net/503437104/GEVernova_Ansible"
# auth_url="https://503437104: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@github.com/<owner>/<repo>.git"
def check_repo_access():
    try:

        result = subprocess.run(
            ["git", "ls-remote", auth_url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return "success"
        else:
            return "failure"

    except Exception as e:
        print(str(e))
        return "failure"
    
if __name__ == "__main__":
    # Example usage:
    repo_url = "https://github.com/your-org/your-repo.git"
    pat = "your_personal_access_token"

    status = check_repo_access(repo_url, pat)
    print(status)