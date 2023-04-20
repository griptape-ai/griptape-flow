from attr import define, field, Factory
from transformers import PreTrainedModel, pipeline, AutoTokenizer
from griptape.flow.artifacts import TextOutput
from griptape.flow.drivers import PromptDriver
from griptape.flow.tokenizers import HuggingFaceTokenizer


@define
class HuggingFacePipelinePromptDriver(PromptDriver):
    SUPPORTED_TASKS = ["text2text-generation", "text-generation"]

    model: str = field(kw_only=True)
    tokenizer: HuggingFaceTokenizer = field(
        default=Factory(
            lambda self: HuggingFaceTokenizer(
                tokenizer=AutoTokenizer.from_pretrained(self.model)
            ), takes_self=True
        ),
        kw_only=True
    )

    def try_run(self, value: any) -> TextOutput:
        generator = pipeline(
            tokenizer=self.tokenizer.tokenizer,
            model=self.model,
            max_new_tokens=self.tokenizer.tokens_left(value)
        )

        if generator.task in self.SUPPORTED_TASKS:
            response = generator(
                value,
                num_return_sequences=1,
            )

            if len(response) == 1:
                output_text = response[0]["generated_text"]

                if generator.task == "text-generation":
                    # Text generation return includes the starter text (not text2text-generation though).
                    output_text = output_text[len(value):]

                return TextOutput(
                    value=output_text
                )
            else:
                raise Exception("Completion with more than one choice is not supported yet.")
        else:
            raise Exception(f"Only models with the following tasks are supported: {self.SUPPORTED_TASKS}")
