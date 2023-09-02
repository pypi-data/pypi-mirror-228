# Plum Econet api wrapper

This package aims to simplify using Plum Econet api available via local network.

Based on and tested with local router connected to HKS Lazar SmartFire pellet furnace.

# Basic usage

```python
import asyncio
from plum_econet import Smartfire

async def main():
    smartfire = Smartfire("<host>", "username", "password")
    await smartfire.update()
    print(f"Current temperature {smartfire.boiler.temperature}")
    print(f"Target temperature {smartfire.boiler.target_temperature}")
    await smartfire.boiler.set_target_temperature(76)
    await asyncio.sleep(5)
    await smartfire.update()
    print(f"Target temperature {smartfire.boiler.target_temperature}")

if __name__ == "__main__":
    asyncio.run(main())
```
