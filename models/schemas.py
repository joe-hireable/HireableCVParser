from typing import List, Optional, Dict, Annotated
from pydantic import BaseModel, Field, ConfigDict, constr, field_validator
from enum import Enum
from datetime import datetime

# Common Enums
class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERRORS = "errors"
    PARTIAL = "partial"

class SeverityEnum(str, Enum):
    ERROR = "error"
    WARNING = "warning"

class SkillProficiencyEnum(str, Enum):
    BEGINNER = "Beginner"
    AVERAGE = "Average"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class SkillTypeEnum(str, Enum):
    HARD = "hard"
    SOFT = "soft"

class LanguageLevelEnum(str, Enum):
    NATIVE = "Native"
    FLUENT = "Fluent"
    ADVANCED = "Advanced"
    INTERMEDIATE = "Intermediate"
    BASIC = "Basic"

# Common Models
class ErrorModel(BaseModel):
    code: str = Field(description="Error code identifier")
    message: str = Field(description="Human-readable error message")
    severity: SeverityEnum = Field(default=SeverityEnum.ERROR)

class FeedbackModel(BaseModel):
    strengths: Annotated[List[str], Field(
        description="Effective aspects",
        min_length=1,
        max_length=5
    )]
    areasToImprove: Annotated[List[str], Field(
        description="Improvement suggestions",
        min_length=1,
        max_length=5
    )]

class BaseResponseSchema(BaseModel):
    """Base class for all response schemas with common configuration"""
    model_config = ConfigDict(extra="ignore")
    
    status: StatusEnum = Field(description="Processing status")
    errors: Optional[List[ErrorModel]] = Field(default=None, description="List of errors encountered")

# Parsing Schema Models

# New Model for Roles within Parsing Experience
class ParsingRoleModel(BaseModel):
    title: str = Field(description="Job title for this specific role")
    start: Optional[str] = None
    end: Optional[str] = None
    current: bool = Field(description="Whether this specific role is current")

