"""
GitHub Repository Automation with Python
---------------------------------------
This script demonstrates how to automate common GitHub repository tasks using
the PyGithub library.
"""

# pip install PyGithub

import os, re, ast, base64
from github import Github
from github import GithubException
from datetime import datetime
import pandas as pd
from roman import toRoman  # Use a small library or custom function for Roman numerals

class stylesheetManipulations(object):
    def __init__(self, filename, *args):
        self.df = pd.read_excel(filename, sheet_name=None)
        self.filename = filename
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
    
    def updateGitHubColumn(self, github_url, assignment_title):
        sheet = self.firstSheet()
    
        # Add "GitHub" column if it doesn't exist
        if "GitHub" not in sheet.columns:
            sheet["GitHub"] = ""

        # Update only the row matching the given assignment title
        sheet.loc[sheet["Assignment Title"] == assignment_title, "GitHub"] = github_url

        # Update the original df with the modified sheet
        for name in self.df:
            self.df[name] = sheet
            break  # Only update the first sheet

        return sheet

    def saveToFile(self, output_filename=None):
        if output_filename is None:
            output_filename = self.filename #.replace(".xlsx", "_with_github.xlsx") 
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            for sheet_name, data in self.df.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        return output_filename
    
    def generate_readme_old(self, data_dict):
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

    def generate_readme_simulations(self, data_dict):
        """
        Generate a clean, properly formatted README.md file
        for simulation-based assignments.

        Args:
            data_dict (dict): Dictionary containing simulation assignment information.

        Returns:
            str: Formatted README.md content.
        """

        # Keys in desired order
        keys = [
            'Assignment Title',
            'Objective',
            'Simulation Type',
            'Types of Dataset',
            'Possible Sources for Dataset',
            'Dataset URLs',
            'Setup Instructions',
            'Implementation Guide',
            'Expected Output(s)',
            'Background Studies'
        ]

        # Keys that should be formatted as bullet point lists
        list_keys = [
            'Types of Dataset',
            'Possible Sources for Dataset',
            'Dataset URLs',
            'Expected Output(s)'
        ]

        # Keys that should be formatted as numbered lists (Arabic numerals)
        numbered_keys = [
            'Setup Instructions',
            'Implementation Guide'
        ]

        readme_content = []

        # Title
        if 'Assignment Title' in data_dict:
            readme_content.append(f"# {data_dict['Assignment Title']}\n")
        else:
            readme_content.append("# Simulation Assignment README\n")

        # Sections
        for key in keys:
            if key == 'Assignment Title':
                continue

            if key in data_dict and data_dict[key]:
                readme_content.append(f"## {key}")

                if key == 'Background Studies':
                    # Structured concept-definition formatting
                    entries = [line.strip() for line in data_dict[key].split('\n') if ':' in line]
                    for entry in entries:
                        term, definition = entry.split(':', 1)
                        readme_content.append(f"### {term.strip()}\n{definition.strip()}\n")

                elif key in numbered_keys:
                    # Treat each line as a full item
                    if isinstance(data_dict[key], list):
                        items = [item.strip() for item in data_dict[key] if item.strip()]
                    else:
                        # Keep newlines as item delimiters
                        items = [item.strip() for item in data_dict[key].split('\n') if item.strip()]

                    for idx, item in enumerate(items, 1):
                        readme_content.append(f"{idx}. {item}")
                    readme_content.append("")

                elif key in list_keys:
                    if isinstance(data_dict[key], list):
                        items = [item.strip() for item in data_dict[key] if item.strip()]
                    else:
                        # Convert newline-separated or comma-separated into list
                        items = [item.strip() for item in data_dict[key].replace(',', '\n').split('\n') if item.strip()]

                    for idx, item in enumerate(items, 1):
                        readme_content.append(f"{idx}. {item}")
                    readme_content.append("")
                else:
                    readme_content.append(f"{data_dict[key]}\n")

        return "\n".join(readme_content)

    def generate_readme(self, data_dict):
        """
        Generate a README.md file from specific keys in a dictionary.
        
        Args:
            data_dict (dict): Dictionary containing project information
            
        Returns:
            str: Formatted README.md content
        """
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

        list_keys = [
            'Possible Computational Techniques',
            'Flask UI Component',
            'Types of Dataset',
            'Possible Sources for Dataset',
            'Dataset URLs',
            'Implementation Guide'
        ]

        readme_content = []

        # Title
        if 'Assignment Title' in data_dict:
            readme_content.append(f"# {data_dict['Assignment Title']}\n")
        else:
            readme_content.append("# Project README\n")

        for key in keys:
            if key == 'Assignment Title':
                continue

            if key in data_dict and data_dict[key]:
                readme_content.append(f"## {key}")

                if key in list_keys:
                    # Ensure value is a list of lines
                    if isinstance(data_dict[key], list):
                        lines = data_dict[key]
                    else:
                        # Split by newline and strip whitespace
                        lines = [line.strip() for line in data_dict[key].splitlines() if line.strip()]

                    # Special handling for Implementation Guide
                    if key == "Implementation Guide":
                        # Filter out section headers like "1. Medical Diagnosis Expert System"
                        step_lines = []
                        for line in lines:
                            if not re.match(r"^\d+\.\s+[A-Z]", line):  # Match titles like '1. Medical Diagnosis...'
                                step_lines.append(line)
                        lines = step_lines

                    # Add numbered list
                    for i, line in enumerate(lines, 1):
                        readme_content.append(f"{i}. {line}")
                    readme_content.append("")
                else:
                    readme_content.append(f"{data_dict[key]}\n")

        return "\n".join(readme_content)


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
            print(f"- {repo.name} ({repo.html_url})")
            repo_item[str(repo.name)] = f"{repo.html_url}"
            repo_list.append(repo_item)
        return repo_list
    
    def search_my_repositories(self, g, query):
        """Search for repositories based on query."""
        #repositories = g.search_repositories(query)
        #print(f"Search results for '{query}':")
        user = g.get_user()
        repo_list = []
        print(user.get_repos())
        for repo in user.get_repos():
            if repo.name == query:
                repo_list.append(repo)
        return repo_list
    
    def search_repositories(self, g, query):
        """Search for repositories based on query."""
        repositories = g.search_repositories(query)
        print(f"Search results for '{query}':")
        for repo in repositories[:10]:  # Limit to first 10 results
            #print(f"- {repo.full_name} ({repo.html_url})")
            #print(f"  Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
            #print(f"  Description: {repo.description}")
            #print()
            pass
        return repositories

    def create_new_repository(self, auth, repo_name, description, readme, filename, private=False, assignment_details=None):
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
        try:
            # Create the repository
            repo = user.create_repo(
                name=repo_name,
                description=description,
                private=private,
                auto_init=False  # We'll create README manually for more control
            )
            print(f"Repository created: {repo.html_url}")
        
        except GithubException as e:
            if e.status == 422 and any(error.get('code') == 'custom' and 
                                    'already exists' in error.get('message', '') 
                                    for error in e.data.get('errors', [])):
                #raise ValueError(f"Repository '{repo_name}' already exists on this account") from e
                return ValueError(f"Repository '{repo_name}' already exists on this account") 
            else:
                # Re-raise other GitHub exceptions
                raise
        # update sheet with repo URL
        sheetOPS    = stylesheetManipulations(filename)
        sheetOPS.updateGitHubColumn(repo.html_url ,repo_name)
        sheetOPS.saveToFile()
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

    def create_python_gitignore(repo):
        """Create Python .gitignore the repository."""
        # Encode content to base64 as required by GitHub API
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
        content_encoded = base64.b64encode(gitignore_content.encode("utf-8")).decode("utf-8")
        repo.create_file(
            path=".gitignore",
            message="Add .gitignore for Python",
            content=content_encoded #gitignore_content
        )
        print(f"File created: .gitignore")
        
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





