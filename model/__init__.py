from core.store import store
from datetime import datetime


class BaseModel(object):
    table = NotImplemented

    fields = []
    key_fields = ['id']

    def __init__(self, *args, **kwargs):
        idx = 0
        for f in self.fields:
            if f in kwargs:
                v = kwargs[f]
            elif idx >= len(args):
                continue
            else:
                v = args[idx]
                idx += 1
            setattr(self, f, v)

    @classmethod
    def _joined_fields(cls):
        if not hasattr(cls, '__joined_fields'):
            cls.__join_fields = ','.join(
                ['`' + field + '`' for field in cls.fields])
        return cls.__join_fields

    @classmethod
    def get(cls, id):
        rs = store.execute(
            'select {0} from {1} '
            'where id=%s'.format(cls._joined_fields(), cls.table), id)
        return cls(**rs[0]) if rs else ''

    @classmethod
    def add(cls, *args, **kwargs):
        input_format = []
        input_fields =[]
        values = []
        idx = 0
        for f in cls.fields:
            if f in kwargs:
                value = kwargs[f]
            elif f == 'id':
                continue
            elif idx < len(args):
                value = args[idx]
                idx += 1
            else:
                continue
            input_fields.append(f)
            if f == 'update_time' or f == 'create_time':
                input_format.append('now()')
            else:
                input_format.append('%s')
                values.append(value)
        input_fields = ['`' + f + '`' for f in input_fields]
        sql = "insert into {0} ({1}) values ({2})".format(
            cls.table, ','.join(input_fields), ','.join(input_format)
        )
        _id = store.execute(sql, *values)
        if _id:
            entity = cls.get(_id)
            return entity

    @classmethod
    def update(cls, id, **kwargs):
        update_fields = []
        values = []
        for f in cls.fields:
            if f in kwargs:
                update_fields.append('`{}`=%s'.format(f))
                if f == 'update_time':
                    values.append(datetime.now())
                else:
                    values.append(kwargs[f])
        values.append(id)
        sql = 'update {0} set {1} where id=%s'.format(cls.table, ','.join(update_fields))
        rs = store.execute(sql, *values)
        return rs

    @classmethod
    def delete(cls, id):
        r = cls.get(id)
        if not r:
            return
        rs = store.execute('delete from {0} where id=%s'.format(cls.table), id)
        return rs

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id != other.id

    def __hash__(self):
        return hash((self.__class__, self.id))

    def __str__(self):
        instance_label = '{class_}:{id_} at {hex_}'.format(
            class_=self.__class__.__name__, id_=self.id, hex_=hex(id(self)))
        field_labels = ['%s:%s' % (name, get_attr_repr(self, name))
                        for name in self.key_fields if name != 'id']

        sum_len = sum(len(label) for label in [instance_label] + field_labels)
        if sum_len > 55:
            joined_label = '\n    '.join([''] + field_labels)
        else:
            joined_label = ' '.join([''] + field_labels)

        return '<{0}{1}>'.format(instance_label, joined_label)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __repr__(self):
        fields = ['%s=%s' % (name, get_attr_repr(self, name))
                  for name in self.key_fields]
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(fields))


def human_readable_repr(value):
    """The ``repr`` alternative implementation which show string literal as
    human-readable format just like the Python 3.
    """
    if isinstance(value, bytes):
        return "b'%s'" % value
    return repr(value)

def get_attr_repr(instance, name):
    value = getattr(instance, name, NotImplemented)
    return human_readable_repr(value)
