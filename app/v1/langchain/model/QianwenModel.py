import tuuz.Database

Table = "ai_qianwen"


def Api_find_byProjectName(project_name):
    return tuuz.Database.Db(self.db).table("ai_qianwen").where('project_name', project_name).find()
