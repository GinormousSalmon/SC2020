from peewee import *

db = SqliteDatabase('users.db')
db.connect()


class Person(Model):
    username = CharField()
    is_gay = BooleanField()

    class Meta:
        database = db


Person.create_table()
a = Person(username="cocksuker", is_gay=True)
a.save()

b = Person(username="sanya", is_gay=True)
b.save()

for person in Person.select().where(Person.username == "gay"):
    print(person.username, person.is_gay, person.get_id())
print(len(Person.select().where(Person.username == "sanya")) == 0)
# print(Person.get(Person.username == "gay"))
# print(Person.select().where(Person.username == "gay"))
