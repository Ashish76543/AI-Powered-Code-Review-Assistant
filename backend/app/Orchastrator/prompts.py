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


RISK_PROMPT = """
You are a Senior Engineering Manager.

Below are three reviews.

Code Review:

{code}

Security Review:

{security}

Performance Review:

{performance}

Determine the overall risk of merging this Pull Request.

Return ONLY one of:

LOW
MEDIUM
HIGH
CRITICAL
"""