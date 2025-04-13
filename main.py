import time
from logic import githubManipulations, stylesheetManipulations, authenticate_github, list_repositories

#authenticate_github()
#g = authenticate_github()
#list_repositories(g)

filename    = "input_files/test_formatted_expert_assignments.xlsx"
sheetOPS    = stylesheetManipulations(filename)
githubOPS   = githubManipulations()
auth        = githubOPS.authenticate_github()

table_columns   = sheetOPS.columnHeader()
table_rows      = sheetOPS.tableRows()
print("table_columns: ", table_columns, "\n")
#print("table_rows: ", table_rows)
for row in table_rows:
    print(type(row))
    print(row["No."])
    print(row["Setup Instructions"], type(row["Setup Instructions"]))
    try:
        title = row["Assignment Title"].replace("Expert ", "")
        title = title.replace(" System", "")
        description = row["Objective"]
        #print(title)
        #print("row: ", row)
        readme = sheetOPS.generate_readme(row)
        #print("readme: ", type(readme))
        createRepo = githubOPS.create_new_repository(auth, title, description, readme)
    except:
        pass
    for column in table_columns:
        #createRepo = githubOPS.create_new_repository(auth, row["Assignment Title"])
        #print(column, ": ", row[column], "\n")
        pass
    time.sleep(2)


#repo_list = githubOPS.list_repositories(auth)
#print(repo_list)
#print(auth)#.get_user("imosudi"));# time.sleep(300)
#createRepo = githubOPS.create_new_repository(auth,"test assignment")