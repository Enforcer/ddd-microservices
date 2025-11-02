import json
from typing import Any, Literal

import httpx

from container_or_host import host_for_dependency

type JsonSchema = dict[str, Any]


class IncompatibleVersion(Exception):
    pass


class ApicurioRegistryClient:
    _DEFAULT_BASE_URL = f"http://{host_for_dependency('apicurio-registry')}:8080/apis/registry/v3/"

    def __init__(
        self, base_url: str = _DEFAULT_BASE_URL
    ) -> None:
        self._client = httpx.Client(base_url=base_url)

    def register_new_artifact(self, artifact_id: str, schema: JsonSchema) -> None:
        # artifactType is determined automatically
        # It should handle asyncapi, openapi and json[schema] fine.
        response = self._client.post(
            "groups/default/artifacts",
            json={
                "artifactId": artifact_id,
                "firstVersion": {
                    "content": {
                        "content": json.dumps(schema),
                        "contentType": "application/json",
                    }
                },
            },
        )
        response.raise_for_status()

    def unregister_artifact(self, artifact_id: str) -> None:
        response = self._client.delete(f"groups/default/artifacts/{artifact_id}")
        response.raise_for_status()

    def set_rule(
        self,
        artifact_id: str,
        rule_type: Literal["COMPATIBILITY"],
        config: Literal["FORWARD", "BACKWARD"],
    ) -> None:
        response = self._client.post(
            f"groups/default/artifacts/{artifact_id}/rules",
            json={"config": config, "ruleType": rule_type},
        )
        response.raise_for_status()

    def check_version(self, artifact_id: str, schema: JsonSchema) -> None:
        response = self._client.post(
            f"groups/default/artifacts/{artifact_id}/versions",
            params={"dryRun": "true"},
            json={
                "content": {
                    "content": json.dumps(schema),
                    "contentType": "application/json",
                }
            },
        )
        if response.status_code == 409:
            raise IncompatibleVersion
        response.raise_for_status()
