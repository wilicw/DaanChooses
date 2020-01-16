import db, config
import random
from pyexcel_ods import save_data
from collections import OrderedDict

db = db.connect()
year = config.year()
setting = db.config.find_one({"id": 0})
maxChoose = int(setting["maxChoose"])
result = []
allclubs = db.clubs.find({"year": int(year)})
count = 0

db.students.update_many({}, {
        "$pull":{
            "results": {
                    "year": year
            }
        }
    })
  
for club in allclubs:
    obj = {
      "id": club["id"],
      "name": club["name"],
      "max": club["max_students"],
      "students": []
    }
    result.append(obj)

for i in range(1, maxChoose+1):
  for index, club in enumerate(result):
    stus = db.students.find({
      "$and": [
        {
          "chooses": {
            "$elemMatch": {
              "club": int(club["id"]),
              "step": int(i)
            }
          }
        },
        {
          "results": {
            "$not": {
              "$elemMatch": {
                "year": year
              }
            }
          }
        },
        {
          "enable": 1
        }
      ]
    })
    stus = list(stus)
    random.shuffle(stus)
    for stu in stus:
      if result[index]["max"] > 0:
        id = stu["account"]
        result[index]["students"].append({
          "name": stu["student_name"],
          "class": stu["student_class"],
          "account": id,
          "step": i,
          "chooses": maxChoose
        })
        db.students.update_one({"account": id}, {
          "$push": {
            "results": {
              "club": int(club["id"]),
              "year": year,
              "step": i
            }
          }
        })
        result[index]["max"] -= 1
        count += 1

print(count)

for index, club in enumerate(result):
  if club["max"] == 0:
    continue
  stus = db.students.find({
    "$and": [
      {
        "results": {
          "$not": {
            "$elemMatch": {
              "year": year
            }
          }
        }
      },
      {
        "enable": 1  
      }
    ]
  })
  err = 0
  if stus != None and result[index]["max"] > 0:
    for stu in stus:
      if result[index]["max"] == 0:
        break
      result[index]["students"].append({
        "name": stu["student_name"],
        "class": stu["student_class"],
        "account": stu["account"],
        "step": -1,
        "chooses": 0
      })
      db.students.update_one({"account": stu["account"]}, {
        "$push": {
          "results": {
            "club": int(club["id"]),
            "year": year,
            "step": -1
          }
        }
      })
      result[index]["max"] -= 1
      count += 1

#print(result)
print(count)

data = [["學號", "班級", "姓名", "課程班別", "志願填寫", "錄取志願"]]
table = OrderedDict()
for item in result:
  data.append([item["name"]])
  for stu in item["students"]:
    data.append([stu["account"], stu["class"], stu["name"], item["name"], "填寫{}志願".format(stu["chooses"]), "第{}志願".format(stu["step"])])
  data.append([])

table.update({"Sheet 1": data})
save_data("/home/wilicw/Downloads/tables.ods", table)