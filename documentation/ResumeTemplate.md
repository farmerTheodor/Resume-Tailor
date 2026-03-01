# Resume Templates
In the Resume Tailor, a resume template is a combination of two things:
- Template: A [Jinja](https://github.com/pallets/jinja) template that can be used to create a PDF. 
- Required Fields: The required data to fill out the template.

Once you create those two items and place them in a new folder within `./resume_templates`, you have created a new resume template. 

## Supported Template Types
**Latex** is currently the only resume template type that is supported. If you want to extend this code to support other types, look into editing the python files within the `src/resume_output` folder. Everything related to templating and compiling should all be contained within that folder.

## Swapping Between Templates
To swap between templates you must:
1. Open your `.env` file. 
2. Modify the `DEFAULT_TEMPLATE_PATH` environment variable with the full path to the folder of your template.
    - Example: `DEFAULT_TEMPLATE_PATH=/workspace/resume_templates/<your_template_here>`


## Generating A New Resume Template
Generating a new resume template can be fairly easy depending on how hands-on you want to be. If you want AI to do most of the work for you, I would suggest using the prompt at the bottom of this document. Regardless of whether you write it using AI or not, it is good to read the documentation.

### Required Files
In order for a template to exist, there must be at least two files. These files must be called `template` and `required_fields` respectively. 
#### Template Files
The template file will contain a Jinja template that the Resume Tailor can populate. This Jinja template can be structured however you see fit. However, there is a caveat for LaTeX files. LaTeX files share some of the same syntax as Jinja templates. Therefore, we have updated the Jinja templates to utilize this syntax instead.
```python
block_start_string="<%"
block_end_string="%>"
variable_start_string="<<"
variable_end_string=">>"
comment_start_string="<#"
comment_end_string="#>"
```
Below is an example of what using them would look like. 
```
<% for job in experience %>
    \resumeSubheading
    {<< job.role >>}{<< job.dates >>}
    {<< job.company >>}{<< job.location >>}
    \resumeItemListStart
    <% for bullet in job.bullets %>
        \resumeItem{<< bullet.value >>}
    <% endfor %>
    \resumeItemListEnd
<% endfor %>
```

The Resume Tailor is very flexible in its data structure. As the Resume Tailor uses AI to transform your experience into the required fields for your template, there are almost no rules in how you structure your template. 
 
#### Required Fields File
The Required Fields file describes the data structure that the template files require. It also contains instructions for an AI on what each field of the data structure should be. For example, here is an oversimplified jinja template that prints out bullet points. 

```
# template.tex
<% for bullet in bullets %>
    - {<< bullet >>}
<% endfor %>
```
The matching required_fields.py file looks like this:
```python
# required_fields.py
class RequiredFields(BaseModel):
    bullets: list[str] = Field(
        ...,
        description="Points that highlight the experience relevant to the job description"
    )
```
**Two things are necessary for the required fields file:** 
1. It is named `required_fields.py`
2. It contains a Pydantic model called `RequiredFields`.

These are necessary as it is how the Resume Tailor can discover and dynamically load the data structure. It dynamically loads the `required_fields` Python file and then looks for a class called `RequiredFields`. If it cannot find either, it will error out. 

### Keeping the Output of a Template to One Page
One feature you can use to improve the results of the Resume Tailor is called **Removable Experience**. Removable Experience is exactly what its name implies. It is something that can be removed from a resume without messing up the format. This is useful as sometimes the AI overselects experience, which then creates a multi-page resume. By having the AI rank each piece of Removable Experience for relevance to the job description, we can systematically remove bullet points until we get our one-page resume. To utilize Removable Experience we must include it in our data structure of both our template and `required_fields` files. Removable Experience uses a data structure with only two fields:
- **rank**: A scale of 1-5 of how important this is relative to the other values.
- **value**: The original value that the Jinja template will use. 

For example, if you want your bullet points to be Removable Experience, you would go from this:
```python
# required_fields.py
class RequiredFields(BaseModel):
    bullets: list[str] = Field(
        ...,
        description="Points that highlight the experience relevant to the job description"
    )
```
```
# template.tex
<% for bullet in bullets %>
    \resumeItem{<< bullet >>}
<% endfor %>
```
To 
```python
# required_fields.py
class RemovableExperience(BaseModel):
    rank: int = Field(
        ...,
        description="A scale of 1-5 of how important this is to the job description relative to the other values. The lowest value will be cut from the resume first.",
    )
    value: str = Field(
        ...,
        description="This is the value that the jinja template will use.",
    )
class RequiredFields(BaseModel):
    bullets: list[RemovableExperience] = Field(
        ...,
        description="Points that highlight the experience relevant to the job description"
    )
```
```
# template.tex
<% for bullet in bullets %>
    \resumeItem{<< bullet.value >>}
<% endfor %>
```


## Prompts
### LaTeX Template Generation Prompt
This prompt will generate the two necessary files as mentioned above. Replace `<<Paste your latex resume here>>` with the LaTeX file you want to transform into a prompt.
```
# Task
Create two files for me to use:
## File 1 (template.tex): 
Convert this input LaTeX resume into a Jinja template. 
Call this file template.tex

## File 2 (required_fields.py):
Based on that Jinja template create a Pydantic model called RequiredFields. This model will include all the fields necessary to complete the Jinja template fully. Include some extra fields for the program to use.
For each field create a description that explains what the field is used for. Describe how long each section should be without specifying the number of lines.
Keep these models simple to understand as another LLM has to follow this.
Call this file required_fields.py
For each item that can be removed use this format for the Pydantic model:
- name: rank 
  description: A scale of 1-5 of how important this is relative to the other. The lowest value will be cut from the resume first
- name: value
  description: This is the value that the Jinja template will use



## Jinja Format

Instead of the default strings for jinja use these instead. As the original conflicts with the latex

- block_start_string="<%"
- block_end_string="%>"
- variable_start_string="<<"
- variable_end_string=">>"
- comment_start_string="<#"
- comment_end_string="#>"

# Input
## LaTeX Resume

<<Paste your latex resume here>>

```
