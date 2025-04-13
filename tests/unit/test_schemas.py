import pytest
from pydantic import ValidationError
from models.schemas import (
    ParsingResponseSchema,
    CSResponseSchema,
    PSResponseSchema,
    RoleResponseSchema,
    ScoringResponseSchema,
    StatusEnum,
    SeverityEnum,
    SkillProficiencyEnum,
    SkillTypeEnum,
    LanguageLevelEnum
)


class TestSchemas:
    """Test cases for Pydantic schema models."""

    def test_parsing_response_valid(self):
        """Test that a valid ParsingResponseSchema can be created."""
        # Create a valid ParsingResponseSchema
        response_data = {
            "status": StatusEnum.SUCCESS,
            "data": {
                "firstName": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
                "phone": "+44 7700 900000",
                "links": [
                    {
                        "title": "LinkedIn",
                        "url": "https://linkedin.com/in/johndoe"
                    }
                ],
                "location": {
                    "city": "London",
                    "country": "United Kingdom",
                    "postalCode": "SW1A 1AA"
                },
                "headline": "Senior Software Engineer",
                "profileStatement": "Experienced Software Engineer with 5+ years of expertise in Python development and cloud infrastructure.",
                "skills": [
                    {
                        "name": "Python",
                        "proficiency": SkillProficiencyEnum.EXPERT,
                        "skillType": SkillTypeEnum.HARD
                    }
                ],
                "achievements": [
                    "Designed and implemented a microservices architecture on GCP, improving system reliability by 40%"
                ],
                "languages": [
                    {
                        "name": "English",
                        "level": LanguageLevelEnum.NATIVE
                    }
                ],
                "experience": [
                    {
                        "company": "Tech Innovations Ltd",
                        "title": "Senior Software Engineer",
                        "start": "January 2021",
                        "end": None,
                        "current": True,
                        "summary": "Leading backend development team",
                        "highlights": [
                            "Designed and implemented a microservices architecture on GCP"
                        ]
                    }
                ],
                "education": [
                    {
                        "institution": "University of London",
                        "qualification": "BSc",
                        "course": "Computer Science",
                        "start": "2012",
                        "end": "2016",
                        "grade": "First Class Honours",
                        "location": {
                            "city": "London",
                            "country": "United Kingdom",
                            "postalCode": "WC1E 6BT"
                        }
                    }
                ],
                "certifications": [
                    {
                        "name": "AWS Certified Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "date": "2020"
                    }
                ],
                "professionalMemberships": [
                    {
                        "institution": "British Computer Society",
                        "name": "Professional Member"
                    }
                ],
                "publications": [
                    {
                        "pubType": "Conference Paper",
                        "title": "Modern Python Development Practices",
                        "date": "2021"
                    }
                ],
                "additionalDetails": [
                    "Open source contributor",
                    "Tech community speaker"
                ]
            }
        }
        
        # Create the model instance
        response = ParsingResponseSchema(**response_data)
        
        # Assertions
        assert response.status == StatusEnum.SUCCESS
        assert response.data.firstName == "John"
        assert response.data.surname == "Doe"
        assert response.data.email == "john.doe@example.com"
        assert len(response.data.skills) == 1
        assert response.data.skills[0].name == "Python"
        assert len(response.data.experience) == 1
        assert response.data.experience[0].company == "Tech Innovations Ltd"
        assert response.data.location.city == "London"
        assert len(response.data.languages) == 1
        assert response.data.languages[0].name == "English"

    def test_parsing_response_invalid(self):
        """Test that an invalid ParsingResponseSchema raises ValidationError."""
        # Missing required fields
        invalid_data = {
            "status": StatusEnum.SUCCESS,
            "data": {
                "firstName": "John",
                # missing surname
                "email": "john.doe@example.com",
                # missing headline
                # missing profileStatement
                # missing skills
                # missing achievements
                # missing experience
            }
        }
        
        # Expect a ValidationError
        with pytest.raises(ValidationError):
            ParsingResponseSchema(**invalid_data)

    def test_cs_response_valid(self):
        """Test that a valid CSResponseSchema can be created."""
        response_data = {
            "status": StatusEnum.SUCCESS,
            "data": {
                "skills": [
                    {
                        "name": "Python",
                        "proficiency": SkillProficiencyEnum.EXPERT,
                        "skillType": SkillTypeEnum.HARD
                    },
                    {
                        "name": "JavaScript",
                        "proficiency": SkillProficiencyEnum.ADVANCED,
                        "skillType": SkillTypeEnum.HARD
                    },
                    {
                        "name": "Leadership",
                        "proficiency": SkillProficiencyEnum.ADVANCED,
                        "skillType": SkillTypeEnum.SOFT
                    },
                    {
                        "name": "Problem Solving",
                        "proficiency": SkillProficiencyEnum.EXPERT,
                        "skillType": SkillTypeEnum.SOFT
                    },
                    {
                        "name": "Docker",
                        "proficiency": SkillProficiencyEnum.INTERMEDIATE,
                        "skillType": SkillTypeEnum.HARD
                    }
                ],
                "feedback": {
                    "strengths": ["Strong technical skills"],
                    "areasToImprove": ["Could add more cloud skills"]
                }
            }
        }
        
        response = CSResponseSchema(**response_data)
        assert response.status == StatusEnum.SUCCESS
        assert len(response.data.skills) == 5
        assert response.data.skills[0].name == "Python"

    def test_role_response_valid(self):
        """Test that a valid RoleResponseSchema can be created."""
        response_data = {
            "status": StatusEnum.SUCCESS,
            "data": {
                "company": "Tech Corp",
                "start": "January 2021",
                "end": None,
                "current": True,
                "summary": "Leading development team",
                "highlights": ["Improved system performance by 50%"],
                "roles": [
                    {
                        "title": "Senior Developer",
                        "start": "January 2021",
                        "end": None,
                        "current": True
                    }
                ],
                "feedback": {
                    "strengths": ["Clear progression"],
                    "areasToImprove": ["Add more metrics"]
                }
            }
        }
        
        response = RoleResponseSchema(**response_data)
        assert response.status == StatusEnum.SUCCESS
        assert response.data.company == "Tech Corp"
        assert len(response.data.roles) == 1
        assert response.data.roles[0].title == "Senior Developer" 