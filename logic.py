"""
GitHub Repository Automation with Python
---------------------------------------
This script demonstrates how to automate common GitHub repository tasks using
the PyGithub library.
"""

# pip install PyGithub

from github import Github
import os
import re
import ast
import base64
from datetime import datetime
import pandas as pd

class stylesheetManipulations(object):
    def __init__(self, filename, *args):
        self.df = pd.read_excel(filename, sheet_name=None)
        super(stylesheetManipulations, self).__init__(*args)
    
    
    def firstSheet(self):
        df = self.df #pd.read_csv('file.csv')
        for name, sheet in df.items():
            #print(f"Sheet: {name}")
            return sheet
         
    def columnHeader(self):
        sheet = self.firstSheet() #pd.read_csv('file.csv')
        list_of_cclumns = sheet.columns.to_list()
        return list_of_cclumns
    
    def tableRows(self):
        sheet = self.firstSheet()        
        # Convert each row to a dictionary
        row_dicts = sheet.to_dict(orient='records')

        return  row_dicts
    
    def generate_readme(self, data_dict):
        """
        Generate a README.md file from specific keys in a dictionary.
        
        Args:
            data_dict (dict): Dictionary containing project information
            
        Returns:
            str: Formatted README.md content
        """
        # List of keys to extract (in order)
        keys = [
            'Assignment Title',
            'Objective',
            'Possible Computational Techniques',
            'Flask UI Component',
            'Types of Dataset',
            'Possible Sources for Dataset',
            'Dataset URLs',
            'Setup Instructions',
            'Implementation Guide'
        ]
        
        # Keys that should be displayed as lists
        list_keys = [
            'Possible Computational Techniques',
            'Flask UI Component',
            'Types of Dataset',
            'Possible Sources for Dataset',
            'Dataset URLs',
        ]
        
        # Start building the README content
        readme_content = []
        
        # Add title if it exists
        if 'Assignment Title' in data_dict:
            readme_content.append(f"# {data_dict['Assignment Title']}\n")
        else:
            readme_content.append("# Project README\n")
        
        # Add other sections
        for key in keys:
            if key == 'Assignment Title':
                continue  # Already handled above
            
            if key in data_dict and data_dict[key]:
                readme_content.append(f"## {key}")
                
                # Format list keys as bullet points
                if key in list_keys and data_dict[key]:
                    # Check if the value is already a list
                    if isinstance(data_dict[key], list):
                        items = data_dict[key]
                    else:
                        # Split by newlines or commas to create list items
                        items = [item.strip() for item in data_dict[key].replace('\n', ',').split(',') if item.strip()]
                    
                    # Add each item as a bullet point
                    for i, item in enumerate(items, 1):
                        readme_content.append(f"{i}. {item}")
                    readme_content.append("")  # Add a blank line after the list
                else:
                    readme_content.append(f"{data_dict[key]}\n")
        
        # Join all sections with newlines
        final_content = "\n".join(readme_content)
        
        return final_content

