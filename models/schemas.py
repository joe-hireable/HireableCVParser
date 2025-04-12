from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict, constr
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
    strengths: List[constr(max_length=200)] = Field(
        description="Effective aspects",
        min_items=1,
        max_items=5
    )
    areas_to_improve: List[constr(max_length=200)] = Field(
        description="Improvement suggestions",
        min_items=1,
        max_items=5
    )

class BaseResponseSchema(BaseModel):
    """Base class for all response schemas with common configuration"""
    model_config = ConfigDict(extra="ignore")
    
    status: StatusEnum = Field(description="Processing status")
    errors: Optional[List[ErrorModel]] = Field(default=None, description="List of errors encountered")

# Parsing Schema Models

# New Model for Roles within Parsing Experience
class ParsingRoleModel(BaseModel):
    title: str = Field(description="Job title for this specific role")
    start: Optional[str] = Field(description="Start date in this role (e.g., MMM YYYY or YYYY)")
    end: Optional[str] = Field(description="End date in this role (e.g., MMM YYYY or YYYY)")
    current: bool = Field(description="Whether this specific role is current")

class LinkModel(BaseModel):
    title: Optional[str] = Field(description="Link title or platform name")
    url: Optional[str] = Field(description="Full URL of the link")

class LocationModel(BaseModel):
    city: Optional[str] = Field(description="City name")
    country: Optional[str] = Field(description="Country name")
    postalCode: Optional[str] = Field(description="Postal code or ZIP")

class SkillModel(BaseModel):
    name: str = Field(description="Name of the skill")
    proficiency: SkillProficiencyEnum = Field(description="Proficiency level")
    skillType: SkillTypeEnum = Field(description="Skill type (hard/soft)")

class LanguageModel(BaseModel):
    name: str = Field(description="Language name")
    level: Optional[LanguageLevelEnum] = Field(description="Proficiency level")

class ExperienceModel(BaseModel):
    company: str = Field(description="Company or organization name")
    start: Optional[str] = Field(description="Overall start date of employment at the company")
    end: Optional[str] = Field(description="Overall end date of employment at the company")
    current: bool = Field(description="Whether this is the current company")
    summary: Optional[str] = Field(description="Brief summary of overall responsibilities at the company")
    highlights: Optional[List[str]] = Field(description="Key achievements during the tenure at the company")
    roles: List[ParsingRoleModel] = Field(description="Specific positions held at this company", min_items=1)

class QualificationModel(BaseModel):
    qualification: Optional[str] = Field(description="Degree or certification type")
    course: str = Field(description="Field of study or course name")
    start: Optional[str] = Field(description="Start date")
    end: Optional[str] = Field(description="End date")
    grade: Optional[str] = Field(description="Grade or classification")

class EducationModel(BaseModel):
    institution: str = Field(description="Educational institution name")
    location: Optional[LocationModel] = Field(description="Institution location")
    qualifications: Optional[List[QualificationModel]] = Field(description="Qualifications obtained")

class CertificationModel(BaseModel):
    name: str = Field(description="Certification name")
    issuer: Optional[str] = Field(description="Issuing organization")
    date: Optional[str] = Field(description="Date of certification")

class MembershipModel(BaseModel):
    institution: str = Field(description="Professional organization name")
    name: str = Field(description="Membership type/level")

class EarlierRoleModel(BaseModel):
    title: str = Field(description="Job title")
    start: Optional[str] = Field(description="Start date")
    end: Optional[str] = Field(description="End date")

class EarlierCareerModel(BaseModel):
    company: str = Field(description="Company name")
    start: Optional[str] = Field(description="Start date")
    end: Optional[str] = Field(description="End date")
    roles: List[EarlierRoleModel] = Field(description="Positions held")

class PublicationModel(BaseModel):
    pubType: Optional[str] = Field(description="Publication type")
    title: str = Field(description="Publication title")
    date: Optional[str] = Field(description="Publication date")

class ParsingDataModel(BaseModel):
    firstName: Optional[str] = Field(description="First name")
    surname: Optional[str] = Field(description="Last name")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    links: Optional[List[LinkModel]] = Field(description="Professional links")
    location: Optional[LocationModel] = Field(description="Current location")
    headline: str = Field(description="Professional headline")
    profileStatement: str = Field(description="Professional summary")
    skills: List[SkillModel] = Field(description="Professional skills")
    achievements: List[str] = Field(description="Notable achievements")
    languages: Optional[List[LanguageModel]] = Field(description="Languages known")
    experience: List[ExperienceModel] = Field(description="Work experience")
    education: Optional[List[EducationModel]] = Field(description="Educational background")
    certifications: Optional[List[CertificationModel]] = Field(description="Professional certifications")
    professionalMemberships: Optional[List[MembershipModel]] = Field(description="Professional memberships")
    earlierCareer: Optional[List[EarlierCareerModel]] = Field(description="Earlier career positions")
    publications: Optional[List[PublicationModel]] = Field(description="Published works")
    addDetails: Optional[List[str]] = Field(description="Additional details")

class ParsingResponseSchema(BaseResponseSchema):
    """Schema for CV/resume parsing response"""
    data: ParsingDataModel = Field(description="Parsed CV data")

# Competency and Skills Schema Models
class CSSkillModel(BaseModel):
    name: constr(max_length=50) = Field(description="Standardized skill name")
    proficiency: SkillProficiencyEnum = Field(description="Skill proficiency level")
    skillType: SkillTypeEnum = Field(description="Skill type")

class CSDataModel(BaseModel):
    skills: List[CSSkillModel] = Field(
        description="Prioritized skills",
        min_items=5,
        max_items=14
    )
    feedback: FeedbackModel = Field(description="Analysis feedback")

class CSResponseSchema(BaseResponseSchema):
    """Schema for skills and competency assessment"""
    data: CSDataModel = Field(description="Skills assessment data")

# Knowledge and Achievements Schema Models
class KADataModel(BaseModel):
    achievements: List[constr(max_length=300)] = Field(
        description="STAR-formatted achievements",
        min_items=2,
        max_items=8
    )
    feedback: FeedbackModel = Field(description="Analysis feedback")

class KAResponseSchema(BaseResponseSchema):
    """Schema for knowledge and achievements assessment"""
    data: KADataModel = Field(description="Achievements assessment data")

# Profile Statement Schema Models
class PSDataModel(BaseModel):
    profileStatement: constr(max_length=750) = Field(description="Optimized professional summary")
    feedback: FeedbackModel = Field(description="Analysis feedback")

class PSResponseSchema(BaseResponseSchema):
    """Schema for profile statement optimization"""
    data: PSDataModel = Field(description="Profile statement data")

# Role Schema Models
class RoleModel(BaseModel):
    title: constr(max_length=100) = Field(description="Standardized job title")
    start: Optional[str] = Field(description="Role start date")
    end: Optional[str] = Field(description="Role end date")
    current: bool = Field(description="Whether this role is current")

class RoleDataModel(BaseModel):
    company: constr(max_length=100) = Field(description="Company name")
    start: Optional[str] = Field(description="Overall employment start date")
    end: Optional[str] = Field(description="Overall employment end date")
    current: bool = Field(description="Whether this is current")
    summary: Optional[constr(max_length=400)] = Field(description="Responsibilities overview")
    highlights: Optional[List[constr(max_length=200)]] = Field(
        description="Key achievements",
        max_items=6
    )
    roles: List[RoleModel] = Field(
        description="Positions held",
        min_items=1,
        max_items=10
    )
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
    matchAssessment: Optional[str] = Field(description="Overall assessment of candidate fit or CV quality", max_length=500)

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