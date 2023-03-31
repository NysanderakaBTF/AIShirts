import os
import replicate

from AIshirts.Exeptions import dailyLimitCheck


class Generator:
    def __init__(self):
        self.api_key = os.environ.get("REPLICATE_API_TOKEN")
        if self.api_key is None:
            raise EnvironmentError("REPLICATE_API_TOKEN environment variable not set")

    async def stable_diffusion_base(self, prompt, user):
        ans = None
        if dailyLimitCheck(user):
            ans = replicate.run(
                prompt.ai_model.access_url,
                input={
                    "prompt": prompt.prompt,
                    "image_dimensions": prompt.width + 'x' + prompt.height,
                    "negative_prompt": prompt.negative_prompt,
                    "num_outputs": prompt.num_outputs,
                    "num_interface_steps": prompt.num_steps,
                    "guidance_scale": prompt.guidance_scale,
                    "scheduler": prompt.scheduler,
                    "seed": prompt.seed
                }
            )
        return ans

    async def stable_diffusion_anime(self, prompt, user):
        ans = None
        if dailyLimitCheck(user):
            ans = replicate.run(
                prompt.ai_model.access_url,
                input={
                    "prompt": prompt.prompt,
                    "width": prompt.width,
                    "height": prompt.height,
                    "negative_prompt": prompt.negative_prompt,
                    "num_outputs": prompt.num_outputs,
                    "num_interface_steps": prompt.num_steps,
                    "guidance_scale": prompt.guidance_scale,
                    "scheduler": prompt.scheduler,
                    "seed": prompt.seed
                }
            )
        return ans

    async def generate(self, prompt, user):
        if prompt.ai_model.name == "stable_diffusion":
            return self.stable_diffusion_base(prompt, user)
        elif prompt.ai_model.name == "arcane":
            return self.stable_diffusion_anime(prompt, user)
        elif prompt.ai_model.name == "anime":
            return self.stable_diffusion_anime(prompt, user)
        else:
            raise ValueError("Unknown AI model")
