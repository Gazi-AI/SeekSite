"""
SeekSite Prompt Enhancer v3
============================
- Enforces NO FRAMEWORKS (Anti-Bootstrap)
- Injects Pollinations AI Images for realism
- Hardens DNA class usage
"""

from design_engine import build_design_dna

# Updated template with IMAGE support and NO-FRAMEWORK enforcement
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<!-- CSS otomatik olarak bu araya enjekte edilecektir. <style> etiketi açmaya gerek yoktur. -->
</head>
<body>
<!-- ÖNEMLİ: Sadece <body> içindeki içeriği yaz. <nav> ile başla. -->
"""

def build_system_prompt(design_dna):
    palette = design_dna["palette"]
    template = TEMPLATE_HTML.format(
        primary=palette['primary'],
        secondary=palette['secondary'],
        accent=palette['accent'],
        bg_dark=palette['bg_dark'],
        bg_card=palette['bg_card']
    )
    
    return f'''## CONTENT GUIDELINES:
1. SAKIN BOOTSTRAP VEYA TAILWIND KULLANMA. Sadece saf HTML yaz.
2. Sadece verilen DNA CSS sınıflarını kullan. Bu sınıflar (.hero, .feature-card, .btn-primary) arka planda tanımlıdır.
3. GÖRSELLER: <img src="https://picsum.photos/seed/{{word}}/1200/800" alt="{{desc}}"> formatını kullan. (Flux kaldırıldı)
4. METİNLER: Profesyonel ve ikna edici Türkçe metinler yaz.

## YOUR JOB:
Aşağıdaki yapıyı takip ederek <body> içeriğini oluştur. Gemma gibi modeller için bu yapı ZORUNLUDUR:

- <nav>: .logo (isim), .nav-links (ul>li>a), .cta-btn (button) sınıflarını kullan.
- <section class="hero">: .container > .hero-content > h1 (gradient için <span> kullan), p, .hero-buttons (.btn-primary, .btn-secondary)
- <section class="features">: .container > .section-header (.section-tag, h2, p), .features-grid > .feature-card (.feature-icon, h3, p)
- <section class="stats">: .container > .stats-grid > .stat-item (h3, p)
- <section class="pricing">: .container > .pricing-grid > .price-card (h3, .price, .price-features, .btn-primary)
- <footer>: .container > .footer-grid, .footer-bottom

## WORKING TEMPLATE:
{template}

## OUTPUT RULE:
Sadece <body> içeriğini ve kapanış etiketlerini yaz. Başka açıklama ekleme."""

## MANDATORY JS (APPEND TO BODY):
<script>
window.addEventListener('scroll',()=>{{const n=document.querySelector('nav');if(n)n.classList.toggle('scrolled',window.scrollY>50)}});
(function(){{
    const hb=document.querySelector('.hamburger'),nl=document.querySelector('.nav-links');
    if(hb)hb.addEventListener('click',()=>nl.classList.toggle('active'));
}})();
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',function(e){{e.preventDefault();const t=document.querySelector(this.getAttribute('href'));if(t)t.scrollIntoView({{behavior:'smooth'}})}}));
</script>
</body>
</html>

Output only the body content and closing tags.'''

def enhance_prompt(user_prompt, existing_code=None, conversation_history=None):
    import re
    messages = []
    if existing_code:
        # Strip CSS to save thousands of tokens; the LLM doesn't need to modify it anyway
        existing_code_no_style = re.sub(r'<style>.*?</style>', '<!-- SYSTEM AUTO-INJECTED CSS -->', existing_code, flags=re.DOTALL | re.IGNORECASE)
        messages.append({"role": "system", "content": f"Modify this code. Output COMPLETE HTML. DO NOT write <style> tags, they are injected by the system automatically.\n\nCODE:\n{existing_code_no_style}"})
        if conversation_history: messages.extend(conversation_history[-4:])
        messages.append({"role": "user", "content": user_prompt})
    else:
        dna = build_design_dna(user_prompt)
        messages.append({"role": "system", "content": build_system_prompt(dna)})
        if conversation_history: messages.extend(conversation_history[-4:])
        messages.append({"role": "user", "content": f"Create a website about: {user_prompt}. Start with <nav>."})
    return messages

def get_enhancement_prompt(enhancement_type):
    prompts = {
        'dark_mode': 'Add dark mode toggle.',
        'animations': 'Add CSS animations.',
        'modern_ui': 'Add glassmorphism.',
    }
    return prompts.get(enhancement_type, enhancement_type)
