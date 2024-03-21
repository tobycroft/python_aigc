import tuuz

Table = "ai_qianwen"


def Api_find_byProjectName(project_name):
    return tuuz.Database.Db().table(Table).whereRow('project_name', project_name).find()
