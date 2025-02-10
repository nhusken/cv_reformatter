# cv_reformatter.py
import logging
from typing import Optional
from werkzeug.datastructures import FileStorage
from langchain_core.output_parsers import StrOutputParser
from parse_docx import convert_to_markdown
from prompt_template import create_prompt
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_llm():
    from langchain_openai import AzureChatOpenAI
    deployment = "gpt-4o-mini"
    llm = AzureChatOpenAI(
        azure_deployment=deployment,
        api_version="2024-08-01-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    logging.info(f"Using {deployment}")
    return llm


def safe_convert_to_markdown(file: Optional[FileStorage]) -> str:
    """Safely convert a file to markdown, handling None case."""
    if file is None:
        return ""
    try:
        return convert_to_markdown(file)
    except Exception as e:
        logging.error(f"Error converting file {file.filename if file else 'None'} to markdown: {e}")
        raise ValueError(f"Error processing file {file.filename if file else 'None'}: {str(e)}")


def reformat_cv_with_llm(
        cv_file: FileStorage,
        template_file: FileStorage,
        example_file: Optional[FileStorage] = None
) -> str:
    """
    Reformat the CV content according to the given template using LangChain.

    Args:
        cv_file: The CV file to reformat (required)
        template_file: The template file to use (required)
        example_file: An optional example file

    Returns:
        Reformatted CV content as string
    """
    try:
        logging.info("Extracting text from CV file")
        cv_content = safe_convert_to_markdown(cv_file)
        logging.debug(f"CV content extracted: {cv_content[:100]}...")

        logging.info("Extracting text from template file")
        template_content = safe_convert_to_markdown(template_file)
        logging.debug(f"Template content extracted: {template_content[:100]}...")

        # Handle optional example file
        example_content = ""
        if example_file:
            logging.info("Extracting text from example file")
            example_content = safe_convert_to_markdown(example_file)
            logging.debug(f"Example content extracted: {example_content[:100]}...")

        logging.debug("Loading LLM")
        llm = load_llm()

        logging.info("Creating prompt")
        prompt = create_prompt(cv_content, template_content, example_content)
        logging.debug(f"Prompt created: {prompt[:100]}...")

        logging.info("Invoking LLM with prompt")
        result = llm.invoke(prompt)

        logging.info("Parsing LLM result")
        parser = StrOutputParser()
        result = parser.invoke(result)
        logging.debug(f"Parsed result: {result[:100]}...")

        return result

    except Exception as e:
        logging.error(f"Error in reformat_cv_with_llm: {str(e)}")
        raise