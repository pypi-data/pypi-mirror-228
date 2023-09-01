from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

import deprecation
import pandas as pd

from predibase.pql.api import Session
from predibase.resource.connection import Connection
from predibase.resource.dataset import Dataset
from predibase.resource.llm.interface import GeneratedResponse, HuggingFaceLLM, LLMDeployment, LLMDeploymentJob
from predibase.version import __version__


class LlmMixin:
    session: Session

    def LLM(self, uri: str) -> Union[HuggingFaceLLM, LLMDeployment]:
        if uri.startswith("pb://deployments/"):
            return LLMDeployment(self.session, uri[len("pb://deployments/") :])

        if uri.startswith("hf://"):
            return HuggingFaceLLM(self.session, uri[len("hf://") :])

        raise ValueError(
            "must provide either a Hugging Face URI (hf://<...>) "
            "or a Predibase deployments URI (pb://deployments/<name>).",
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

    @deprecation.deprecated(
        deprecated_in="2023.5.8",
        current_version=__version__,
        details="Use the LLMDeployment().prompt method instead",
    )
    def prompt(
        self,
        templates: Union[str, List[str]],
        deployment_names: Union[str, List[str]],
        index: Optional[Union[str, Dataset]] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        limit: Optional[int] = 10,
        options: Optional[Dict[str, float]] = None,
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        if isinstance(deployment_names, list) and len(deployment_names) == 1:
            deployment_names = deployment_names[0]
        if isinstance(templates, list) and len(templates) == 1:
            templates = templates[0]

        if not (index or dataset) and isinstance(deployment_names, str) and isinstance(templates, str):
            # talk directly to the LLM, bypassing Temporal and the engines.
            return self.generate(input_text=templates, deployment_name=deployment_names, options=options)

        # Set the connection if we have a dataset or index
        conn_id = None
        if isinstance(dataset, Dataset):
            conn_id = dataset.connection_id
        elif isinstance(index, Dataset):
            conn_id = index.connection_id
        resp = self.session.post_json(
            "/prompt",
            json={
                "connectionID": conn_id,
                "deploymentNames": [deployment_names] if isinstance(deployment_names, str) else deployment_names,
                "templates": [templates] if isinstance(templates, str) else templates,
                "options": options,
                "limit": limit,
                "indexName": index.name if isinstance(index, Dataset) else index,
                "datasetName": dataset.name if isinstance(dataset, Dataset) else dataset,
            },
            timeout=300,  # increase timeout to 5 minutes for this request
        )

        responses = [GeneratedResponse(**r) for r in resp["responses"]]
        return GeneratedResponse.to_pandas(responses)

    @deprecation.deprecated(
        deprecated_in="2023.5.8",
        current_version=__version__,
        details="Use the HuggingFaceLLM().deploy method instead",
    )
    def deploy_llm(
        self,
        deployment_name: str,
        model_name: str,
        engine_template: Optional[str] = None,
        scale_down_period=None,
    ) -> LLMDeploymentJob:
        return HuggingFaceLLM(self.session, model_name).deploy(
            deployment_name,
            engine_template=engine_template,
            scale_down_period=scale_down_period,
        )

    @deprecation.deprecated(
        deprecated_in="2023.5.8",
        current_version=__version__,
        details="Use the LLMDeployment().delete method instead",
    )
    def delete_llm(self, deployment_name: str):
        self.session.delete_json(f"/llms/{deployment_name}")

    def list_all_llms(self):
        return self.session.get_json("/llms?activeOnly=false")

    def list_deployed_llms(self):
        return self.session.get_json("/llms")

    @abstractmethod
    def get_dataset(self) -> Dataset:
        pass

    @abstractmethod
    def list_connections(self) -> List[Connection]:
        pass
