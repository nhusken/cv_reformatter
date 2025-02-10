from langchain.prompts import PromptTemplate

def create_prompt(cv_content: str, template_content: str, example_content: str):
    prompt_template = PromptTemplate(
        input_variables=["cv", "template", "example"],
        template="""
        Rewrite the CV using the provided template and optional example.
        
        You will be given:
        
        Original CV: The current version of the CV.
        Template: The desired format for the new CV.
        Optional Example: A filled-out template with the data of somebody else.        
        
        Use only the information from the Original CV to populate the new Template.
        Steps
        Analyze the Original CV: Extract all relevant information, including personal details, work experience, education, skills, and any other pertinent sections.
        Map Information to Template: Align the extracted data with the corresponding sections in the new Template, ensuring that each piece of information fits appropriately.
        Incorporate Optional Example: If an example is provided, use it to guide the tone, style, and formatting, ensuring consistency with the filled-out template.
        Format and Review: Ensure the rewritten CV adheres to the new Template's structure and formatting guidelines. Check for clarity, conciseness, and correctness.
        Finalize the CV: Prepare the final version of the rewritten CV in the specified output format.
        Output Format
        Provide the rewritten CV in the same format as the provided Template. Ensure that all sections are properly formatted and that the content aligns with the structure of the Template.
        
        Notes
        Ensure that no new information is added beyond what is present in the Original CV.
        Maintain a professional and consistent tone throughout the CV.
        Use the language of the template and example as a guide for the rewritten CV. Translate the CV content into the new format while preserving the original meaning.
        Pay attention to formatting details such as font style, size, and section headings as specified in the Template.

        # CV:
        {cv}
        
        # Example
        {example}
        
        # Template:
        {template}
        """
    )
    prompt = prompt_template.format(cv=cv_content, template=template_content, example=example_content)
    return prompt