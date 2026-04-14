"""
SeekSite Design DNA Engine
==========================
The secret sauce that makes even weak LLMs produce stunning websites.

Problem: Small models can code but they CAN'T IMAGINE beautiful designs.
Solution: We give them complete, pre-built CSS component code so they only 
need to assemble pieces and fill in content - zero imagination required.

This module provides ready-made HTML+CSS snippets for every section of a website.
The model's job becomes: pick components, fill text, customize colors.
"""

# ============================================================
# COLOR PALETTES - Curated, harmonious color systems
# ============================================================
COLOR_PALETTES = {
    "tech": {
        "name": "Tech / Modern",
        "keywords": ["teknoloji", "tech", "startup", "saas", "yazilim", "software", "app", "uygulama", "dijital", "digital", "ai", "yapay zeka"],
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "accent": "#a78bfa",
        "bg_dark": "#0f172a",
        "bg_card": "#1e293b",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%)",
        "hero_gradient": "linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa)",
        "text_gradient": "linear-gradient(135deg, #6366f1, #ec4899)",
    },
    "nature": {
        "name": "Nature / Health",
        "keywords": ["saglik", "health", "doga", "nature", "organik", "organic", "yesil", "green", "spa", "wellness", "fitness", "spor", "gym"],
        "primary": "#10b981",
        "secondary": "#059669",
        "accent": "#34d399",
        "bg_dark": "#022c22",
        "bg_card": "#064e3b",
        "bg_gradient": "linear-gradient(135deg, #022c22 0%, #064e3b 50%, #065f46 100%)",
        "hero_gradient": "linear-gradient(135deg, #10b981, #059669, #34d399)",
        "text_gradient": "linear-gradient(135deg, #10b981, #6ee7b7)",
    },
    "creative": {
        "name": "Creative / Art",
        "keywords": ["sanat", "art", "yaratici", "creative", "tasarim", "design", "fotograf", "photo", "muzik", "music", "galeri", "portfolio"],
        "primary": "#f43f5e",
        "secondary": "#ec4899",
        "accent": "#fb7185",
        "bg_dark": "#1e1b4b",
        "bg_card": "#312e81",
        "bg_gradient": "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%)",
        "hero_gradient": "linear-gradient(135deg, #f43f5e, #ec4899, #a855f7)",
        "text_gradient": "linear-gradient(135deg, #f43f5e, #ec4899)",
    },
    "business": {
        "name": "Business / Professional",
        "keywords": ["is", "business", "kurumsal", "corporate", "profesyonel", "professional", "danismanlik", "consulting", "hukuk", "law", "finans", "finance"],
        "primary": "#3b82f6",
        "secondary": "#2563eb",
        "accent": "#60a5fa",
        "bg_dark": "#0f172a",
        "bg_card": "#1e293b",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0c4a6e 100%)",
        "hero_gradient": "linear-gradient(135deg, #3b82f6, #2563eb, #1d4ed8)",
        "text_gradient": "linear-gradient(135deg, #3b82f6, #06b6d4)",
    },
    "warm": {
        "name": "Warm / Food",
        "keywords": ["yemek", "food", "restoran", "restaurant", "kafe", "cafe", "kahve", "coffee", "pizza", "burger", "pasta", "tatli", "firinci", "bakery"],
        "primary": "#f59e0b",
        "secondary": "#d97706",
        "accent": "#fbbf24",
        "bg_dark": "#1c1917",
        "bg_card": "#292524",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #292524 50%, #451a03 100%)",
        "hero_gradient": "linear-gradient(135deg, #f59e0b, #d97706, #b45309)",
        "text_gradient": "linear-gradient(135deg, #f59e0b, #ef4444)",
    },
    "elegant": {
        "name": "Elegant / Luxury",
        "keywords": ["luks", "luxury", "elegant", "otel", "hotel", "moda", "fashion", "guzellik", "beauty", "dugun", "wedding", "premium"],
        "primary": "#d4af37",
        "secondary": "#b8860b",
        "accent": "#f0d060",
        "bg_dark": "#0a0a0a",
        "bg_card": "#1a1a1a",
        "bg_gradient": "linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2d2d2d 100%)",
        "hero_gradient": "linear-gradient(135deg, #d4af37, #b8860b, #8b6914)",
        "text_gradient": "linear-gradient(135deg, #d4af37, #f0d060)",
    },
    "education": {
        "name": "Education / Learning",
        "keywords": ["egitim", "education", "kurs", "course", "okul", "school", "universite", "ogren", "learn", "akademi", "academy"],
        "primary": "#8b5cf6",
        "secondary": "#7c3aed",
        "accent": "#a78bfa",
        "bg_dark": "#0f172a",
        "bg_card": "#1e293b",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #2e1065 100%)",
        "hero_gradient": "linear-gradient(135deg, #8b5cf6, #7c3aed, #6d28d9)",
        "text_gradient": "linear-gradient(135deg, #8b5cf6, #ec4899)",
    },
}

