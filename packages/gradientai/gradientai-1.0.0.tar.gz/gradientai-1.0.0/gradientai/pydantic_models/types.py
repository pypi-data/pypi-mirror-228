from pydantic import BaseModel


class CompleteResponse(BaseModel):
    generated_output: str


class FineTuneResponse(BaseModel):
    number_of_trainable_tokens: int
    sum_loss: float
