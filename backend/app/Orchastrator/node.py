from app.utils.logger import logger


def validate_input(state):

    logger.info("========== LANGGRAPH START ==========")

    logger.info(state["repo"])

    logger.info(state["pr_number"])

    logger.info(len(state["files"]))

    return state


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

    return state


def code_review_agent(state):

    logger.info("Running Code Review Agent")

    state["code_review"] = "Code Review Finished"

    return state


def security_review_agent(state):

    logger.info("Running Security Agent")

    state["security_review"] = "Security Review Finished"

    return state


def performance_review_agent(state):

    logger.info("Running Performance Agent")

    state["performance_review"] = "Performance Review Finished"

    return state


def finish(state):

    logger.info("========== FINAL RESULT ==========")

    logger.info(state["code_review"])

    logger.info(state["security_review"])

    logger.info(state["performance_review"])

    logger.info("========== GRAPH END ==========")

    return state