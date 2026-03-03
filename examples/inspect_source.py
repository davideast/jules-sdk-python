"""Inspecting detailed source repositories using the Jules SDK.

Usage:
    export JULES_API_KEY=your-key
    python examples/inspect_source.py
"""
from jules import JulesClient
from jules.models import GitHubRepo

def main() -> None:
    with JulesClient() as client:
        print("Finding a source to inspect...")
        sources = list(client.list_sources())
        if not sources:
            print("No sources found. Try running getting_started.py first.")
            return

        target_source = sources[0]
        print(f"\nFetching detailed source: {target_source.name}")

        # In a real app, you might receive the source name from user input
        source = client.get_source(target_source.name)

        print(f"Source ID: {source.id}")

        if source.github_repo:
            repo: GitHubRepo = source.github_repo
            print("\nGitHub Repository Details:")
            print(f"Owner/Repo: {repo.owner}/{repo.repo}")
            print(f"Private: {'Yes' if repo.is_private else 'No'}")

            if repo.default_branch:
                print(f"Default Branch: {repo.default_branch.display_name}")

            if repo.branches:
                print(f"\nFound {len(repo.branches)} total branches.")
                print("Available branches:")
                for b in repo.branches[:5]:  # print up to 5
                    print(f"- {b.display_name}")
        else:
            print("\nThis source is not a GitHub repository.")

if __name__ == "__main__":
    main()
