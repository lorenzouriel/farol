"""CPF-masking interface, established ahead of TSE prestação de contas / Portal
da Transparência donor sources (deferred to a later build) so those sources
plug in later without an architecture change.

Production deployments MUST set a real secret via CPF_MASK_SALT — the default
below is dev-only and MUST NOT be used outside local development.
"""
from __future__ import annotations

import hashlib
import os

DEFAULT_CPF_MASK_SALT = "farol-dev-salt"


def mask_cpf(cpf: str) -> str:
    salt = os.environ.get("CPF_MASK_SALT", DEFAULT_CPF_MASK_SALT)
    digest = hashlib.sha256(f"{salt}{cpf}".encode("utf-8"))
    return digest.hexdigest()


def mask_donor_fields(record: dict, fields: list[str]) -> dict:
    masked = dict(record)
    for field in fields:
        value = masked.get(field)
        if field not in masked or value is None:
            continue
        masked[field] = mask_cpf(value)
    return masked
