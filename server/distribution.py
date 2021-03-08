import db, config
import random, threading
from pyexcel_ods import save_data
from collections import OrderedDict
from dataclasses import dataclass

db = db.connect()


@dataclass
class Student:
    id: int
    account: str
    password: str
    student_name: str
    student_class: str
    student_number: int
    year: int
    chooses: list
    _chooses: list
    results: list
    enable: bool
    step: int = 0


@dataclass
class Club:
    id: int
    name: str
    max_students: int
    reject: str
    teacher: str
    location: str
    comment: str
    year: int
    student_year: int
    classification: int


def obj2club(club_obj):
    return Club(
        int(club_obj["_id"]),
        str(club_obj["name"]),
        int(club_obj["max_students"]),
        str(club_obj["reject"]),
        str(club_obj["teacher"]),
        str(club_obj["location"]),
        str(club_obj["comment"]),
        int(club_obj["year"]),
        int(club_obj["student_year"]),
        int(club_obj["classification"]),
    )


def obj2stu(stu_obj):
    return Student(
        int(stu_obj["id"]),
        str(stu_obj["account"]),
        str(stu_obj["password"]),
        str(stu_obj["student_name"]),
        str(stu_obj["student_class"]),
        str(stu_obj["student_number"]),
        int(stu_obj["year"]),
        list(stu_obj["chooses"]),
        list(stu_obj["chooses"]),
        list(stu_obj["results"]),
        int(stu_obj["enable"]),
    )


