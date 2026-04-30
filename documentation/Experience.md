# Experience
Experience comes in three different forms.
1. **Personal Information**: This type of experience contains information that is tied to yourself. e.g. your name, education, phone number, general skills.
2. **Work Experience**: This type of experience contains information related to one of your past jobs.
3. **Personal Project**: This type of experience contains information related to everything else.


## Loading Experience into the Resume Tailor
All Experience is found by the Resume Tailor within a single folder as specified by the `EXPERIENCE_DATA_PATH` env variable. The default folder is called `experience`. This folder can have other folders allowing for as much organization as you need. 


## Experience Templates
Experience templates can be tuned to your preferences. Since the conversion between experience and the resume template is done via an LLM, there are no hard formats required. This fixed structure exists (instead of loading in arbitrary YAML) because it allows the Resume Tailor to pass context for each item to the LLM, making the conversion between experience and the resume template required fields much smoother.

### Updating the Experience Templates
If the current format does not align with your needs and you want to update the experience, you have options. If you want to make small changes, you can do so by modifying the experience types in the folder `src/experience/experience_types`. If you want to make an entirely new experience type, you will need to create another experience type in the `src/experience/experience_types` folder. You will then need to update the constants `SUPPORTED_DATA_TYPES` and `EXPERIENCE_DATA_TYPES` within `src/experience/data_loader.py` to include your new experience type. 


Below is the suggested experience format.


### Personal Information
```yaml
# Personal Information

name: "your-name"
# an open dict for additional personal information. You can add any key value pair that you want here.
reachout_points:
  important-key: "important value"
  address: "your-address"
  phone: "your-phone-number"
  email: "your-email-address"
  linkedin: "your-linkedin-profile"
  github: "your-github-username"

# If you have no education, set this to an empty list: []
list_of_education:
  - degree: "your-degree"
    level: "your-level"
    institution: "your-institution"
    graduation_year: "your-graduation-year"
    location: "your-location"


# If you have no certifications, set this to an empty list: []
list_of_certifications:
  - certification_name: "your-certification-name"
    year_obtained: "year-obtained"
    month_obtained: "month-obtained"

list_of_skills:
  - "your-languages-1"
```

### Work Experience
```yaml
company: "your-company-name"
list_of_titles:
    - "your-title-1"
    - "your-title-2"
city: "your-city"
region: "your-region"
start_date: "your-start-date"
# If currently employed, do not use an end_date field
end_date: "your-end-date"
# You can have multiple experiences in a single company. Think about all the projects the company had you do.
list_of_experiences:
    - description: >
            An optional description of your work experience. Detailing responsibilities, achievements, and technologies used. Not included in the experience selection prompt but can be used for cover letter generation or other future enhancements.
        technologies_used:
            - "your-technology-1"
            - "your-technology-2"
        list_of_resume_lines:
            - template_resume_line: "your-resume-line-example"
                substitution_suggestions: [
                        "suggestion in how to modify your resume line if required"
                ]
```

### Personal Project Experience
```yaml
project_name: "your-project-name"
date_last_worked_on: "your-last-date"
description: >
  An optional description of the personal project. Detailing achievements, and technologies used. Used for helping the llm tweak resume points and overall resume structure. Not included in the experience selection prompt but can be used for cover letter generation or other future enhancements.
technologies_used:
  - "tech-1"
list_of_resume_lines:
  - template_resume_line: "Line about what you did in the project and the impact it had. This is what the llm will tweak to tailor your resume."
    substitution_suggestions: []
```