class LinkModel(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None

class LocationModel(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None

class SkillModel(BaseModel):
    name: str = Field(description="Name of the skill")
    proficiency: SkillProficiencyEnum = Field(description="Proficiency level")
    skillType: SkillTypeEnum = Field(description="Skill type (hard/soft)")

class LanguageModel(BaseModel):
    name: str = Field(description="Language name")
    level: Optional[LanguageLevelEnum] = None

class ExperienceModel(BaseModel):
    company: str = Field(description="Company or organization name")
    title: str = Field(description="Job title")
    start: Optional[str] = None
    end: Optional[str] = None
    current: bool = Field(description="Whether this is the current role")
    summary: Optional[str] = None
    highlights: Optional[List[str]] = None

class EducationModel(BaseModel):
    institution: str = Field(description="Educational institution name")
    qualification: Optional[str] = None
    course: str = Field(description="Field of study or course name")
    start: Optional[str] = None
    end: Optional[str] = None
    grade: Optional[str] = None
    location: Optional[LocationModel] = None

class CertificationModel(BaseModel):
    name: str = Field(description="Certification name")
    issuer: Optional[str] = None
    date: Optional[str] = None

class ProfessionalMembershipModel(BaseModel):
    institution: str = Field(description="Professional organization name")
    name: str = Field(description="Membership type/level")

class PublicationModel(BaseModel):
    pubType: Optional[str] = None
    title: str = Field(description="Publication title")
    date: Optional[str] = None

class ParsingDataModel(BaseModel):
    firstName: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    links: Optional[List[LinkModel]] = None
    location: Optional[LocationModel] = None
    headline: str = Field(description="Professional headline")
    profileStatement: str = Field(description="Professional summary")
    skills: List[SkillModel] = Field(description="Professional skills")
    achievements: List[str] = Field(description="Notable achievements")
    languages: Optional[List[LanguageModel]] = None
    experience: List[ExperienceModel] = Field(description="Work experience")
    education: Optional[List[EducationModel]] = None
    certifications: Optional[List[CertificationModel]] = None
    professionalMemberships: Optional[List[ProfessionalMembershipModel]] = None
    publications: Optional[List[PublicationModel]] = None
    additionalDetails: Optional[List[str]] = None

class ParsingResponseSchema(BaseResponseSchema):
    """Schema for CV/resume parsing response"""
    data: ParsingDataModel = Field(description="Parsed CV data")

# Competency and Skills Schema Models
class CSSkillModel(BaseModel):
    name: Annotated[str, Field(description="Standardized skill name", max_length=50)]
    proficiency: SkillProficiencyEnum = Field(description="Skill proficiency level")
    skillType: SkillTypeEnum = Field(description="Skill type")

class CSDataModel(BaseModel):
    skills: Annotated[List[CSSkillModel], Field(
        description="Prioritized skills",
        min_length=5,
        max_length=14
    )]
    feedback: FeedbackModel = Field(description="Analysis feedback")

class CSResponseSchema(BaseResponseSchema):
    """Schema for skills and competency assessment"""
    data: CSDataModel = Field(description="Skills assessment data")

# Knowledge and Achievements Schema Models
class KADataModel(BaseModel):
    achievements: Annotated[List[Annotated[str, Field(max_length=300)]], Field(
        description="STAR-formatted achievements",
        min_length=2,
        max_length=8
    )]
    feedback: FeedbackModel = Field(description="Analysis feedback")

class KAResponseSchema(BaseResponseSchema):
    """Schema for knowledge and achievements assessment"""
    data: KADataModel = Field(description="Achievements assessment data")

# Profile Statement Schema Models
class PSDataModel(BaseModel):
    profileStatement: Annotated[str, Field(description="Optimized professional summary", max_length=750)]
    feedback: FeedbackModel = Field(description="Analysis feedback")

class PSResponseSchema(BaseResponseSchema):
    """Schema for profile statement optimization"""
    data: PSDataModel = Field(description="Profile statement data")

# Role Schema Models
class RoleModel(BaseModel):
    title: Annotated[str, Field(description="Standardized job title", max_length=100)]
    start: Optional[str] = Field(description="Role start date")
    end: Optional[str] = Field(description="Role end date")
    current: bool = Field(description="Whether this role is current")

class RoleDataModel(BaseModel):
    company: Annotated[str, Field(description="Company name", max_length=100)]
    start: Optional[str] = None
    end: Optional[str] = None
    current: bool = Field(description="Whether this is current")
    summary: Optional[Annotated[str, Field(description="Responsibilities overview", max_length=400)]] = None
    highlights: Optional[Annotated[List[Annotated[str, Field(max_length=200)]], Field(
        description="Key achievements",
        max_length=6
    )]] = None
    roles: Annotated[List[RoleModel], Field(
        description="Positions held",
        min_length=1,
        max_length=10
    )]
    feedback: FeedbackModel = Field(description="Analysis feedback")

class RoleResponseSchema(BaseResponseSchema):
    """Schema for work experience role optimization"""
    data: RoleDataModel = Field(description="Role optimization data")

# Scoring Schema Models
class ScoresModel(BaseModel):
    overall: float = Field(description="Overall weighted score (0-100)", ge=0, le=100)
    relevance: float = Field(description="Match with job requirements (0-100)", ge=0, le=100)
    skillsAlignment: float = Field(description="Alignment of skills with requirements (0-100)", ge=0, le=100)
    experienceMatch: float = Field(description="Match of experience with requirements (0-100)", ge=0, le=100)
    achievementFocus: float = Field(description="Focus on achievements and results (0-100)", ge=0, le=100)
    presentation: float = Field(description="CV formatting and readability (0-100)", ge=0, le=100)
    atsCompatibility: float = Field(description="Likely success with ATS systems (0-100)", ge=0, le=100)

class ScoringDataModel(BaseModel):
    scores: ScoresModel = Field(description="Numerical scores across dimensions")
    feedback: FeedbackModel = Field(description="Analysis feedback")
    matchAssessment: Optional[Annotated[str, Field(description="Overall assessment of candidate fit or CV quality", max_length=500)]] = None

class ScoringResponseSchema(BaseResponseSchema):
    """Schema for CV scoring against job description"""
    data: ScoringDataModel = Field(description="Scoring assessment data")

# Schema registry mapping task names to their corresponding Pydantic models
SCHEMA_REGISTRY = {
    'parsing': ParsingResponseSchema,
    'role': RoleResponseSchema,
    'cs': CSResponseSchema,
    'ka': KAResponseSchema,
    'ps': PSResponseSchema,
    'scoring': ScoringResponseSchema
} 