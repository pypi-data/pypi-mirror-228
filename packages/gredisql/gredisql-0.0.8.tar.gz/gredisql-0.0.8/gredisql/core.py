# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 30 Aug 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""

import typing
import redis
import strawberry

REDIS_host = 'localhost'
REDIS_port = 6379
REDIS_db = 0
REDIS_decode_response = True

rr = redis.StrictRedis(host=REDIS_host,
                       port=REDIS_port,
                       db=REDIS_db,
                       decode_responses=REDIS_decode_response)


@strawberry.type
class CommonString:
    response: typing.Optional[str]


class CommonDict:
    response: dict


@strawberry.input
class KeyVal:
    key: str
    value: str


@strawberry.type
class Query:
    @strawberry.field
    def set(self,
            name: str,
            value: str,
            ex: typing.Optional[int] = None,
            px: typing.Optional[int] = None,
            nx: typing.Optional[bool] = False,
            xx: typing.Optional[bool] = False,
            keepttl: typing.Optional[bool] = False,
            get: typing.Optional[bool] = False,
            exat: typing.Optional[int] = None,
            pxat: typing.Optional[int] = None
            ) -> CommonString:
        print(name, value, get)
        resp = rr.set(
            name=name,
            value=value,
            ex=ex,
            px=px,
            nx=nx,
            xx=xx,
            keepttl=keepttl,
            get=get,
            exat=exat,
            pxat=pxat
        )
        print('resp:', resp)
        return CommonString(response=resp)

    @strawberry.field
    def get(self, name: str) -> CommonString:
        resp = rr.get(name=name)
        return CommonString(response=resp)

    @strawberry.field
    def getex(self,
              name: str,
              ex: typing.Optional[int] = None,
              px: typing.Optional[int] = None,
              exat: typing.Optional[int] = None,
              pxat: typing.Optional[int] = None,
              persist: bool = False
              ) -> CommonString:
        resp = rr.getex(name=name, ex=ex, px=px, exat=exat, pxat=pxat, persist=persist)
        return CommonString(response=resp)

    @strawberry.field
    def info(self) -> CommonString:
        info_dict = rr.info()
        print(info_dict)
        return CommonString(response=str(info_dict))

    @strawberry.field
    def mset(self, mappings: typing.List[KeyVal]) -> bool:
        mappings = {m.key: m.value for m in mappings}
        resp = rr.mset(mappings)
        return resp

    @strawberry.field
    def mget(self, keys: typing.List[str]) -> typing.List[str]:
        resp = rr.mget(keys=keys)
        return resp

    @strawberry.field
    def incrby(self, name: str, amount: int = 1) -> str:
        return rr.incrby(name=name, amount=amount)

    @strawberry.field
    def decrby(self, name: str, amount: int = 1) -> str:
        return rr.decrby(name=name, amount=amount)

    @strawberry.field
    def incrbyfloat(self, name: str, amount: float = 1.0) -> str:
        return rr.incrbyfloat(name=name, amount=amount)

    @strawberry.field
    def keys(self, pattern: str) -> typing.List[str]:
        return rr.keys(pattern=pattern)

    @strawberry.field
    def delete(self, names: typing.List[str]) -> str:
        return rr.delete(*names)

    @strawberry.field
    def exists(self, names: typing.List[str]) -> str:
        return rr.exists(*names)

    @strawberry.field
    def append(self, key: str, value: str) -> str:
        return rr.append(key=key, value=value)

    @strawberry.field
    def expire(
            self,
            name: str,
            time: int,
            nx: typing.Optional[bool] = False,
            xx: typing.Optional[bool] = False,
            gt: typing.Optional[bool] = False,
            lt: typing.Optional[bool] = False) -> str:
        return rr.expire(
            name=name,
            time=time,
            nx=nx,
            xx=xx,
            gt=gt,
            lt=lt
        )

    @strawberry.field
    def expireat(
            self,
            name: str,
            when: int,
            nx: typing.Optional[bool] = False,
            xx: typing.Optional[bool] = False,
            gt: typing.Optional[bool] = False,
            lt: typing.Optional[bool] = False) -> str:
        return rr.expireat(
            name=name,
            when=when,
            nx=nx,
            xx=xx,
            gt=gt,
            lt=lt
        )

    @strawberry.field
    def getdel(self, name: str) -> str:
        return rr.getdel(name=name)

    ## Redis Sets
    @strawberry.field
    def sadd(self, name: str, values: typing.List[str]) -> int:
        return rr.sadd(name, *values)

    @strawberry.field
    def scard(self, name: str) -> int:
        return rr.scard(name=name)

    @strawberry.field
    def sdiff(self, keys: typing.List[str],
              ) -> typing.List[str]:
        answers = rr.sdiff(keys)
        print('answers:', answers)
        return answers

    @strawberry.field
    def sdiffstore(self,
                   keys: typing.List[str],
                   dest: str) -> int:
        return rr.sdiffstore(dest=dest,
                             keys=keys)

    @strawberry.field
    def sinter(self,
               keys: typing.List[str]) -> typing.List[str]:
        return rr.sinter(keys)

    @strawberry.field
    def sinterstore(self,
                    keys: typing.List[str],
                    dest: str
                    ) -> int:
        return rr.sinterstore(dest=dest, keys=keys)

    @strawberry.field
    def sismember(self,
                  name: str,
                  value: str
                  ) -> int:
        return rr.sismember(name=name, value=value)

    @strawberry.field
    def smembers(self,
                 name: str
                 ) -> typing.List[str]:
        return rr.smembers(name=name)

    @strawberry.field
    def sismember(self,
                  name: str,
                  value: str
                  ) -> int:
        return rr.sismember(name=name, value=value)

    @strawberry.field
    def smove(self,
              src: str,
              dst: str,
              value: str
              ) -> int:
        return rr.smove(src=src, dst=dst, value=value)

    @strawberry.field
    def spop(self,
             name: str,
             count: typing.Optional[int]
             ) -> int:
        return rr.spop(name=name, count=count)


schema = strawberry.Schema(Query)

from flask import Flask
from strawberry.flask.views import GraphQLView


class Server:
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5055,
                 debug=True
                 ):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view("graphql_view", schema=schema),
        )

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port,
            debug=self.debug
        )
