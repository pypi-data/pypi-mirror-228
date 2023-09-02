import json
import typing
from dataclasses import dataclass
import asyncio
import websockets.client as wsc
from .util import SatiDict

STATE_CONNECTED = 0
STATE_RECONNECTING = 1
STATE_UNRECOVERABLE = 2

class SatiUnrecoverableException(Exception):
    def __init__(self, message: str):
        super().__init__(f"sati: {message}")

class SatiException(Exception):
    ''' api error '''

    code: int

    def __init__(self, message: str, code: int = 0):
        super().__init__(f"sati: #{code}: {message}")
        self.code = code

@dataclass
class QueueEntry:
    fut: asyncio.Future
    method: str
    data: dict

class SatiSocket:
    ''' low-level api wrapper '''
    __token: str
    __state: int = STATE_RECONNECTING
    __socket: typing.Any
    __reconnection_interval: float
    __connector_ref: asyncio.Task
    __id_counter: int = 0
    __awaited_replies: dict = {}
    __error = None
    __queue = []
    __url: str
    __event_handlers = {}
    __debug: bool

    def __init__(
        self,
        token: str,
        reconnection_interval: float = 1,
        url = 'wss://api.sati.ac/ws',
        debug = False
    ):
        self.__token = token
        self.__reconnection_interval = reconnection_interval
        self.__url = url
        self.__connector_ref = asyncio.create_task(self.__connector())
        self.__debug = debug

    async def __connector(self):
        while self.__state != STATE_UNRECOVERABLE:
            try:
                try:
                    await self.__connect()
                except asyncio.CancelledError as ex:
                    raise SatiUnrecoverableException('socket closed') from ex
            except SatiUnrecoverableException as ex:
                self.__state = STATE_UNRECOVERABLE
                self.__error = ex
                break
            except Exception as ex:
                print(ex)
            await asyncio.sleep(self.__reconnection_interval)

    async def __connect(self):
        self.__socket = await wsc.connect(self.__url)
        self.__state = STATE_RECONNECTING

        reader = asyncio.create_task(self.__reader())
        auth_resp = await self.__send('auth', { 'token': self.__token })

        if not auth_resp.success:
            ex = SatiUnrecoverableException('invalid token')
            for entry in self.__queue:
                entry.fut.set_exception(ex)
            self.__queue = []
            raise ex

        self.__state = STATE_CONNECTED
        for entry in self.__queue:
            asyncio.create_task(self.__resend_call(entry))
        self.__queue = []

        await reader

    async def __resend_call(self, call: QueueEntry):
        try:
            result = await self.call(call.method, call.data)
            call.fut.set_result(result)
        except Exception as ex:
            call.fut.set_exception(ex)

    async def __send(self, msg_type: str, data: dict) -> dict:
        self.__id_counter += 1
        msg_id = self.__id_counter

        if self.__debug:
            print(f'sending message {msg_type} with id {msg_id}', data)

        if msg_type in ( 'auth', 'call' ):
            fut = self.__awaited_replies[msg_id] = asyncio.Future()
        await self.__socket.send(json.dumps({
            'id': self.__id_counter,
            'type': msg_type,
            'data': data
        }))

        if msg_type in ( 'auth', 'call' ):
            return await fut

    async def call(self, method: str, data: dict = {}) -> SatiDict:
        if self.__state == STATE_CONNECTED:
            resp = await self.__send('call', {
                'method': method,
                'data': data
            })
            if not resp.success:
                raise SatiException(resp.data.description, code=resp.data.code)
            return resp.data
        if self.__state == STATE_RECONNECTING:
            fut = asyncio.Future()
            self.__queue.append(QueueEntry(fut, method, data))
            return await fut
        if self.__state == STATE_UNRECOVERABLE:
            raise self.__error

    async def __reader(self):
        try:
            async for msg in self.__socket:
                msg = SatiDict(json.loads(msg))

                if self.__debug:
                    print('recieved message', msg)

                if msg.type in [ 'auth', 'call' ] and msg.to in self.__awaited_replies:
                    self.__awaited_replies[msg.to].set_result(msg.data)
                elif msg.type == 'event':
                    if msg.data.type not in self.__event_handlers:
                        continue
                    for handler in self.__event_handlers[msg.data.type]:
                        handler(msg.data.data)
        except Exception as ex:
            for key, reply in self.__awaited_replies.items():
                reply.set_exception(ex)
                del self.__awaited_replies[key]
            raise ex

    def close(self):
        self.__connector_ref.cancel()

    def on(self, event: str, handler: typing.Callable[[SatiDict], None]):
        if event not in self.__event_handlers:
            self.__event_handlers[event] = []

        self.__event_handlers[event].append(handler)
