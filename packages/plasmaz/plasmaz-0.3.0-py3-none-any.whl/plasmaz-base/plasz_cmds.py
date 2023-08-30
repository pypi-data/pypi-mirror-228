class plasz_cmds:
    def __init__(self, github_api, github_events):
        self.github_api = github_api
        self.github_events = github_events

    def create_issue(self, repo, title, body):
        data = {"title": title, "body": body}
        self.github_api.post(f"repos/{repo}/issues", data=data)
        self.github_events.trigger("issue_created", repo, title)

    def list_repositories(self, username):
        repos = self.github_api.get(f"users/{username}/repos")
        for repo in repos:
            print(repo["name"])

    def get_repo_info(self, repo):
        info = self.github_api.get(f"repos/{repo}")
        print(f"Repository: {info['name']}")
        print(f"Description: {info['description']}")
        print(f"Language: {info['language']}")
        print(f"Stars: {info['stargazers_count']}")

    def create_repository(self, name, description):
        data = {"name": name, "description": description}
        self.github_api.post("user/repos", data=data)
        print(f"Repository '{name}' created!")

    def list_issues(self, repo):
        issues = self.github_api.get(f"repos/{repo}/issues")
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']}")

    def close_issue(self, repo, issue_number):
        data = {"state": "closed"}
        self.github_api.patch(f"repos/{repo}/issues/{issue_number}", data=data)
        print(f"Issue #{issue_number} closed!")
