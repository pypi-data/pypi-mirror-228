from abc import ABC
from types import TracebackType
from typing import Any, List, Literal, Optional, overload
from typing_extensions import Self

from gradientai.pydantic_models.types import CompleteResponse, FineTuneResponse

from gradientai.openapi.client.api.models_api import ModelsApi
from gradientai.openapi.client.api_client import ApiClient
from gradientai.openapi.client.configuration import Configuration
from gradientai.openapi.client.models.complete_model_body_params import (
    CompleteModelBodyParams,
)
from gradientai.openapi.client.models.create_model_request_body import (
    CreateModelRequestBody,
)
from gradientai.openapi.client.models.create_model_request_body_initial_hyperparameters import (
    CreateModelRequestBodyInitialHyperparameters,
)
from gradientai.openapi.client.models.create_model_request_body_initial_hyperparameters_lora_hyperparameters import (
    CreateModelRequestBodyInitialHyperparametersLoraHyperparameters,
)
from gradientai.openapi.client.models.create_model_request_body_initial_hyperparameters_training_arguments import (
    CreateModelRequestBodyInitialHyperparametersTrainingArguments,
)
from gradientai.openapi.client.models.create_model_request_body_model import (
    CreateModelRequestBodyModel,
)
from gradientai.openapi.client.models.fine_tune_model_request_body import (
    FineTuneModelRequestBody,
)
from gradientai.openapi.client.models.model_adapter import (
    ModelAdapter as ApiModelAdapter,
)
from typing_extensions import assert_never

from gradientai.helpers.env_manager import ENV_MANAGER


class Model(ABC):
    _api_instance: ModelsApi
    _id: str
    _workspace_id: str

    def __init__(
        self, *, api_instance: ModelsApi, id: str, workspace_id: str
    ) -> None:
        self._api_instance = api_instance
        self._id = id
        self._workspace_id = workspace_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    def complete(
        self,
        *,
        query: str,
        max_generated_token_count: Optional[int] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
    ) -> CompleteResponse:
        response = self._api_instance.complete_model(
            id=self._id,
            x_gradient_workspace_id=self._workspace_id,
            complete_model_body_params=CompleteModelBodyParams(
                query=query,
                max_generated_token_count=max_generated_token_count,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
            ),
        )
        return CompleteResponse(generated_output=response.generated_output)


class ModelAdapter(Model):
    _base_model_id: str
    _name: str

    def __init__(
        self,
        *,
        api_instance: ModelsApi,
        id: str,
        base_model_id: str,
        name: str,
        workspace_id: str,
    ) -> None:
        super().__init__(
            api_instance=api_instance, id=id, workspace_id=workspace_id
        )
        self._base_model_id = base_model_id
        self._name = name

    @property
    def base_model_id(self) -> str:
        return self._base_model_id

    @property
    def name(self) -> str:
        return self._name

    def delete(self) -> None:
        self._api_instance.delete_model(
            id=self._id, x_gradient_workspace_id=self._workspace_id
        )

    def fine_tune(
        self,
        *,
        samples: list[dict[Literal["inputs"], str]],
    ) -> FineTuneResponse:
        response = self._api_instance.fine_tune_model(
            id=self._id,
            x_gradient_workspace_id=self._workspace_id,
            fine_tune_model_request_body=FineTuneModelRequestBody(
                samples=samples
            ),
        )
        return FineTuneResponse(
            number_of_trainable_tokens=response.number_of_trainable_tokens,
            sum_loss=response.sum_loss,
        )


class BaseModel(Model):
    _slug: str

    def __init__(
        self, *, api_instance: ModelsApi, id: str, slug: str, workspace_id: str
    ) -> None:
        super().__init__(
            api_instance=api_instance, id=id, workspace_id=workspace_id
        )
        self._slug = slug

    @property
    def slug(self) -> str:
        return self._slug

    def create_model_adapter(
        self,
        *,
        name: str,
        rank: Optional[int] = None,
        learning_rate: Optional[float] = None,
    ) -> ModelAdapter:
        response = self._api_instance.create_model(
            create_model_request_body=CreateModelRequestBody(
                initial_hyperparameters=CreateModelRequestBodyInitialHyperparameters(
                    lora_hyperparameters=CreateModelRequestBodyInitialHyperparametersLoraHyperparameters(
                        rank=rank
                    ),
                    training_arguments=CreateModelRequestBodyInitialHyperparametersTrainingArguments(
                        learning_rate=learning_rate
                    ),
                ),
                model=CreateModelRequestBodyModel(
                    name=name, base_model_id=self._id
                ),
            ),
            x_gradient_workspace_id=self._workspace_id,
        )
        return ModelAdapter(
            api_instance=self._api_instance,
            base_model_id=self._id,
            id=response.id,
            name=name,
            workspace_id=self._workspace_id,
        )


class Gradient:
    _api_client: ApiClient
    _api_instance: ModelsApi
    _workspace_id: str

    def __init__(
        self,
        *,
        access_token: str = ENV_MANAGER.access_token,
        host: Optional[str] = ENV_MANAGER.public_api_url,
        workspace_id: str = ENV_MANAGER.workspace_id,
    ) -> None:
        self._api_client = ApiClient(
            Configuration(
                access_token=access_token,
                host=host,
            )
        )
        self._api_instance = ModelsApi(self._api_client)
        self._workspace_id = workspace_id

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        __exc_type: Optional[type[BaseException]],
        __exc_val: Optional[BaseException],
        __exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    def close(self) -> None:
        self._api_client.close()

    def get_base_model(self, *, base_model_slug: str) -> BaseModel:
        models: List[BaseModel] = self.list_models(only_base=True)
        return next(
            filter(lambda model: model._slug == base_model_slug, models)
        )

    def get_model_adapter(self, *, model_adapter_id: str) -> ModelAdapter:
        response = self._api_instance.get_model(
            id=model_adapter_id, x_gradient_workspace_id=self._workspace_id
        )
        return ModelAdapter(
            api_instance=self._api_instance,
            base_model_id=response.base_model_id,
            id=response.id,
            name=response.name,
            workspace_id=self._workspace_id,
        )

    @overload
    def list_models(self, *, only_base: Literal[True]) -> List[BaseModel]:
        ...

    @overload
    def list_models(self, *, only_base: Literal[False]) -> List[Model]:
        ...

    def list_models(self, *, only_base: bool) -> List[Model]:  # type: ignore
        response = self._api_instance.list_models(
            x_gradient_workspace_id=self._workspace_id, only_base=only_base
        )

        def create_model_instance(
            api_model: Any,
        ) -> Model:
            match api_model.type:
                case "baseModel":
                    return BaseModel(
                        api_instance=self._api_instance,
                        id=api_model.id,
                        slug=api_model.slug,
                        workspace_id=self._workspace_id,
                    )
                case "modelAdapter":
                    response: ApiModelAdapter = api_model
                    return ModelAdapter(
                        api_instance=self._api_instance,
                        base_model_id=response.base_model_id,
                        id=response.id,
                        name=response.name,
                        workspace_id=self._workspace_id,
                    )
                case _:
                    assert_never(api_model.type)

        models = [
            create_model_instance(model.actual_instance)
            for model in response.models
        ]
        return models