def distribuiton(student_year: int, club_year: int, choose_year: int,
                 dist_year: int, writeDB: bool, reject):
    setting = db.config.find_one({"_id": student_year})
    maxChoose = int(setting["maxChoose"])
    result = []

    # get all clubs data
    clubs = db.clubs.find({
        "year": club_year,
        "student_year": student_year,
        "enable": True
    })
    clubs = sorted([obj2club(club) for club in clubs],
                   key=lambda x: x.max_students)
    print(len(clubs), "clubs.")

    # get all students already had club
    reserve_students = db.students.find({
        "year": student_year,
        "enable": 1,
        "results": {
            "$elemMatch": {
                "year": dist_year
            }
        }
    })
    reserve_students = [obj2stu(student) for student in reserve_students]
    print(len(reserve_students), "students had been distributed.")

    # decrease max students in clubs
    for i, club in enumerate(clubs):
        clubs[i].max_students -= db.students.find({
            "year": student_year,
            "enable": 1,
            "results": {
                "$elemMatch": {
                    "year": dist_year,
                    "club": club.id
                }
            },
        }).count()

    # get all students isn't distribution
    students = db.students.find({
        "year": student_year,
        "enable": 1,
        "results": {
            "$not": {
                "$elemMatch": {
                    "year": dist_year
                }
            }
        },
    })
    students = [obj2stu(student) for student in students]
    print(len(students), "students had not been distributed.")

    # filter reject class
    students = list(
        filter(lambda x: (x.student_class[:2] not in reject), students))

    def process_accept(stu: Student, accept, unaccept, results_object):
        for s in accept:
            if s.account == stu.account:
                stu.results.append({
                    **results_object,
                    **{
                        "step":
                        list(
                            filter(
                                lambda x: x["club"] == results_object["club"],
                                stu.chooses,
                            ))[0]["step"]
                    },
                })
                # print(stu.account, stu.results)
                stu.chooses = []
        for s in unaccept:
            if s.account == stu.account:
                stu.chooses = list(
                    filter(lambda x: x["club"] != results_object["club"],
                           stu.chooses))
        return stu

    def result_choose(stu):
        for r in stu.results:
            stu.chooses = list(
                filter(lambda x: x["club"] != r["club"], stu.chooses))

        stu.chooses = list(filter(lambda x: x["club"] != 286, stu.chooses))
        return stu

    students = list(map(result_choose, students))

    while True:
        for i, club in enumerate(clubs):

            def match_filter(stu: Student):
                if stu.student_class[:2] in club.reject:
                    return False
                if len(
                        list(
                            filter(lambda r: r["year"] == dist_year,
                                   stu.results))):
                    return False
                if not len(stu.chooses):
                    return False
                chooses = sorted(
                    list(
                        filter(lambda x: x["year"] == choose_year,
                               stu.chooses)),
                    key=lambda x: x["step"],
                )
                for r in stu.results:
                    if r["club"] == club.id:
                        return False
                if len(chooses) and chooses[0]["club"] == club.id:
                    return True
                return False

            if club.max_students <= 0:

                def removeFromChooses(stu):
                    stu.chooses = list(
                        filter(lambda x: x["club"] != club.id, stu.chooses))
                    return stu

                students = list(
                    map(lambda stu: removeFromChooses(stu), students))
                continue
            match_stu = list(filter(match_filter, students))
            # print(len(match_stu), "students match filter.")
            if len(match_stu) == 0:
                continue
            random.shuffle(match_stu)
            n = (len(match_stu)
                 if len(match_stu) <= club.max_students else club.max_students)
            accept = match_stu[:n]
            print(club.name, len(accept), "accepted")
            unaccept = match_stu[n:]
            results_object = {"year": dist_year, "club": club.id}
            clubs[i].max_students -= len(accept)
            students = list(
                map(
                    lambda stu: process_accept(stu, accept, unaccept,
                                               results_object),
                    students,
                ))
        print(
            len(
                list(
                    filter(
                        lambda x: len(
                            list(
                                filter(lambda y: y["year"] == choose_year, x.
                                       chooses))),
                        students,
                    ))), "left.")
        if (len(
                list(
                    filter(
                        lambda x: len(
                            list(
                                filter(lambda y: y["year"] == choose_year, x.
                                       chooses))),
                        students,
                    ))) == 0):
            break
    print("Start random")
    random.shuffle(students)
    for i, stu in enumerate(students):
        if len(list(filter(lambda r: r["year"] == dist_year,
                           stu.results))) == 0:
            random.shuffle(clubs)
            for j, club in enumerate(clubs):
                if club.max_students > 0:
                    print(club.name, club.max_students)
                    students[i].results.append({
                        "year": dist_year,
                        "club": club.id,
                        "step": -1
                    })
                    clubs[j].max_students -= 1
                    break
        else:
            pass
    print("=========")
    # get all clubs data
    clubs = db.clubs.find({
        "year": club_year,
        "student_year": student_year,
    })
    clubs = sorted([obj2club(club) for club in clubs],
                   key=lambda x: x.max_students)
    clubs = sorted(clubs, key=lambda x: x.id)

    if writeDB:
        for stu in students:
            try:
                results = list(
                    filter(lambda r: r["year"] == dist_year, stu.results))[0]
            except:
                continue
            db.students.update_one({"account": stu.account},
                                   {"$push": {
                                       "results": results
                                   }})
        students = db.students.find({
            "year": student_year,
            "enable": 1,
        })
        students = [obj2stu(student) for student in students]
        students = list(
            filter(lambda x: (x.student_class[:2] not in reject), students))

    table = OrderedDict()
    data = [["學號", "班級", "姓名", "課程", "錄取志願序", "填寫志願數"]]
    for i, club in enumerate(clubs):
        i = str(i + 1)

        def fillinstep(stu: Student):
            step = 0
            try:
                step = int(
                    list(filter(lambda x: x["year"] == dist_year,
                                stu.results))[0]["step"])
            except:
                pass
            stu.step = step
            return stu

        accept = sorted(
            list(
                map(
                    fillinstep,
                    list(
                        filter(
                            lambda stu: len(
                                list(
                                    filter(
                                        lambda r:
                                        (r["club"] == club.id and r["year"] ==
                                         dist_year), stu.results))),
                            students,
                        )),
                )),
            key=lambda s: s.step,
        )
        print(club.name, len(accept))
        data.append([f"{i.zfill(2)} {club.name}"])
        for stu in accept:
            step = stu.step
            if step == 0:
                step = "優先錄取"
            elif step == -1:
                step = "隨機分發"
            data.append([
                stu.account,
                stu.student_class,
                stu.student_name,
                f"{i.zfill(2)} {club.name}",
                step,
                len(
                    list(
                        filter(lambda x: x["year"] == choose_year,
                               stu._chooses))),
            ])
        data.append([])
    table.update({"Sheet 1": data})
    save_data(f"/tmp/{dist_year} {student_year} 屆分發結果.ods", table)


distribuiton(student_year=112,
             club_year=1090101,
             choose_year=1090101,
             dist_year=1090201,
             writeDB=True,
             reject=["餐飲"])
