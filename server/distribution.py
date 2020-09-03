import db, config
import random, threading
from pyexcel_ods import save_data
from collections import OrderedDict

db = db.connect()

class Student():
  def __init__(self, stu_obj):
    self.id = int(stu_obj["id"])
    self.account = str(stu_obj["account"])
    self.password = str(stu_obj["password"])
    self.student_name = str(stu_obj["student_name"])
    self.student_class = str(stu_obj["student_class"])
    self.student_number = str(stu_obj["student_number"])
    self.year = int(stu_obj["year"])
    self.chooses = list(stu_obj["chooses"])
    self._chooses = list(stu_obj["chooses"])
    self.results = list(stu_obj["results"])
    self.enable = int(stu_obj["enable"])
    self.step = int(0)
  def __repr__(self):
    return f'Stduent({self.id}, "{self.account}" "{self.student_name}")'

class Club():
  def __init__(self, club_obj):
    self.id = int(club_obj["_id"])
    self.name = str(club_obj["name"])
    self.max_students = int(club_obj["max_students"])
    self.reject = str(club_obj["reject"])
    self.teacher = str(club_obj["teacher"])
    self.location = str(club_obj["location"])
    self.comment = str(club_obj["comment"])
    self.year = int(club_obj["year"])
    self.student_year = int(club_obj["student_year"])
    self.classification = int(club_obj["classification"])
  def __repr__(self):
    return f'Club({self.id}, "{self.name}" {self.year})'

def distribuiton(student_year: int):
  setting = db.config.find_one({"_id": student_year})
  year = int(setting["year"])
  maxChoose = int(setting["maxChoose"])
  result = []

  # get all clubs data
  clubs = db.clubs.find({
    "year": year,
    "student_year": student_year,
    "enable": True
  })
  clubs = sorted([ Club(club) for club in clubs ], key=lambda x: x.max_students)

  # get all students already had club
  reserve_students = db.students.find({
    "year": student_year,
    "enable": 1,
    "results": {
      "$elemMatch": {
        "year": year
      }
    }
  })
  reserve_students = [ Student(student) for student in reserve_students ]
  
  # decrease max students in clubs
  for i, club in enumerate(clubs):
    clubs[i].max_students -= db.students.find({
      "year": student_year,
      "enable": 1,
      "results": {
        "$elemMatch": {
          "year": year,
          "club": club.id
        }
      }
    }).count()

  # get all students isn't distribution
  students = db.students.find({
    "year": student_year,
    "enable": 1,
    "results": {
      "$not": {
        "$elemMatch": {
          "year": year
        }
      }
    }
  })
  students = [ Student(student) for student in students ]
  
  def process_accept(stu: Student, accept, unaccept, results_object):
    for s in accept:
      if s.account == stu.account:
        stu.results.append({
          **results_object,
          **{
            "step": list(filter(lambda x: x["club"] == results_object["club"], stu.chooses))[0]["step"]
          }
        })
        # print(stu.account, stu.results)
        stu.chooses = []
    for s in unaccept:
      if s.account == stu.account:
        stu.chooses = list(filter(lambda x: x["club"] != results_object["club"], stu.chooses))
    return stu

  while True:
    for i, club in enumerate(clubs):
      def match_filter(stu: Student):
        if stu.student_class[:2] in club.reject:
          return False
        if len(list(filter(lambda r: r["year"] == year, stu.results))):
          return False
        if not len(stu.chooses):
          return False
        chooses = sorted(list(filter(lambda x: x["year"]==year, stu.chooses)), key=lambda x: x["step"])
        if len(chooses) and chooses[0]["club"] == club.id:
          return True
        return False
      if club.max_students == 0:
        def removeFromChooses(stu):
          stu.chooses = list(filter(lambda x: x["club"] != club.id, stu.chooses))
          return stu
        students = list(map(lambda stu: removeFromChooses(stu), students))
        continue
      match_stu = list(filter(match_filter, students))
      if len(match_stu) == 0:
        continue
      random.shuffle(match_stu)
      n = len(match_stu) if len(match_stu) <= club.max_students else club.max_students
      accept = match_stu[:n]
      unaccept = match_stu[n:]
      results_object = {
        "year": year,
        "club": club.id
      }
      clubs[i].max_students -= len(accept)
      students = list(map(lambda stu: process_accept(stu, accept, unaccept, results_object), students))
    print(len(list(filter(lambda x: len(list(filter(lambda y: y["year"] == year ,x.chooses))), students))))
    if len(list(filter(lambda x: len(list(filter(lambda y: y["year"] == year ,x.chooses))), students))) == 0:
      break
  
  random.shuffle(students)
  for i, stu in enumerate(students):
    if len(list(filter(lambda r: r["year"] == year, stu.results))) == 0:
      random.shuffle(clubs)
      for j, club in enumerate(clubs):
        if club.max_students > 0:
          students[i].results.append({
            "year": year,
            "club": club.id,
            "step": -1
          })
          clubs[j].max_students -= 1
          break
    else:
      pass

  clubs = sorted(clubs, key=lambda x: x.id)

  for stu in students:
    results = list(filter(lambda r: r["year"] == year, stu.results))[0]
    db.students.update_one({
      "account": stu.account
    }, {
      "$push": {
        "results": results
      }
    })

  students = db.students.find({
    "year": student_year,
    "enable": 1,
  })
  students = [ Student(student) for student in students ]

  table = OrderedDict()
  data = [["學號", "班級", "姓名", "課程", "錄取志願序", "填寫志願數"]]
  for i, club in enumerate(clubs):
    i = str(i+1)
    def fillinstep(stu: Student):
      step = 0
      try:
        step = int(list(filter(lambda x: x["year"] == year, stu.results))[0]["step"])
      except:
        pass
      stu.step = step
      return stu
    accept = sorted(list(map(fillinstep, list(filter(lambda stu: len(list(filter(lambda r: r["club"] == club.id, stu.results))), students)))), key = lambda s: s.step)
    print(club.name, len(accept))
    data.append([f"{i.zfill(2)} {club.name}"])
    for stu in accept:
      step = stu.step
      if step == 0:
        step = "優先錄取"
      elif step == -1:
        step = "隨機分發"
      data.append([stu.account, stu.student_class, stu.student_name, f"{i.zfill(2)} {club.name}", step, len(list(filter(lambda x: x["year"] == year, stu._chooses)))])
    data.append([])
  table.update({"Sheet 1": data})
  save_data(f"/tmp/{year} {student_year} 屆分發結果.ods", table)

# distribuiton(112)
