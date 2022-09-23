import inquirer

questions = [
        inquirer.List('level', message="Choose level",
                       choices=['Easy', 'Medium', 'Hard'],
            ),
    ]

level = inquirer.prompt(questions)
print(level['level'])
print(type(level))
