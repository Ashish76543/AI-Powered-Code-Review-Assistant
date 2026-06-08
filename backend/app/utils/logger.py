import logging


##logging is used for  log instead of printing mmultiple levels are present and specifyign level prints from that level and below(more serious)
# DEBUG    -> very detailed internal info
# INFO     -> normal important events
# WARNING  -> something suspicious
# ERROR    -> something failed
# CRITICAL -> serious crash/problem
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

##only prints from info to below ,format give time ,levelname and message

logger = logging.getLogger(__name__)

##create logger object