class githubManipulations(object):
    def __init__(self, *args):
        super(githubManipulations, self).__init__(*args)
    
    def authenticate_github(self):
        """
        Authenticate to GitHub using either a personal access token or username/password.
        Returns a Github object.
        """
        try:
            # Method 1: Using Personal Access Token (recommended)
            # Create token at https://github.com/settings/tokens with appropriate scopes
            token = os.environ.get("GITHUB_TOKEN")
            if token:
                loginUser = Github(token)
                return loginUser
        except:   
            # Method 2: Using username and password (less secure, not recommended for production)
            username = os.environ.get("GITHUB_USERNAME")
            password = os.environ.get("GITHUB_PASSWORD")
            if username and password:
                return Github(username, password)
        
        raise ValueError("GitHub credentials not found in environment variables")
    
    def list_repositories(self, g):
        """List all repositories for the authenticated user."""
        user = g.get_user()
        #print("Your repositories:")
        repo_list = []
        for repo in user.get_repos():
            repo_item = {}
            #print(f"- {repo.name} ({repo.html_url})")
            repo_item[str(repo.name)] = f"{repo.html_url}"
            repo_list.append(repo_item)
        return repo_list
    
    def search_repositories(g, query):
        """Search for repositories based on query."""
        repositories = g.search_repositories(query)
        print(f"Search results for '{query}':")
        for repo in repositories[:10]:  # Limit to first 10 results
            print(f"- {repo.full_name} ({repo.html_url})")
            print(f"  Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
            print(f"  Description: {repo.description}")
            print()

    def create_new_repository(self, auth, repo_name, description, readme, private=False, assignment_details=None):
        """
        Create a new repository for the authenticated user with a structured README.md file.
        
        Parameters:
        - g: Github object (authenticated)
        - repo_name: Name of the repository to create
        - description: Repository description
        - private: Whether the repository should be private
        - assignment_details: Dictionary containing assignment information for the README.md
        """
        #print(auth)
        #auth = 
        user = auth.get_user()
        
        # Create the repository
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            auto_init=False  # We'll create README manually for more control
        )
        print(f"Repository created: {repo.html_url}")
        
        # Create a structured README.md
        if assignment_details is None:
            # Default template if no specific details provided
            assignment_details = {
                "title": "Assignment Title",
                "objective": "Brief description of the assignment objective.",
                "computational_techniques": ["Technique 1", "Technique 2", "Technique 3"],
                "flask_ui": "Description of the Flask UI components required.",
                "dataset_types": ["Type 1", "Type 2"],
                "sources": ["Source 1", "Source 2"],
                "dataset_urls": ["https://example.com/dataset1", "https://example.com/dataset2"],
                "setup_instructions": "Instructions on how to set up the project.",
                "implementation_guide": "Step-by-step guide for implementation."
            }
        
        # Create README content
        readme_content = f"""# {assignment_details.get('title', repo_name)}

    ## Objective
    {assignment_details.get('objective', 'No objective provided.')}

    ## Computational Techniques
    """
        
        # Add computational techniques as list
        
        techniques = assignment_details.get('computational_techniques', [])
        for technique in techniques:
            readme_content += f"- {technique}\n"
        
        # Add remaining sections
        readme_content += f"""
    ## Flask UI Component
    {assignment_details.get('flask_ui', 'No Flask UI details provided.')}

    ## Types of Datasets
    """
        
        # Add dataset types as list
        dataset_types = assignment_details.get('dataset_types', [])
        for dtype in dataset_types:
            readme_content += f"- {dtype}\n"
        
        readme_content += f"""
    ## Sources/Datasets
    """
        
        # Add sources as list
        sources = assignment_details.get('sources', [])
        for source in sources:
            readme_content += f"- {source}\n"
        
        readme_content += f"""
    ## Dataset URLs
    """
        
        # Add dataset URLs as list
        urls = assignment_details.get('dataset_urls', [])
        for url in urls:
            readme_content += f"- [{url}]({url})\n"
        
        readme_content += f"""
           ## Implementation Guide
            {assignment_details.get('implementation_guide', 'No implementation guide provided.')}
            """
        
        # Create the README.md file in the repository
        import base64
        content_encoded = base64.b64encode(readme_content.encode("utf-8")).decode("utf-8")
        repo.create_file(
            path="README.md",
            message="Initial commit: Add structured README.md",
            content=readme
        )
        print(f"README.md created with structured assignment information")
        
        return repo


        
def authenticate_github():
    """
    Authenticate to GitHub using either a personal access token or username/password.
    Returns a Github object.
    """
    try:
        # Method 1: Using Personal Access Token (recommended)
        # Create token at https://github.com/settings/tokens with appropriate scopes
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            return Github(token)
    except:   
        # Method 2: Using username and password (less secure, not recommended for production)
        username = os.environ.get("GITHUB_USERNAME")
        password = os.environ.get("GITHUB_PASSWORD")
        if username and password:
            return Github(username, password)
    
    raise ValueError("GitHub credentials not found in environment variables")

def create_new_repository(g, repo_name, description="", private=False):
    """Create a new repository for the authenticated user."""
    user = g.get_user()
    repo = user.create_repo(
        name=repo_name,
        description=description,
        private=private,
        auto_init=True  # Initialize with README
    )
    print(f"Repository created: {repo.html_url}")
    return repo

