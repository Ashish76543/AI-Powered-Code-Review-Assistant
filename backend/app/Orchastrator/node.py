from app.utils.logger import logger


def validate_input(state):

    logger.info("========== LANGGRAPH START ==========")

    logger.info("Repository : %s", state["repo"])

    logger.info("PR Number : %s", state["pr_number"])

    logger.info("Files : %d", len(state["files"]))

    return state



def build_context(state):

    logger.info("Building Context")

    for file in state["files"]:

        logger.info("--------------------------------")

        logger.info(file["filename"])

        logger.info(file["code"])

        logger.info(file["analysis"])

        logger.info(file["issues"])

        logger.info(file["similar_files"])

    return state


def finish(state):

    logger.info("Context Ready")

    logger.info("========== LANGGRAPH END ==========")

    return state