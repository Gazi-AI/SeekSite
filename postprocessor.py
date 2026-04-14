"""
SeekSite Code Postprocessor (v4)
================================
- Strips Pollinations AI ads/promotions from generated code
- Wraps incomplete content in Design DNA templates
- Fixes CSS syntax errors and structural breaks
"""

import re
from design_engine import build_design_dna


def strip_pollinations_ads(code):
    """Remove Pollinations AI promotional text that gets injected into responses"""
    if not code:
        return code
    
    cleaned = code
    
    # Pattern 1: Full ad block with markdown formatting
    # ---\n**Support Pollinations.AI:**\n---\n🌸 **Ad** 🌸\nPowered by...
    cleaned = re.sub(
        r'-{2,}\s*\n?\s*\*{0,2}\s*Support Pollinations\.AI.*?keep AI accessible for everyone\.?\s*',
        '', cleaned, flags=re.DOTALL | re.IGNORECASE
    )
    
    # Pattern 2: Just the ad line
    cleaned = re.sub(
        r'🌸.*?Ad.*?🌸.*?\n?',
        '', cleaned, flags=re.DOTALL
    )
    
    # Pattern 3: Powered by line with link
    cleaned = re.sub(
        r'Powered by Pollinations\.AI.*?(?:accessible for everyone|pollinations\.ai/redirect/kofi\))\.?\s*',
        '', cleaned, flags=re.DOTALL | re.IGNORECASE
    )
    
    # Pattern 4: Support mission link
    cleaned = re.sub(
        r'\[Support our mission\]\(https?://pollinations\.ai[^\)]*\)[^\n]*',
        '', cleaned, flags=re.IGNORECASE
    )
    
    # Pattern 5: Standalone --- separators that were part of the ad (3+ dashes on their own line)
    # Only remove if they're clearly ad artifacts (consecutive ---)
    cleaned = re.sub(r'\n-{3,}\s*\n-{3,}\s*\n', '\n', cleaned)
    
    # Pattern 6: Any remaining pollinations references in non-code context
    cleaned = re.sub(
        r'\*{0,2}Support Pollinations\.AI:?\*{0,2}',
        '', cleaned, flags=re.IGNORECASE
    )
    
    # Clean up leftover empty lines from ad removal
    cleaned = re.sub(r'\n{4,}', '\n\n', cleaned)
    
    return cleaned


def clean_generated_code(code):
    """Clean LLM output: remove markdown wrappers and Pollinations ads"""
    if not code or not code.strip():
        return ""
    
    cleaned = code
    
    # Strip Pollinations ads FIRST
    cleaned = strip_pollinations_ads(cleaned)
    
    # Remove markdown code fences
    cleaned = re.sub(r'```(?:html?|css|javascript|js)?\s*\n?', '', cleaned)
    cleaned = re.sub(r'\n?```\s*$', '', cleaned)
    
    # Aggressive Chat Stripping: Remove common conversational prefixes and confusion messages
    chat_garbage = [
        r'^(?:I\'?m sorry|Sure|Here is|Certainly|Of course|I am not sure|Could you provide|I apologize|My apologies).*?(?=<!DOCTYPE|<html|<nav|<section|<div|<header|<footer|<style)',
        r'^(?:I\'?m sorry|I don\'?t have|Please provide|I need the exact|I am not sure what code).*?(?:\n|<|$)',
        r'^(?:Here is the remaining|Continuing from).*?[:\n]',
        # If the entire block is just I'm sorry / I'm not sure text (no tags)
        r'^(?:I\'?m sorry|I am not sure|I apologize).*?$'
    ]
    
    for pattern in chat_garbage:
        cleaned = re.sub(pattern, '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    # If the code starts with a quote followed by chat-like text, strip it
    if cleaned.startswith('"') or cleaned.startswith("'"):
        cleaned = re.sub(r'^["\'].*?["\']\s*', '', cleaned, flags=re.DOTALL)

    return cleaned.strip()


def auto_fix_html(code, user_prompt=""):
    """
    Intelligent wrapper. If the model didn't provide a full HTML,
    wrap the content in our 'Design DNA' template.
    """
    if not code or not code.strip():
        return code

    # If it already contains HTML skeleton tags (even if partial), just apply structural fixes.
    # We DO NOT want to wrap it inside another <body> tag and cause nested HTML syntax errors.
    if any(tag in code.lower() for tag in ['<html', '<head', '<body', '<!doctype html']):
        return _apply_structural_fixes(code)
    
    # If it looks like a partial or just content, wrap it!
    # This is the "Safety Net" for weak LLMs
    dna = build_design_dna(user_prompt)
    palette = dna["palette"]
    
    # Simple template wrapper
    template = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SeekSite Proje</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        {dna['css']}
        /* Fix for potential invisible content */
        body {{ min-height: 100vh; background: {palette['bg_dark']}; }}
    </style>
</head>
<body>
    {code}
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        // Init animations
        if(typeof AOS !== 'undefined') AOS.init({{ duration: 800, once: true }});
        
        // Navbar effect
        window.addEventListener('scroll', () => {{
            const nav = document.querySelector('nav');
            if(nav) nav.classList.toggle('scrolled', window.scrollY > 50);
        }});
        
        // Mobile toggle scoped
        (function(){{
            const hb = document.querySelector('.hamburger');
            const nl = document.querySelector('.nav-links');
            if(hb && nl) hb.addEventListener('click', () => nl.classList.toggle('active'));
        }})();
    </script>
</body>
</html>"""
    
    return _apply_structural_fixes(template)

def _apply_structural_fixes(code):
    """Fix syntax errors in CSS and common HTML breaks"""
    fixed = code
    
    # Strip ads one more time (safety net)
    fixed = strip_pollinations_ads(fixed)
    
    # Fix common CSS breaks (like box-shadowbox-shadow or incomplete media queries)
    fixed = fixed.replace('box-shadowbox-shadow:', 'box-shadow:')
    
    # Fix unclosed style/script tags
    if fixed.lower().count('<style') > fixed.lower().count('</style>'):
        fixed = fixed + '</style>'
    if fixed.lower().count('<script') > fixed.lower().count('</script>'):
        fixed = fixed + '</script>'
        
    # Ensure </html> exists
    if '</html>' not in fixed.lower():
        fixed = fixed + '</html>'
        
    return fixed

def validate_html(code):
    """Basic validation"""
    if not code.strip():
        return {"valid": False, "issues": ["Empty code"]}
    
    issues = []
    if '<html' not in code.lower(): issues.append("Missing <html>")
    if '</body>' not in code.lower(): issues.append("Missing </body>")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues
    }

def full_fix(code, user_prompt=""):
    """Complete pipeline"""
    cleaned = clean_generated_code(code)
    fixed = auto_fix_html(cleaned, user_prompt)
    validation = validate_html(fixed)
    return fixed, validation
