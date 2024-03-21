import tuuz.Database

Table = "ai_qianwen"


def Api_find_byProjectName(project_name):
    return tuuz.Database.Db().table("ai_qianwen").whereRow('project_name', project_name).find()
