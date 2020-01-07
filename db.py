import sqlite3
conn = sqlite3.connect("userInfo.db")
c = conn.cursor()

def getUser(userId):
    c.execute("SELECT * FROM users WHERE id = :id", {"id": userId})
    return c.fetchone()

def updateLevel(level, userId):
    c.execute("UPDATE users SET level = :level WHERE id = :id", {"level": level, "id": userId})
