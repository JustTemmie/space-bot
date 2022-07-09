from apscheduler.schedulers.asyncio import AsyncIOScheduler

import database as db

import time

db.build()

scheduler = AsyncIOScheduler()
scheduler.start()
db.autosave(scheduler)

db.commit()

db.execute("INSERT INTO playerData (UserID) VALUES (?)", 368423564229083137)