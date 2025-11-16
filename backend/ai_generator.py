# ai_generator.py
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

def generate_documentation(code_text: str, parsed_structure: dict) -> str:
    """
    Use Groq LLM to generate documentation. Returns Markdown string.
    If Groq fails, returns a graceful fallback summary.
    """
    try:
        prompt = f"""
# You are an expert senior software engineer and technical writer.
# Generate clear, professional Markdown documentation for the following Python code.

# INSTRUCTIONS:
# - Start with a short **Overview** (2-3 sentences).
# - Add a **Purpose** section.
# - Add a **Table of Contents** placeholder (the PDF generator will create page numbers).
# - For each class: name + description + method list.
# - For each function: signature, purpose, parameters and return (if obvious).
# - Add an **Imports** section: explain why important imports are used.
# - Add a **How it works** section: describe flow and interactions.
# - Add **Example usage** if relevant.
# - Use Markdown formatting (headings, bullet lists, code blocks).
# - Keep it professional and concise.

# CODE:


PARSED_STRUCTURE:
{parsed_structure}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert technical writer and software engineer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
        )

        # Groq returns message objects; use .content property
        return response.choices[0].message.content

    except Exception as e:
        # Always return a fallback short summary if remote call fails
        print("GROQ ERROR:", e)
        lines = []
        lines.append("# Overview\n")
        lines.append("Automatic documentation generation failed to contact the AI. A brief auto-summary follows.\n")
        # simple fallback: list imports, classes, functions
        lines.append("## Parsed Structure\n")
        lines.append("```\n" + str(parsed_structure) + "\n```\n")
        lines.append("## Note\n")
        lines.append(f"AI error: {e}\n")
        return "\n".join(lines)



































# import os
# from groq import Groq
# from dotenv import load_dotenv
# load_dotenv()


# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def generate_documentation(code, parsed):
#     try:
#         prompt = f"""
# You are an AI that generates clean, beginner-friendly documentation.

# Code:
# {code}

# Parsed structure:
# {parsed}

# Write detailed documentation in Markdown.
# """

#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3,
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         print("GROQ ERROR:", e)
#         return f"AI ERROR: {e}"
