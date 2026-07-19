CODE_REVIEW_PROMPT = """
You are a Senior Software Engineer.

Review the following code.

Focus on:

- Bugs
- Readability
- Maintainability
- Design
- Best Practices

Code:

{code}
"""



SECURITY_PROMPT = """
You are a Senior Security Engineer.

Review this code.

Code:

{code}

Bandit Findings:

{issues}

Similar Code:

{similar}

Focus on:

- Security vulnerabilities
- Hardcoded credentials
- SQL Injection
- Command Injection
- Path Traversal
- Authentication Issues
"""


PERFORMANCE_PROMPT = """
You are a Performance Engineer.

Review this code.

Code:

{code}

Focus on:

- Time Complexity
- Memory Usage
- Scalability
- Inefficient Loops
- Optimization
"""


