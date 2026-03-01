import pytest


from src.job_analytics.job_details_retriever import get_job_details, JobDetails


def test_get_job_details():
    job_description = """
    We are looking for a Software Engineer at TechCorp.
    """

    expected_details = JobDetails(
        company_name="TechCorp",
        position="Software Engineer",
    )

    retrieved_details = get_job_details(job_description)

    assert (
        retrieved_details == expected_details
    ), f"Expected :{expected_details}\n, but got \n{retrieved_details}"