def create_file(repo, path, content, commit_message):
    """Create a new file in the repository."""
    # Encode content to base64 as required by GitHub API
    content_encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    repo.create_file(
        path=path,
        message=commit_message,
        content=content_encoded
    )
    print(f"File created: {path}")

def create_branch(repo, branch_name, base_branch="main"):
    """Create a new branch in the repository."""
    # Get the reference to the base branch
    base_ref = repo.get_git_ref(f"heads/{base_branch}")
    # Create new branch from the base branch
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=base_ref.object.sha
    )
    print(f"Branch created: {branch_name}")

def create_pull_request(repo, title, body, head_branch, base_branch="main"):
    """Create a pull request."""
    pr = repo.create_pull(
        title=title,
        body=body,
        head=head_branch,
        base=base_branch
    )
    print(f"Pull request created: {pr.html_url}")
    return pr

def add_collaborator(repo, username, permission="push"):
    """Add a collaborator to the repository."""
    # Permission can be 'pull', 'push', 'admin', 'maintain', or 'triage'
    repo.add_to_collaborators(username, permission)
    print(f"Added {username} as collaborator with {permission} permission")

def set_branch_protection(repo, branch="main"):
    """Set branch protection rules."""
    # Enabling basic branch protection rules
    repo.get_branch(branch).edit_protection(
        required_approving_review_count=1,
        enforce_admins=True,
        dismiss_stale_reviews=True,
        required_status_checks=None,
        user_push_restrictions=None,
        team_push_restrictions=None
    )
    print(f"Branch protection enabled for {branch}")

def list_repositories(g):
    """List all repositories for the authenticated user."""
    user = g.get_user()
    print("Your repositories:")
    for repo in user.get_repos():
        print(f"- {repo.name} ({repo.html_url})")

def search_repositories(g, query):
    """Search for repositories based on query."""
    repositories = g.search_repositories(query)
    print(f"Search results for '{query}':")
    for repo in repositories[:10]:  # Limit to first 10 results
        print(f"- {repo.full_name} ({repo.html_url})")
        print(f"  Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
        print(f"  Description: {repo.description}")
        print()

def automate_workflow_example():
    """Example workflow demonstrating multiple operations."""
    try:
        # Authentication
        g = authenticate_github()
        
        # Create a new repository
        repo_name = f"automated-repo-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        repo = create_new_repository(g, repo_name, "Repository created via PyGithub", private=True)
        
        # Create a Python file
        python_content = """
def hello_world():
    print("Hello, GitHub Automation!")

if __name__ == "__main__":
    hello_world()
"""
        create_file(repo, "hello.py", python_content, "Add hello world script")
        
        # Create .gitignore file
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
.env
venv/
ENV/
"""
        create_file(repo, ".gitignore", gitignore_content, "Add .gitignore for Python")
        
        # Create a feature branch
        create_branch(repo, "feature-update", "main")
        
        # Update hello.py on the feature branch
        updated_content = """
def hello_world():
    print("Hello, GitHub Automation!")
    print("This file was updated through the API")

def another_function():
    return "Adding new functionality"

if __name__ == "__main__":
    hello_world()
    print(another_function())
"""
        # Get the file reference first
        file = repo.get_contents("hello.py", ref="feature-update")
        repo.update_file(
            path=file.path,
            message="Update hello.py with new function",
            content=base64.b64encode(updated_content.encode("utf-8")).decode("utf-8"),
            sha=file.sha,
            branch="feature-update"
        )
        
        # Create a pull request
        create_pull_request(
            repo, 
            "Feature: Update hello script", 
            "This PR adds a new function to hello.py\n\nAutomated via PyGithub", 
            "feature-update"
        )
        
        print("Workflow completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage of the functions
    # Uncomment the ones you want to use
    
    # Simple authentication and repository listing
    #g = authenticate_github()
    #list_repositories(g)
    
    # Search for repositories related to Python automation
    # search_repositories(g, "python automation language:python")
    
    # Run the full automated workflow example
    # automate_workflow_example()
    pass