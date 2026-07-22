from app.utils.logger import logger

from app.Orchastrator.llm import get_llm
from app.Orchastrator.prompts import (
    CODE_REVIEW_PROMPT,
    SECURITY_PROMPT,
    PERFORMANCE_PROMPT,
)
from app.Orchastrator.prompts import RISK_PROMPT
llm = get_llm()

def validate_input(state):

    logger.info("========== LANGGRAPH START ==========")

    logger.info(state["repo"])

    logger.info(state["pr_number"])

    logger.info(len(state["files"]))

    return {}


def build_context(state):

    logger.info("Building Context")

    for file in state["files"]:

        logger.info("--------------------------------")

        logger.info(file["filename"])

        logger.info(file["status"])

        logger.info(file["patch"])

        logger.info(file["code"])

        logger.info(file["analysis"])

        logger.info(file["issues"])

        logger.info(file["similar_files"])

    return {}


def code_review_agent(state):

    reviews = []

    logger.info("Running Code Review Agent")

    for file in state["files"]:

        prompt = CODE_REVIEW_PROMPT.format(
            code=file["code"]
        )

        response = llm.invoke(prompt)

        reviews.append(
            f"""
        File: {file["filename"]}

        {response.content}
        """
                )

    return {
        "code_review": "\n".join(reviews)
    }






def security_review_agent(state):

    reviews = []

    logger.info("Running Security Review Agent")

    for file in state["files"]:

        prompt = SECURITY_PROMPT.format(
            code=file["code"],
            issues=file["issues"],
            similar=file["similar_files"],
        )

        response = llm.invoke(prompt)

        reviews.append(
            f"""
File: {file["filename"]}

{response.content}
"""
        )

    return {
        "security_review": "\n".join(reviews)
    }





def performance_review_agent(state):

    reviews = []

    logger.info("Running Performance Review Agent")

    for file in state["files"]:

        prompt = PERFORMANCE_PROMPT.format(
            code=file["code"]
        )

        response = llm.invoke(prompt)

        reviews.append(
            f"""
File: {file["filename"]}

{response.content}
"""
        )

    return {
        "performance_review": "\n".join(reviews)
    }







def aggregate_reviews(state):

    review = f"""
================ CODE REVIEW ================

{state['code_review']}

================ SECURITY REVIEW ================

{state['security_review']}

================ PERFORMANCE REVIEW ================

{state['performance_review']}
"""
    logger.info(">>> aggregate")
    return {
        "final_review": review
    }






def risk_assessment_agent(state):

    logger.info("Running Risk Assessment")

    prompt = RISK_PROMPT.format(
        code=state["code_review"],
        security=state["security_review"],
        performance=state["performance_review"]
    )

    response = llm.invoke(prompt)

    risk = response.content.strip().upper()

    logger.info(f"Risk: {risk}")

    return {
        "risk": risk
    }





def decide_next(state):

    risk = state["risk"]

    if risk in ["HIGH", "CRITICAL"]:
        return "deep_security"

    return "formatter"





def deep_security_agent(state):

    logger.info("Running Deep Security Review")

    reviews = []

    for file in state["files"]:

        prompt = f"""
You are a Senior Application Security Engineer.

The pull request has been classified as **{state["risk"]}** risk.

Perform a comprehensive security audit of the following file.

Repository:
{state["repo"]}

Pull Request:
{state["pr_number"]}

Filename:
{file["filename"]}

==================== CODE ====================

{file["code"]}

==================== AST ANALYSIS ====================

{file["analysis"]}

==================== BANDIT FINDINGS ====================

{file["issues"]}

==================== SIMILAR CODE ====================

{file["similar_files"]}

==================== PREVIOUS SECURITY REVIEW ====================

{state["security_review"]}

Your task:

1. Verify whether the previous security review missed anything.
2. Look for:
   - Hardcoded secrets
   - SQL Injection
   - Command Injection
   - Path Traversal
   - Insecure Deserialization
   - Authentication issues
   - Authorization issues
   - Unsafe file handling
   - Dangerous library usage
   - Business logic vulnerabilities
3. Explain the severity of every issue.
4. Suggest secure fixes.
5. Mention any false positives from Bandit if applicable.

Return your answer in markdown.
"""

        response = llm.invoke(prompt)

        reviews.append(
            f"""
## File: {file["filename"]}

{response.content}
"""
        )
    logger.info(">>> deep_security")
    return {
        "security_review": (
            state["security_review"]
            + "\n\n# Deep Security Review\n\n"
            + "\n".join(reviews)
        )
    }

def review_formatter(state):

    review = f"""
# Pull Request Review

Repository:
{state["repo"]}

PR:
{state["pr_number"]}

Overall Risk:
{state["risk"]}

--------------------------------

## Code Review

{state["code_review"]}

--------------------------------

## Security Review

{state["security_review"]}

--------------------------------

## Performance Review

{state["performance_review"]}
"""
    logger.info(">>> formatter")
    return {
        "final_review": review
    }




def finish(state):
    logger.info(">>> finish")
    logger.info(state["final_review"])

    return {}