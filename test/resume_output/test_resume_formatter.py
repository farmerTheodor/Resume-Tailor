import pytest
from pathlib import Path

from src.resume_output import get_formatted_resume, get_resume_template

from resume_templates.test_format.required_fields import (
    EducationItem,
    ExperienceItem,
    Header,
    ProjectItem,
    RankedItem,
    RequiredFields,
    SkillCategory,
)


@pytest.fixture()
def test_template_resume():
    return get_resume_template(Path("/workspace/resume_templates/test_format"))


def test_get_formatted_resume_with_valid_data(test_template_resume):
    output = get_formatted_resume(
        template_resume=test_template_resume,
        required_fields=_get_dummy_required_fields(),
    )

    assert "Test User" in output


def test_get_formatted_resume_with_unescaped_characters_for_latex_resume(
    test_template_resume,
):
    work_experience = _get_dummy_experience_item(
        role="Developer & Engineer",
        company="Test Corp #1",
        dates="2022 - Present",
        bullets=[
            RankedItem(
                rank=5, value="Developed using $, %, &, #, _, {, }, ~, ^, and \\."
            )
        ],
    )
    skills = [
        _get_dummy_skill_category(
            category_name="Languages",
            skills="Python, C#, JavaScript & TypeScript",
        )
    ]

    required_fields = _get_dummy_required_fields(
        experience=[work_experience],
        skills=skills,
    )

    output = get_formatted_resume(
        template_resume=test_template_resume, required_fields=required_fields
    )

    assert "Developed using $, %, &, #, _, {, }, ~, ^, and \\." not in output
    assert "Developer \\& Engineer" in output
    assert "Test Corp \\#1" in output
    assert "2022 - Present" in output
    assert "Python, C\\#, JavaScript \\& TypeScript" in output


def _get_dummy_required_fields(
    header: Header = None,
    education: list[EducationItem] = None,
    experience: list[ExperienceItem] = None,
    projects: list[ProjectItem] = None,
    skills: list[SkillCategory] = None,
    target_job_title: str = "Software Engineer",
    max_resume_pages: int = 1,
) -> RequiredFields:
    if header is None:
        header = _get_dummy_header()
    if education is None:
        education = [_get_dummy_education_item()]
    if experience is None:
        experience = [_get_dummy_experience_item()]
    if projects is None:
        projects = [_get_dummy_project_item()]
    if skills is None:
        skills = [_get_dummy_skill_category()]

    return RequiredFields(
        header=header,
        education=education,
        experience=experience,
        projects=projects,
        skills=skills,
        target_job_title=target_job_title,
        max_resume_pages=max_resume_pages,
    )


def _get_dummy_header(
    name="Test User",
    phone="555-0100",
    email="test@example.com",
    linkedin="linkedin.com/in/testuser",
    github="github.com/testuser",
) -> Header:
    return Header(
        name=name,
        phone=phone,
        email=email,
        linkedin=linkedin,
        github=github,
    )


def _get_dummy_education_item(
    institution="Test University",
    location="Test City, TS",
    degree="BS in CS",
    dates="Aug. 2016 -- May 2020",
) -> EducationItem:
    return EducationItem(
        institution=institution,
        location=location,
        degree=degree,
        dates=dates,
    )


def _get_dummy_experience_item(
    role="Developer",
    company="Test Corp",
    location="Test City, TS",
    dates="Jan. 2020 -- Present",
    bullets=None,
) -> ExperienceItem:
    if bullets is None:
        bullets = [RankedItem(rank=5, value="Built software")]
    return ExperienceItem(
        role=role,
        company=company,
        location=location,
        dates=dates,
        bullets=bullets,
    )


def _get_dummy_project_item(
    title="Test Project",
    technologies="Python",
    dates="2020 -- Present",
    bullets=None,
) -> ProjectItem:
    if bullets is None:
        bullets = [RankedItem(rank=5, value="A test project")]
    return ProjectItem(
        title=title,
        technologies=technologies,
        dates=dates,
        bullets=bullets,
    )


def _get_dummy_skill_category(
    category_name="Languages",
    skills="Python",
) -> SkillCategory:
    return SkillCategory(
        category_name=category_name,
        skills=skills,
    )
