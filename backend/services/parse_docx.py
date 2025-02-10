import subprocess
import shutil
from pathlib import Path
import logging
import sys
import os
import tempfile
from werkzeug.datastructures import FileStorage
from typing import Union
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_pandoc_installed() -> bool:
    """Check if pandoc is available in the system."""
    return shutil.which('pandoc') is not None


def save_temporary_file(file_storage: FileStorage) -> str:
    """Save FileStorage object to a temporary file and return its path."""
    temp_fd, temp_path = tempfile.mkstemp(suffix='.docx')
    try:
        os.close(temp_fd)
        file_storage.save(temp_path)
        return temp_path
    except Exception as e:
        os.unlink(temp_path)
        raise e


def clean_table_markup(text: str) -> str:
    """Clean up table formatting to make it more readable."""
    lines = text.split('\n')
    cleaned_lines = []
    inside_table = False

    for line in lines:
        # Skip complex table formatting lines
        if re.match(r'^\+[-=]+\+$', line) or re.match(r'^\|[-=]+\|$', line):
            continue

        # Clean up table rows
        if line.startswith('|'):
            inside_table = True
            # Remove extra spaces and pipes
            line = re.sub(r'\|\s+', '| ', line)
            line = re.sub(r'\s+\|', ' |', line)
            # Remove dimension specifications
            line = re.sub(r'\{width=[^}]+\}', '', line)
            line = re.sub(r'\{height=[^}]+\}', '', line)
            cleaned_lines.append(line)
        else:
            if inside_table:
                # Add a blank line after table
                cleaned_lines.append('')
                inside_table = False
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def convert_to_markdown(file_input: Union[str, FileStorage], output_path: str = None) -> str:
    """
    Convert DOCX to Markdown using pandoc with simple table formatting.

    Args:
        file_input: Path to input DOCX file or Flask FileStorage object
        output_path: Optional path for output file. If None, returns markdown as string

    Returns:
        Markdown text if output_path is None, otherwise None
    """
    temp_path = None

    try:
        if not check_pandoc_installed():
            raise EnvironmentError("Pandoc is not installed. Please install pandoc first.")

        # Handle FileStorage input
        if isinstance(file_input, FileStorage):
            temp_path = save_temporary_file(file_input)
            input_path = temp_path
        else:
            input_path = str(file_input)
            if not Path(input_path).exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

        # Simple pandoc command focusing on basic markdown
        cmd = [
            'pandoc',
            str(input_path),
            '--from', 'docx',
            '--to', 'markdown_strict',
            '--wrap=none',
            '--columns=100'
        ]

        # Set up environment with proper encoding
        env = dict(os.environ)
        if sys.platform == 'win32':
            env['PYTHONIOENCODING'] = 'utf-8'

        if output_path:
            cmd.extend(['--output', str(output_path)])
            subprocess.run(cmd, env=env, check=True, encoding='utf-8')
            logger.info(f"Converted document to {output_path}")
            return None
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                check=True
            )

            # Clean up the output
            markdown = result.stdout

            # Basic cleanup
            markdown = markdown.strip()
            markdown = markdown.replace('\r\n', '\n')
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)

            # Clean up tables
            markdown = clean_table_markup(markdown)

            # Remove any remaining HTML
            markdown = re.sub(r'<[^>]+>', '', markdown)

            return markdown

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.encode('utf-8').decode('utf-8', errors='replace') if e.stderr else str(e)
        logger.error(f"Pandoc conversion failed: {error_msg}")
        raise
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        raise
    finally:
        # Clean up temporary file if it was created
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")


def save_markdown_to_file(markdown_text: str, output_path: str):
    """Save markdown text to file with proper encoding."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        logger.info(f"Saved markdown to {output_path}")
    except Exception as e:
        logger.error(f"Error saving markdown to file: {str(e)}")
        raise