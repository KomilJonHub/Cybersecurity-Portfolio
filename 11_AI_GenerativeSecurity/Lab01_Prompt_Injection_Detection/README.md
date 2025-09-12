# Lab01 - Prompt Injection Detection

## Objective
Create a basic script to identify potentially malicious instructions within Large Language Model prompts.

## Tools Used
- Python 3

## How It Works
The script scans input text for suspicious phrases such as "ignore previous instructions" or "override security". If a match is found, the prompt is flagged for further review.

## Sample Usage
```bash
python detect_injection.py
```

## Findings
- Simple heuristics can catch obvious injection attempts but require tuning for false positives.

## References
- [Prompt Injection Attacks](https://owasp.org/www-community/attacks/Prompt_injection)
