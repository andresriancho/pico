from hashlib import md5

from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
from CodernityDB.index import IndexConflict
from CodernityDB.database import PreconditionsException
from CodernityDB.storage import IU_Storage

#
# http://stackoverflow.com/a/34708989/1347554
#
def monkey_get(self, start, size, status='c'):
    if status == 'd':
        return None
    else:
        self._f.seek(start)
        return self.data_from(self._f.read(size))

IU_Storage.get = monkey_get
#
# http://stackoverflow.com/a/34708989/1347554
#

class WithTestNameIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(WithTestNameIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        test_name = data.get('test_name')
        if test_name is not None:
            return md5(test_name).digest(), data

        return None

    def make_key(self, key):
        return md5(key).digest()


def read_samples(db_filename, test_name):
    db = Database(db_filename)
    db.open()

    test_name_ind = WithTestNameIndex(db.path, 'test_name')

    try:
        db.edit_index(test_name_ind)
    except (IndexConflict, PreconditionsException):
        db.add_index(test_name_ind)

    for data in db.get_many('test_name', test_name, limit=-1):
        yield data


def read_timing_samples(db_filename, test_name, token, key):
    timing_data = []

    for data in read_samples(db_filename, test_name):
        if data['token_1'] == token or data['token_0'] == token:
            timing_data.append(data[key])

    return timing_data
