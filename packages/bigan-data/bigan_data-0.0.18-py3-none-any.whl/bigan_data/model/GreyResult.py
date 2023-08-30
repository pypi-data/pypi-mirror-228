from typing import Optional

from sqlalchemy import Column
from sqlmodel import Field, Session, SQLModel, create_engine, select


class GreyRelationAnalyzerResMonthly(SQLModel, table=True):
    __tablename__ = "grey_relation_analyzer_res_monthly"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(description="代码, sh000001", index=True)
    current_month: str = Field(description="年月", index=True)
    result_month:  str = Field(description="res年月")
    result_month1: str = Field(description="res年月1")
    result_month2: str = Field(description="res年月2")
    result_month3: str = Field(description="res年月3")
    result_month4: str = Field(description="res年月4")
    result_month5: str = Field(description="res年月5")
