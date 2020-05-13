import sqlite3

conn = sqlite3.connect("userInfo.db")

# https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

c = conn.cursor()

def getUser(userId, guildId):
    c.execute("SELECT * FROM users WHERE id = :id AND guild_id = :guild_id", {"id": userId, "guild_id": guildId})
    return c.fetchone()

def insertNewUser(userId, guildId, name):
    newUser = {"id": userId, "guild_id": guildId, "name": name, "messages": 0, "level": 0, "is_upgraded": 0, "currency": 0, "datetime_adventure": ""}
    c.execute("INSERT INTO users VALUES (:id, :guild_id, :name, :messages, :level, :is_upgraded, :currency, :datetime_adventure)", newUser)
    conn.commit()
    return newUser

def updateUser(user):
    c.execute("UPDATE users SET name = :name, messages = :messages, level = :level, currency = :currency, datetime_adventure = :datetime_adventure WHERE id = :id AND guild_id = :guild_id", user)
    conn.commit()

def updateUpgradeStatus(userId, guildId, newStatus):
    c.execute("update users SET is_upgraded = :is_upgraded WHERE id = :id AND guild_id = :guild_id", {"is_upgraded": newStatus, "id": userId, "guild_id": guildId})
    conn.commit()

def updateAdventureTiming(userId, guildId, newTiming):
    c.execute("update users SET datetime_adventure = :datetime_adventure WHERE id = :id AND guild_id = :guild_id", {"datetime_adventure": newTiming, "id": userId, "guild_id": guildId})
    conn.commit()


def modifyLevel(userId, guildId, increment):
    c.execute("update users SET currency = currency + :increment WHERE id = :id AND guild_id = :guild_id", {"increment": increment, "id": userId, "guild_id": guildId})
    conn.commit()

def modifyCurrency(userId, guildId, increment):
    c.execute("update users SET currency = currency + :increment WHERE id = :id AND guild_id = :guild_id", {"increment": increment, "id": userId, "guild_id": guildId})
    conn.commit()

def sortByMessages(limit, guildId):
    c.execute("SELECT messages, name FROM users WHERE guild_id = :guild_id ORDER BY messages DESC LIMIT 10", {"guild_id": guildId})
    return c.fetchall()


