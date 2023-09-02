import asyncio
import base64

from .util import SatiDict
from .socket import SatiSocket

class UnableToSolveTask(Exception):
    task: SatiDict
    def __init__(self, task: SatiDict):
        super().__init__(f"sati: unable to solve {task.type} task #{task.id}")
        self.task = task

class Sati:
    '''
    usage example:
    >>> from sati import Sati
    >>>
    >>> sati = Sati(token)
    >>> task = await sati.solve('Turnstile',
    >>>     siteKey='0x4AAAAAAAHMEd1rGJs9qy-0',
    >>>     pageUrl='https://polygon.sati.ac/Turnstile')
    >>>
    >>> print(task.result.token)
    '''

    _socket: SatiSocket
    _project_id: int
    _awaited_tasks: dict = {}

    def __init__(
        self,
        token: str,
        url: str = 'wss://api.sati.ac/ws',
        reconnection_interval: float = 1,
        project_id: int = 0,
        debug = False
    ):
        self._socket = SatiSocket(token, reconnection_interval, url, debug)
        self._project_id = project_id
        self._socket.on('taskUpdate', self._process_task)

    async def solve(self, task_type: str, **data):
        # special case for images
        if task_type == 'ImageToText' and 'image' in data and \
            isinstance(data['image'], (bytearray, bytes)):
            data['image'] = base64.b64encode(data['image']).decode('ascii')

        task = await self._socket.call('createTask', {
            'type': task_type,
            'data': data,
            'projectId': self._project_id
        })
        fut = asyncio.Future()
        self._awaited_tasks[task.id] = fut
        return await fut

    def _process_task(self, task: SatiDict):
        if task.id not in self._awaited_tasks or task.state not in ('success', 'error'):
            return
        fut = self._awaited_tasks[task.id]
        if task.state == 'success':
            fut.set_result(task)
        else:
            fut.set_exception(UnableToSolveTask(task))

    def destroy(self):
        self._socket.close()

    async def get_balance(self) -> float:
        return (await self._socket.call('getBalance')).balance
