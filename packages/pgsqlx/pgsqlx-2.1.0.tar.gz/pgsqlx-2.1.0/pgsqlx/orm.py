from .constant import KEY_SEQ
from .db import insert, save_key_seq
from . import get_snowflake_id, PostgresEngine
from .log_support import orm_insert_log, logger

# Don't remove. Import for not repetitive implementation
from sqlbatis.orm import DelFlag, KeyStrategy, Model as BaseModel


class Model(BaseModel):
    """
    Create a class extends Model:

    class Person(Model):
        __key__ = 'id'
        __table__ = 'person'
        __update_by__ = 'update_by'
        __update_time__ = 'update_time'
        __del_flag__ = 'del_flag'
        __key_seq__ = 'person_id_seq'

        def __init__(self, id: int = None, name: str = None, age: int = None, update_by: int = None, update_time: datetime = None, del_flag: int = None):
            self.id = id

            self.update_by = update_by
            self.update_time = update_time
            self.del_flag = del_flag
            self.name = name
            self.age = age

    then you can use like follow:
        init_db(person='xxx', password='xxx', database='xxx', host='xxx', ...)  # or dbx.init_db(...) init db first,
        person = Person(name='张三', age=55)
        effect_rowcount = person.persist()
        id = person.inst_save()
    """

    @classmethod
    def save(cls, **kwargs):
        """
        id = Person.save(name='张三', age=20)
        :return: Primary key
        """
        orm_insert_log('save', cls.__name__, **kwargs)
        key, table = cls._get_key_and_table()
        if key in kwargs:
            insert(table, **kwargs)
            return kwargs[key]

        key_strategy = cls._get_key_strategy()
        if key_strategy == KeyStrategy.SNOWFLAKE:
            kwargs[key] = get_snowflake_id()
            insert(table, **kwargs)
            return kwargs[key]
        else:
            key_seq = cls._get_key_seq()
            return save_key_seq(key_seq, table, **kwargs)

    @classmethod
    def _get_key_seq(cls):
        if hasattr(cls, KEY_SEQ):
            return cls.__key_seq__
        logger.warning("%s not set attribute '%s'" % (cls.__name__, KEY_SEQ))
        key, table = cls._get_key_and_table()
        return PostgresEngine.build_key_seq(table=table, key=key)
