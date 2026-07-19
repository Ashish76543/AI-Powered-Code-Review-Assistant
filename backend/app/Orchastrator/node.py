from app.utils.logger import logger

from app.Orchastrator.llm import get_llm
from app.Orchastrator.prompts import (
    CODE_REVIEW_PROMPT,
    SECURITY_PROMPT,
    PERFORMANCE_PROMPT,
)

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
        "security_review": reviews
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
        "performance_review": reviews
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

    return {
        "final_review": review
    }






def finish(state):

    logger.info(state["final_review"])

    return {}