# ============================================================
# DESIGN DNA - Pre-built CSS component code
# These are COMPLETE, TESTED CSS/HTML patterns that the model
# can drop in directly. No imagination needed!
# ============================================================

DNA_NAVBAR = """
/* ===== NAVBAR DNA ===== */
nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}
nav.scrolled {
    padding: 0.7rem 2rem;
    background: rgba(15, 23, 42, 0.95);
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
}
nav .logo {
    font-size: 1.5rem;
    font-weight: 800;
    background: {text_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
nav .nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
    list-style: none;
}
nav .nav-links a {
    color: #94a3b8;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.3s ease;
    position: relative;
}
nav .nav-links a::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: {primary};
    transition: width 0.3s ease;
    border-radius: 1px;
}
nav .nav-links a:hover { color: #f1f5f9; }
nav .nav-links a:hover::after { width: 100%; }
nav .cta-btn {
    padding: 0.6rem 1.5rem;
    background: {hero_gradient};
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}
nav .cta-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
}
.hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 5px;
}
.hamburger span {
    width: 25px;
    height: 2px;
    background: #e2e8f0;
    border-radius: 2px;
    transition: all 0.3s ease;
}
@media (max-width: 768px) {
    .hamburger { display: flex; }
    nav .nav-links {
        position: fixed;
        top: 0;
        right: -100%;
        width: 70%;
        height: 100vh;
        background: {bg_dark};
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: right 0.3s ease;
        box-shadow: -10px 0 30px rgba(0,0,0,0.5);
    }
    nav .nav-links.active { right: 0; }
    nav .nav-links a { font-size: 1.2rem; }
}
"""

DNA_HERO = """
/* ===== HERO SECTION DNA ===== */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 8rem 2rem 4rem;
    position: relative;
    overflow: hidden;
    background: {bg_gradient};
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba({primary_rgb}, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 70% 80%, rgba({secondary_rgb}, 0.1) 0%, transparent 50%);
    animation: heroShift 15s ease-in-out infinite alternate;
}
@keyframes heroShift {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(-30px, 20px) rotate(3deg); }
}
.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0.4rem 1rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    font-size: 0.8rem;
    color: {accent};
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
    color: #f1f5f9;
}
.hero h1 span {
    background: {text_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: #94a3b8;
    line-height: 1.7;
    max-width: 600px;
    margin: 0 auto 2.5rem;
}
.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}
.btn-primary {
    padding: 0.9rem 2.2rem;
    background: {hero_gradient};
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba({primary_rgb}, 0.4);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba({primary_rgb}, 0.6);
}
.btn-secondary {
    padding: 0.9rem 2.2rem;
    background: transparent;
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    backdrop-filter: blur(10px);
}
.btn-secondary:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.3);
    transform: translateY(-2px);
}
"""

DNA_FEATURES = """
/* ===== FEATURES DNA ===== */
.features {
    padding: 6rem 2rem;
    background: {bg_dark};
    position: relative;
}
.section-header {
    text-align: center;
    max-width: 600px;
    margin: 0 auto 4rem;
}
.section-tag {
    display: inline-block;
    padding: 0.3rem 1rem;
    background: rgba({primary_rgb}, 0.1);
    border: 1px solid rgba({primary_rgb}, 0.2);
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {primary};
    margin-bottom: 1rem;
}
.section-header h2 {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}
.section-header p {
    color: #94a3b8;
    font-size: 1rem;
    line-height: 1.7;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
}
.feature-card {
    padding: 2rem;
    background: {bg_card};
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: {hero_gradient};
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}
.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba({primary_rgb}, 0.2);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 30px rgba({primary_rgb}, 0.05);
}
.feature-card:hover::before {
    transform: scaleX(1);
}
.feature-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba({primary_rgb}, 0.1);
    color: {primary};
    font-size: 1.3rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
}
.feature-card:hover .feature-icon {
    background: {hero_gradient};
    color: white;
    transform: scale(1.1) rotate(5deg);
}
.feature-card h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.7rem;
}
.feature-card p {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.7;
}
"""

