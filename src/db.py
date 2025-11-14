import sqlite3

databse='main.db'


def get_student(digital_id):
    con = sqlite3.connect(databse)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM students WHERE digital_id=?", [digital_id])

    r = res.fetchone()

    print(r)
    if not r: return None


    student = {'digital_id':r[0], 'first_name':r[1], 'last_name':r[2], 'midle_name':r[3], 'group':r[4]}

    con.commit()
    con.close()

    return student

def get_teacher(digital_id):
    con = sqlite3.connect(databse)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM teachers WHERE digital_id=?", [digital_id])

    r = res.fetchone()

    if not r: return None


    teacher = {'digital_id':r[0], 'first_name':r[1], 'last_name':r[2], 'midle_name':r[3], 'kafedra':r[4]}

    con.commit()
    con.close()

    return teacher

def get_para(id):
    con = sqlite3.connect(databse)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM schedule WHERE id=?", [id])

    r = res.fetchone()

    if not r: return None


    para = {'id':r[0], 'week':r[1], 'day':r[2], 'num':r[3], 'room':r[4], 'teacher':r[5], 'type':r[6], 'date':r[7], 'discipline':r[8], 'group':r[9]}

    con.commit()
    con.close()

    return para




def get_student_schedule(week, user_id):
    con = sqlite3.connect(databse)
    cur = con.cursor()

    group = get_student(user_id)['group']


    res = cur.execute("SELECT * FROM schedule WHERE week=? AND grop=?", [week, group])

    ras = res.fetchall()

    pnd, vtr, srd, cht, ptn = [], [], [], [], []

    for r in ras:
        teacher = get_teacher(r[5])
        para = {'day':r[2], 'num':r[3], 'room':r[4], 'teacher':teacher, 'type':r[6], 'discipline':r[8], 'group':r[9]}

        if r[2] == 1:
            pnd.append(para)
        elif r[2] == 2:
            vtr.append(para)
        elif r[2] == 3:
            srd.append(para)
        elif r[2] == 4:
            cht.append(para)
        elif r[2] == 5:
            ptn.append(para)

    con.commit()
    con.close()

    return pnd, vtr, srd, cht, ptn

def get_teacher_schedule(week, user_id):
    con = sqlite3.connect(databse)
    cur = con.cursor()

    res = cur.execute("SELECT * FROM schedule WHERE week=? AND teacher=?", [week, user_id])

    ras = res.fetchall()

    pnd, vtr, srd, cht, ptn = [], [], [], [], []

    for r in ras:
        teacher = get_teacher(r[5])
        para = {'day':r[2], 'num':r[3], 'room':r[4], 'teacher':teacher, 'type':r[6], 'date':r[7], 'discipline':r[8], 'group':r[9]}

        if r[2] == 1:
            pnd.append(para)
        elif r[2] == 2:
            vtr.append(para)
        elif r[2] == 3:
            srd.append(para)
        elif r[2] == 4:
            cht.append(para)
        elif r[2] == 5:
            ptn.append(para)

    con.commit()
    con.close()

    return pnd, vtr, srd, cht, ptn

def get_otsenki(user_id, disc_id):
    con = sqlite3.connect(databse)
    cur = con.cursor()

    res = cur.execute("SELECT * FROM journal WHERE student_id=? and disc=?", [user_id, disc_id])

    ots = res.fetchall()

    output = []

    for ot in ots:
        para = get_para(ot[1])
        otsenka = ot[2]
        output.append({'para':para, 'otsenka': otsenka})

    con.commit()
    con.close()

    return output
