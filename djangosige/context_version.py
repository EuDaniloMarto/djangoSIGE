from typing import Dict
from django.http import HttpRequest


def sige_version(request: HttpRequest) -> Dict[str, str]:
    return {"versao": "v1.0.0"}
