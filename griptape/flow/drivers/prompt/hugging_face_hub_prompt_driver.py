from attr import define, field, Factory
from huggingface_hub import InferenceApi
from griptape.flow.artifacts import TextOutput
from griptape.flow.drivers import PromptDriver
from griptape.flow.tokenizers import HuggingFaceTokenizer


@define
class HuggingFaceHubPromptDriver(PromptDriver):
    DEFAULT_TASK = "text-generation"
    SUPPORTED_TASKS = ["text2text-generation", "text-generation"]
    DEFAULT_PARAMS = {
        "return_full_text": False,
        "max_new_tokens": 250
    }

    tokenizer: HuggingFaceTokenizer = field(kw_only=True)
    repo_id: str = field(kw_only=True)
    api_token: str = field(kw_only=True)
    use_gpu: bool = field(default=False, kw_only=True)
    params: dict = field(factory=dict, kw_only=True)
    model: str = field(default=Factory(lambda self: self.repo_id, takes_self=True), kw_only=True)
    client: InferenceApi = field(
        default=Factory(
            lambda self: InferenceApi(repo_id=self.repo_id, token=self.api_token, gpu=self.use_gpu), takes_self=True
        ),
        kw_only=True
    )

    def try_run(self, value: any) -> TextOutput:
        if self.client.task in self.SUPPORTED_TASKS:
            response = self.client(
                inputs=value,
                params=self.DEFAULT_PARAMS | self.params
            )

            if len(response) == 1:
                return TextOutput(
                    value=response[0]["generated_text"]
                )
            else:
                raise Exception("Completion with more than one choice is not supported yet.")
        else:
            raise Exception(f"Only models with the following tasks are supported: {self.SUPPORTED_TASKS}")
