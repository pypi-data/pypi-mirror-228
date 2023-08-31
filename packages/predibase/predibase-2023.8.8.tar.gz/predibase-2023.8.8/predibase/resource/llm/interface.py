import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TYPE_CHECKING, Union

import yaml
from dataclasses_json import config, dataclass_json, LetterCase

from predibase.resource.connection import get_dataset
from predibase.resource.dataset import Dataset
from predibase.resource.engine import Engine
from predibase.resource.llm.response import GeneratedResponse
from predibase.resource.model import create_model_repo, ModelFuture, ModelRepo
from predibase.util import load_yaml

if TYPE_CHECKING:
    from predibase.pql.api import Session


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_DIR = os.path.join(_PATH_HERE, "templates")


class HuggingFaceLLM:
    def __init__(self, session: "Session", model_name: str):
        self.session = session
        self.model_name = model_name

    def deploy(
        self,
        deployment_name: str,
        engine_template: Optional[str] = None,
        scale_down_period: Optional[int] = None,
    ) -> "LLMDeploymentJob":
        valid_llms = self.session.get_json("/supported_llms")
        valid_llms_by_names = {x["modelName"]: x for x in valid_llms}
        if self.model_name not in valid_llms_by_names:
            raise ValueError(
                f"Model name {self.model_name} is not supported. Valid models are: {valid_llms_by_names.keys()}",
            )

        model_params = {
            **valid_llms_by_names[self.model_name],
            "name": deployment_name,
            "modelName": self.model_name,
            "engineTemplate": engine_template,
            "scaleDownPeriod": scale_down_period,
        }
        print("Deploying the model with the following params:")
        print(model_params)

        self.session.post_json(
            "/llms",
            json=model_params,
        )

        return LLMDeploymentJob(deployment_name, self.session)

    def finetune(
        self,
        template: Optional[str] = None,
        target: Optional[str] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        engine: Optional[Union[str, Engine]] = None,
        config: Optional[Union[str, Dict]] = None,
        repo: Optional[str] = None,
    ) -> ModelFuture:
        if config is None:
            with open(os.path.join(_TEMPLATE_DIR, "defaults.yaml")) as f:
                config_str = f.read()
            config_str = config_str.format(base_model=self.model_name, template=template, target=target)
            config = yaml.safe_load(config_str)
        else:
            config = load_yaml(config)

        if repo is None:
            dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
            if "/" in dataset_name:
                _, dataset_name = dataset_name.split("/")

            model_name = self.model_name
            if "/" in model_name:
                _, model_name = model_name.split("/")

            repo = f"{model_name}-{dataset_name}"

        if "/" in repo:
            repo = repo.replace("/", "-")

        repo: ModelRepo = get_or_create_repo(self.session, repo)
        if dataset is None:
            # Assume the dataset is the same as the repo head
            md = repo.head().to_draft()
            md.config = config
        else:
            if isinstance(dataset, str):
                conn_name = None
                if "/" in dataset:
                    conn_name, dataset = dataset.split("/")
                dataset = get_dataset(self.session, dataset, connection_name=conn_name)
            md = repo.create_draft(config=config, dataset=dataset)

        return md.train_async(engine=engine)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class _LLMDeployment:
    id: int = field(metadata=config(field_name="id"))
    tenant_id: int = field(metadata=config(field_name="tenantID"))
    uuid: str = field(metadata=config(field_name="uuid"))
    name: str = field(metadata=config(field_name="name"))
    description: Optional[str] = field(metadata=config(field_name="description"))
    model_name: str = field(metadata=config(field_name="modelName"))
    num_shards: Optional[int] = field(metadata=config(field_name="numShards"))
    quantize: bool = field(metadata=config(field_name="quantize"))
    deployment_status: str = field(metadata=config(field_name="deploymentStatus"))

    prompt_template: str = field(metadata=config(field_name="promptTemplate"))
    min_replicas: int = field(metadata=config(field_name="minReplicas"))
    max_replicas: int = field(metadata=config(field_name="maxReplicas"))
    created: str = field(metadata=config(field_name="created"))
    updated: str = field(metadata=config(field_name="updated"))
    created_by_user_id: Optional[int] = field(metadata=config(field_name="createdByUserID"))
    scale_down_period: int = field(metadata=config(field_name="scaleDownPeriod"))
    error_message: str = field(metadata=config(field_name="errorMessage"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentReadyResponse:
    name: str
    ready: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentScaledResponse:
    name: str
    scaled: bool


class LLMDeployment:
    def __init__(self, session: "Session", name: str, deployment_metadata: Optional[_LLMDeployment] = None):
        self.session = session
        self.name = name
        self.data = (
            _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
            if deployment_metadata is None
            else deployment_metadata
        )

    def generate(
        self,
        input_text: str,
        deployment_name: str,
        options: Optional[Dict[str, float]] = None,
    ):
        if not isinstance(deployment_name, str):
            raise ValueError("deployment_name must be a string.")

        # following the HuggingFace TGI schema.
        return self.session.post_json(
            f"/llms/{deployment_name}/generate",
            {
                "inputs": input_text,
                "parameters": options,
            },
        )

    def prompt(
        self,
        templates: Union[str, List[str]],
        index: Optional[Union[str, Dataset]] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        limit: Optional[int] = 10,
        options: Optional[Dict[str, float]] = None,
    ) -> List[GeneratedResponse]:
        if isinstance(templates, list) and len(templates) == 1:
            templates = templates[0]
        if not (index or dataset) and isinstance(templates, str):
            # talk directly to the LLM, bypassing Temporal and the engines.
            return self.generate(input_text=templates, deployment_name=self.name, options=options)

        deployment_status = self.get_status()
        if deployment_status != "active":
            raise Exception(f"Target LLM deployment `{self.name}` is not active yet!")

        deployment_ready = self.is_ready()
        if not deployment_ready:
            print(f"WARNING: Target LLM deployment `{self.name}` is not fully scaled yet. Responses may be delayed...")

        conn_id = None
        if isinstance(dataset, Dataset):
            conn_id = dataset.connection_id
        elif isinstance(index, Dataset):
            conn_id = index.connection_id
        resp = self.session.post_json(
            "/prompt",
            json={
                "connectionID": conn_id,
                "deploymentNames": [self.name],
                "templates": [templates] if isinstance(templates, str) else templates,
                "options": options,
                "limit": limit,
                "indexName": index.name if isinstance(index, Dataset) else index,
                "datasetName": dataset.name if isinstance(dataset, Dataset) else dataset,
            },
        )

        responses = resp["responses"]
        return [GeneratedResponse(**r) for r in responses]

    def delete(self):
        return self.session.delete_json(f"/llms/{self.name}")

    def is_ready(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/ready")
        return LLMDeploymentReadyResponse.from_dict(resp).ready

    def wait_for_ready(self, timeout_seconds: int = 600, poll_interval_seconds: int = 5) -> bool:
        start = time.time()
        while int(time.time() - start) < timeout_seconds:
            if self.is_ready():
                return True
            time.sleep(poll_interval_seconds)
        return False

    def is_scaled(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/scaled")
        return LLMDeploymentScaledResponse.from_dict(resp).scaled

    def get_status(self) -> str:
        resp = _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
        return resp.deployment_status


class LLMDeploymentJob:
    def __init__(self, deployment_name: str, session: "Session"):
        self._deployment_name = deployment_name
        self._uri = f"pb://jobs/deploy::{deployment_name}"
        self._session = session

    def get(self) -> LLMDeployment:
        resp = self._session.get_llm_deployment_until_with_logging(
            f"/llms/{self._deployment_name}",
            lambda resp: resp["deploymentStatus"] == "active",
            lambda resp: f"Failed to create deployment {self._deployment_name} with status {resp['deploymentStatus']}"
            if resp["deploymentStatus"] in ("failed", "canceled")
            else None,
        )

        return LLMDeployment(self._session, self._deployment_name, resp)

    def cancel(self):
        return self._session.post_json(f"/llms/{self._deployment_name}/cancel", {})


def get_or_create_repo(session: "Session", repo_name: str) -> ModelRepo:
    return create_model_repo(session, name=repo_name, exists_ok=True)
