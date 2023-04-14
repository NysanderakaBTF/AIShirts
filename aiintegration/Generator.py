import os
from datetime import datetime

import replicate
from asgiref.sync import sync_to_async

from AIShirts.Exeptions import dailyLimitCheck
from cust_and_stuff.models import Customer


class Generator:
    def __init__(self):
        self.api_key = os.environ.get("REPLICATE_API_TOKEN")
        if self.api_key is None:
            raise EnvironmentError("REPLICATE_API_TOKEN environment variable not set")

    async def stable_diffusion_base(self, prompt, user):
        ans = None
        if dailyLimitCheck(user):
            ans = await sync_to_async(replicate.run)(
                prompt.ai_model.access_url,
                input={
                    "prompt": prompt.prompt,
                    "image_dimensions": str(prompt.width) + 'x' + str(prompt.height),
                    "negative_prompt": prompt.negative_prompt,
                    "num_outputs": prompt.num_outputs,
                    "num_interface_steps": prompt.num_steps,
                    "guidance_scale": prompt.guidance_scale,
                    "scheduler": prompt.scheduler.name,
                    "seed": prompt.seed
                }
            )
        return ans

    async def stable_diffusion_anime(self, prompt, user):
        ans = None
        if dailyLimitCheck(user):
            ans = await sync_to_async(replicate.run)(
                prompt.ai_model.access_url,
                input={
                    "prompt": prompt.prompt,
                    "width": prompt.width,
                    "height": prompt.height,
                    "negative_prompt": prompt.negative_prompt,
                    "num_outputs": prompt.num_outputs,
                    "num_interface_steps": prompt.num_steps,
                    "guidance_scale": prompt.guidance_scale,
                    "scheduler": prompt.scheduler.name,
                    "seed": prompt.seed
                }
            )
        return ans

    async def generate(self, prompt, user):
        cus = await Customer.objects.aget(email=user.email)
        cus.generation_count += 1
        cus.last_count = datetime.now()
        await sync_to_async(cus.save)()
        if prompt.ai_model.name == "stable_diffusion":
            return await self.stable_diffusion_base(prompt, cus)
        elif prompt.ai_model.name == "arcane":
            return await self.stable_diffusion_anime(prompt, cus)
        elif prompt.ai_model.name == "anime":
            return await self.stable_diffusion_anime(prompt, cus)
        else:
            raise ValueError("Unknown AI model")
