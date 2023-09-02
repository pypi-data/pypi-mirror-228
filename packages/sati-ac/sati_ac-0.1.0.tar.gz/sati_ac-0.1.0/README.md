# sati-ac - python client for sati.ac
[![NPM version](https://badge.fury.io/py/sati-ac.svg)](https://pypi.org/project/sati-ac)

## usage example
```py
import asyncio
from sati import Sati

async def main():
	sati = Sati(token)
	print(await sati.get_balance())
	task = await sati.solve('Turnstile',
		siteKey = '0x4AAAAAAAHMEd1rGJs9qy-0',
		pageUrl = 'https://polygon.sati.ac/Turnstile'
	)
	print(task.result.token)

asyncio.run(main)
```