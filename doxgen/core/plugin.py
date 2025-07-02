import enum
import uuid
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field

class FType(enum.StrEnum):
    """Field type."""
    BOOL = 'b'
    CHAR = 'c'
    DATE = 'd'
    INT = 'i'
    DEC = '#'
    CHOICE = 's'
    INN = 'inn'
    OGRN = 'ogrn'

class PluginField(BaseModel):
    ftype: FType
    attrs: Dict[str, Any]  # django fields specific

class Plugin(BaseModel):
    """Plugin representation"""
    uuid: uuid.UUID  # K_T_UUID
    name: str  # K_T_NAME
    engine: str  # K_T_T.K_T_T_ENGINE
    comments: Optional[str] = None
    legend: Optional[str] = None
    fields: Dict[str, PluginField]  # K_T_FIELD; ordered from py3.7
    sample: Optional[List[str, Any]] = None
