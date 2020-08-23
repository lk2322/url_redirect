from peewee import *
import errors
import random
db = SqliteDatabase('URL.db')


class URL(Model):
    o_url = CharField()
    r_url = CharField(unique=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


def add_url(o_url, r_url, rerol=False) -> None:
    try:
        url = URL.create(o_url=o_url, r_url=r_url)
        url.save()
    except IntegrityError as e:
        if rerol:
            add_url(o_url, ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8)))
        else:
            raise errors.LinkAlreadyExistsError(r_url)
        print(e)
        print(f'This links already exists in the database:  {r_url}')


def get_url(r_url):
    try:
        url = URL.get(URL.r_url == r_url)
    except Exception as e:
        if e.__class__.__name__ == 'URLDoesNotExist':
            return 404
    return url.o_url
db.create_tables([URL])
