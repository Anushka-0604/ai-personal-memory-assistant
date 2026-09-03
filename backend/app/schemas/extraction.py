from pydantic import BaseModel, Field


class MemoryExtractionBase(BaseModel):
    """
    Base schema representing structured information
    extracted from a user memory.
    """

    people: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    dates: list[str] = Field(default_factory=list)

    events: list[str] = Field(default_factory=list)
    tasks: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)

    summary: str = ""


class MemoryExtraction(MemoryExtractionBase):
    """
    Final validated extraction object.
    """

    pass