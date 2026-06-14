import tempfile
## to create a temporary file
import subprocess
##to implement direct system calls
import json

import os


def run_bandit(code: str):

    with tempfile.NamedTemporaryFile(
        suffix=".py",
        mode="w",
        delete=False
    ) as temp:
    ##create temp file with extension.py ,write more and dont delet as soon as created,store in temp
        temp.write(code)
        ##write into temp
        temp_path = temp.name
        ##store the path to the file
    try:

        result = subprocess.run(
            [
                "bandit",
                "-f",
                "json",
                temp_path
            ],##run as bandit -f json temporary.py ,basically execute and get result using bandit
            capture_output=True,##dont print to console,capture in variable
            text=True##output as json text
        )

        output = json.loads(result.stdout)##convert json text to dictionary

        return output.get("results", []) ##return the lust in dictionary with index key results,if not present return empty list

    except Exception:

        return []

    finally:

        os.remove(temp_path)