DNA_STATS = """
/* ===== STATS/COUNTER DNA ===== */
.stats {
    padding: 4rem 2rem;
    background: linear-gradient(135deg, rgba({primary_rgb}, 0.05), rgba({secondary_rgb}, 0.05));
    border-top: 1px solid rgba(255,255,255,0.03);
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
    text-align: center;
}
.stat-item h3 {
    font-size: 2.5rem;
    font-weight: 900;
    background: {text_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.stat-item p {
    color: #94a3b8;
    font-size: 0.9rem;
    font-weight: 500;
}
"""

DNA_PRICING = """
/* ===== PRICING DNA ===== */
.pricing {
    padding: 6rem 2rem;
    background: {bg_dark};
}
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    max-width: 1000px;
    margin: 0 auto;
}
.price-card {
    padding: 2.5rem 2rem;
    background: {bg_card};
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 20px;
    text-align: center;
    transition: all 0.4s ease;
    position: relative;
}
.price-card.featured {
    border-color: {primary};
    background: linear-gradient(180deg, rgba({primary_rgb}, 0.1) 0%, {bg_card} 100%);
    transform: scale(1.05);
}
.price-card.featured::before {
    content: 'Populer';
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.3rem 1.5rem;
    background: {hero_gradient};
    color: white;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
}
.price-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.price-card.featured:hover {
    transform: scale(1.05) translateY(-5px);
}
.price-card h3 {
    font-size: 1.2rem;
    color: #94a3b8;
    margin-bottom: 1rem;
    font-weight: 600;
}
.price {
    font-size: 3rem;
    font-weight: 900;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}
.price span { font-size: 1rem; font-weight: 400; color: #64748b; }
.price-features {
    list-style: none;
    margin: 2rem 0;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.price-features li {
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
}
.price-features li i { color: {accent}; }
.price-card .btn-primary {
    width: 100%;
    justify-content: center;
}
"""

DNA_TESTIMONIALS = """
/* ===== TESTIMONIALS DNA ===== */
.testimonials {
    padding: 6rem 2rem;
    background: {bg_gradient};
}
.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
}
.testimonial-card {
    padding: 2rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.testimonial-card:hover {
    transform: translateY(-5px);
    border-color: rgba({primary_rgb}, 0.3);
}
.testimonial-stars {
    color: #fbbf24;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}
.testimonial-card blockquote {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    font-style: italic;
}
.testimonial-author {
    display: flex;
    align-items: center;
    gap: 12px;
}
.testimonial-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: {hero_gradient};
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1rem;
}
.testimonial-info h4 { color: #f1f5f9; font-size: 0.9rem; font-weight: 600; }
.testimonial-info p { color: #64748b; font-size: 0.8rem; }
"""

DNA_CONTACT = """
/* ===== CONTACT FORM DNA ===== */
.contact {
    padding: 6rem 2rem;
    background: {bg_dark};
}
.contact-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    max-width: 1100px;
    margin: 0 auto;
}
@media (max-width: 768px) {
    .contact-wrapper { grid-template-columns: 1fr; }
}
.contact-info h2 {
    font-size: 2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 1rem;
}
.contact-info p {
    color: #94a3b8;
    line-height: 1.7;
    margin-bottom: 2rem;
}
.contact-details {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}
.contact-item {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #cbd5e1;
}
.contact-item i {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba({primary_rgb}, 0.1);
    color: {primary};
}
.contact-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.form-group { display: flex; flex-direction: column; gap: 0.3rem; }
.form-group label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
}
.form-group input,
.form-group textarea {
    padding: 0.8rem 1rem;
    background: {bg_card};
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #f1f5f9;
    font-family: inherit;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    outline: none;
}
.form-group input:focus,
.form-group textarea:focus {
    border-color: {primary};
    box-shadow: 0 0 0 3px rgba({primary_rgb}, 0.1);
}
.form-group textarea { resize: vertical; min-height: 120px; }
"""

