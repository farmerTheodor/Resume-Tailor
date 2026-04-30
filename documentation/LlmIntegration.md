# LLM Integration

The Resume Tailor uses LLMs to do four things:
1. Select relevant experience for the resume.
2. Modify relevant experience if required.
3. Format the experience to fit the required fields as specified by the resume template.
4. (Optional) Select and format experience for the cover letter.

Currently, we use Open Router to do this. It was chosen because you can easily select more expensive or cheaper models without having to do much programming.

## Changing the model 
To change the default model that the Resume Tailor uses, update the environment variable `DEFAULT_MODEL` in the `.env` file. Set the environment variable to the Open Router model id. 

## Changing the provider
Currently only Open Router is supported. However, if you want to add more (i.e. make it local), follow these steps:
1. Add another source to the folder `src/llm`.
2. Implement the `get_structured_llm_response` similar to how it is done in `open_router_facade.py`.
3. Update `llm_interface.py` to point to your new source.


## Changing The Output
Currently within the Resume Tailor there are only four spots to change the output of the resume or cover letter. The spots are:
- **Your Experience**: The Resume Tailor takes in everything but the description of your experience. If you are finding that hallucinations are happening, it will typically be because of something in here.
- **Your Resume Template**: Within the descriptions of the fields and the variable names themselves. If, for whatever reason, the wording has been changed drastically, it is probably because of something in here.
- **The Resume Prompt**: The experience selector prompt for resumes is located in `src/experience/selector/prompts/resume_selection_prompt.md`. If changing the above two does not have the desired effect, update this.
- **The Cover Letter Prompt**: The experience selector prompt for cover letters is located in `src/experience/selector/prompts/cover_letter_selection_prompt.md`. If the cover letter output is not what you expect, update this.

## Debugging LLM Output
If you are struggling with wrangling the LLM to spit out something good. In order to debug LLM output, I have developed a flag that can be turned on and off through an environment variable `LLM_DEBUG_MODE`. To turn on the debug mode, set the environment variable equal to `true`. To turn it off, either unset the environment variable or change it to anything else.
Debug mode will modify the data structure coming out of the LLM to include a reason for each value. This will allow you to find logic bugs within your prompt, experience, or resume template.