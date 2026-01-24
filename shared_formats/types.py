from typing import Optional, List
from pydantic import BaseModel, Field


class JobListing(BaseModel):
    id: str
    title: str
    company: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    description: str
    redirect_url: str
    created: str
    category: Optional[str] = None
    contract_time: Optional[str] = None  # e.g., full-time, part-time
    contract_type: Optional[str] = None  # e.g., permanent, contract


class SearchCriteria(BaseModel):
    keywords: str
    location: str
    distance: int = 10
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    results_per_page: int = 20
    page: int = 1
    target_count: Optional[int] = None
    sort_by: Optional[str] = None
    what_exclude: Optional[str] = None
    full_time: bool = False
    permanent: bool = False
    contract: bool = False
    part_time: bool = False
    days_old: Optional[int] = None