DNA_FOOTER = """
/* ===== FOOTER DNA ===== */
footer {
    padding: 4rem 2rem 2rem;
    background: {bg_card};
    border-top: 1px solid rgba(255,255,255,0.05);
}
.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}
@media (max-width: 768px) {
    .footer-grid { grid-template-columns: 1fr 1fr; }
}
.footer-brand .logo {
    font-size: 1.3rem;
    font-weight: 800;
    background: {text_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
    display: inline-block;
}
.footer-brand p {
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.7;
    margin-bottom: 1.2rem;
}
.footer-social {
    display: flex;
    gap: 10px;
}
.footer-social a {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    color: #94a3b8;
    transition: all 0.3s ease;
    text-decoration: none;
}
.footer-social a:hover {
    background: {primary};
    color: white;
    transform: translateY(-3px);
}
.footer-col h4 {
    color: #f1f5f9;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-weight: 700;
}
.footer-col a {
    display: block;
    color: #64748b;
    text-decoration: none;
    font-size: 0.85rem;
    padding: 0.3rem 0;
    transition: color 0.3s ease;
}
.footer-col a:hover { color: {accent}; }
.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    color: #475569;
    font-size: 0.8rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}
"""

DNA_BASE = """
/* ===== BASE DNA ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: {bg_dark};
    color: #e2e8f0;
    overflow-x: hidden;
    line-height: 1.6;
}
a { color: inherit; text-decoration: none; }
img { max-width: 100%; height: auto; border-radius: 12px; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
section { position: relative; padding: 6rem 0; }

/* Core Component Resets for Weaker Models */
h1, h2, h3, h4 { color: #f1f5f9; margin-bottom: 1rem; line-height: 1.2; }
p { margin-bottom: 1.5rem; color: #94a3b8; }
button, .btn { 
    display: inline-flex; 
    align-items: center; 
    gap: 8px; 
    padding: 0.8rem 1.8rem; 
    border-radius: 50px; 
    font-weight: 600; 
    cursor: pointer; 
    transition: all 0.3s ease;
    border: none;
}
input, textarea {
    width: 100%;
    padding: 0.8rem 1rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: white;
    margin-bottom: 1rem;
}

/* Smooth section transitions */
section + section { border-top: 1px solid rgba(255,255,255,0.03); }

/* Utility animations */
[data-aos] { transition-property: transform, opacity; }
"""


def hex_to_rgb(hex_color):
    """Convert hex color to comma-separated RGB string"""
    hex_color = hex_color.lstrip('#')
    return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}"


def detect_category(prompt):
    """Detect website category from user prompt"""
    prompt_lower = prompt.lower()
    
    # Remove Turkish characters for matching
    replacements = {'ı': 'i', 'ö': 'o', 'ü': 'u', 'ş': 's', 'ç': 'c', 'ğ': 'g'}
    for old, new in replacements.items():
        prompt_lower = prompt_lower.replace(old, new)
    
    best_match = "tech"  # default
    best_score = 0
    
    for key, palette in COLOR_PALETTES.items():
        score = 0
        for keyword in palette["keywords"]:
            keyword_normalized = keyword
            for old, new in replacements.items():
                keyword_normalized = keyword_normalized.replace(old, new)
            if keyword_normalized in prompt_lower:
                score += 1
        if score > best_score:
            best_score = score
            best_match = key
    
    return best_match


def build_design_dna(prompt):
    """
    Build complete Design DNA for the given prompt.
    Returns ready-to-use CSS code and palette info that gets injected
    into the system prompt, so the model doesn't need to imagine anything.
    """
    category = detect_category(prompt)
    palette = COLOR_PALETTES[category]
    
    # Compute RGB values
    primary_rgb = hex_to_rgb(palette["primary"])
    secondary_rgb = hex_to_rgb(palette["secondary"])
    
    # Build replacement dict
    replacements = {
        "{primary}": palette["primary"],
        "{secondary}": palette["secondary"],
        "{accent}": palette["accent"],
        "{bg_dark}": palette["bg_dark"],
        "{bg_card}": palette["bg_card"],
        "{bg_gradient}": palette["bg_gradient"],
        "{hero_gradient}": palette["hero_gradient"],
        "{text_gradient}": palette["text_gradient"],
        "{primary_rgb}": primary_rgb,
        "{secondary_rgb}": secondary_rgb,
    }
    
    # Assemble all DNA components
    components = [
        DNA_BASE,
        DNA_NAVBAR,
        DNA_HERO,
        DNA_FEATURES,
        DNA_STATS,
        DNA_PRICING,
        DNA_TESTIMONIALS,
        DNA_CONTACT,
        DNA_FOOTER,
    ]
    
    full_css = ""
    for component in components:
        css = component
        for key, value in replacements.items():
            css = css.replace(key, value)
        full_css += css + "\n"
    
    return {
        "category": category,
        "palette": palette,
        "css": full_css,
        "primary_rgb": primary_rgb,
        "secondary_rgb": secondary_rgb,
    }
