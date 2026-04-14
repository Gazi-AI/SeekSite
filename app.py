"""
SeekSite - AI Website Builder
Powered by Pollinations AI (OpenAI/gpt-oss-20b)
Uses Design DNA injection to make even weak LLMs produce stunning websites.
"""

from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import re
from config import OLLAMA_API_URL, OLLAMA_MODELS_URL, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE, STREAM_TIMEOUT, HOST, PORT, DEBUG
from prompt_enhancer import enhance_prompt, get_enhancement_prompt
from postprocessor import clean_generated_code, validate_html, auto_fix_html, full_fix, strip_pollinations_ads
from design_engine import build_design_dna, COLOR_PALETTES

app = Flask(__name__, static_folder='static', template_folder='templates')


def single_stream_request(messages, model=None):
    """Make a single streaming request to Ollama API and yield chunks + return accumulated text"""
    target_model = model or DEFAULT_MODEL
    payload = {
        "model": target_model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": 4096 # Limit to match Ollama's typical defaults or user needs
        }
    }
    
    accumulated = ""
    
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=STREAM_TIMEOUT
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                try:
                    data = json.loads(line_str)
                    if 'message' in data:
                        content = data['message'].get('content', '')
                        if content:
                            accumulated += content
                            yield ('chunk', content)
                    
                    if data.get('done'):
                        break
                except json.JSONDecodeError:
                    continue
    except requests.exceptions.RequestException as e:
        yield ('error', str(e))
    
    yield ('done', accumulated)


def stream_from_ollama(messages, dna_css=None, model=None):
    """Stream response from Ollama with auto-continuation if code is cut off."""
    MAX_CONTINUATIONS = 5
    full_accumulated = ""
    current_messages = list(messages)
    
    # Send DNA CSS down the stream ONCE before anything else
    if dna_css:
        yield f'data: {json.dumps({"dnaCss": dna_css})}\n\n'
        
    for attempt in range(MAX_CONTINUATIONS + 1):
        chunk_accumulated = ""
        is_first_chunk = True
        buffer = ""
        
        for event_type, data in single_stream_request(current_messages, model=model):
            if event_type == 'chunk':
                if attempt > 0 and is_first_chunk:
                    # Chat Filter: Strip apologies/explanations from continuation responses
                    buffer += data
                    # If we have enough data to check for common chat patterns
                    if len(buffer) > 100 or '\n' in buffer or '<' in buffer:
                        # Common chat starters to remove
                        chat_patterns = [
                            r'^I\'m sorry.*?\.', 
                            r'^Sure.*?\!', 
                            r'^\*\*.*?\*\*',
                            r'^Here is the.*?\:',
                            r'^I need the exact snippet.*?\?',
                            r'^Could you please provide.*?\?',
                            r'^Please find the.*?\:',
                            r'^Continuing from where.*?\:',
                        ]
                        cleaned_buffer = buffer
                        for p in chat_patterns:
                            cleaned_buffer = re.sub(p, '', cleaned_buffer, flags=re.IGNORECASE | re.DOTALL).strip()
                        
                        # Only yield if it's not looking like a chat apology
                        if cleaned_buffer:
                            full_accumulated += cleaned_buffer
                            chunk_accumulated += cleaned_buffer
                            yield f'data: {json.dumps({"content": cleaned_buffer})}\n\n'
                        is_first_chunk = False
                        buffer = ""
                else:
                    full_accumulated += data
                    chunk_accumulated += data
                    yield f'data: {json.dumps({"content": data})}\n\n'
            elif event_type == 'error':
                yield f'data: {json.dumps({"error": data})}\n\n'
                yield 'data: [DONE]\n\n'
                return
        
        # Strip Pollinations ads (renamed to local cleanup if needed, but keeping for now)
        cleaned = strip_pollinations_ads(full_accumulated)
        if cleaned != full_accumulated:
            full_accumulated = cleaned
        
        # Check if code is complete
        stripped = full_accumulated.strip()
        if '</html>' in stripped.lower() or (attempt >= MAX_CONTINUATIONS):
            break
        
        # Context extraction: find where it cut off
        tail = full_accumulated[-200:] # Just a small tail to remind it
        
        # Proper continuation format: append the FULL partial assistant message, then the continue prompt
        current_messages.append({"role": "assistant", "content": full_accumulated})
        current_messages.append({
            "role": "user", 
            "content": f"Your code generation was cut off exactly here:\n{tail}\n\nPlease CONTINUE the code starting from the very next character. DO NOT repeat the beginning. DO NOT explain yourself. ONLY write the remaining HTML code."
        })
    
    # Final ad strip and send clean version
    final_clean = strip_pollinations_ads(full_accumulated)
    if final_clean != full_accumulated:
        # Send replacement to frontend
        yield f'data: {json.dumps({"replace": final_clean})}\n\n'
    
    yield 'data: [DONE]\n\n'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """Fetch installed Ollama models"""
    try:
        response = requests.get(OLLAMA_MODELS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        models = [m['name'] for m in data.get('models', [])]
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e), "models": [DEFAULT_MODEL]}), 200 # Fallback to default if Ollama is unreachable


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate or modify a website via streaming"""
    data = request.json
    user_prompt = data.get('prompt', '')
    existing_code = data.get('existing_code', None)
    conversation_history = data.get('history', None)
    model = data.get('model', DEFAULT_MODEL)
    
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    messages = enhance_prompt(user_prompt, existing_code, conversation_history)
    dna = build_design_dna(user_prompt)
    
    return Response(
        stream_from_ollama(messages, dna_css=dna['css'], model=model),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

@app.route('/api/enhance', methods=['POST'])
def enhance():
    """Enhance existing website with specific improvements"""
    data = request.json
    code = data.get('code', '')
    enhancement_type = data.get('type', '')
    prompt = data.get('prompt', '') # Need prompt for DNA
    model = data.get('model', DEFAULT_MODEL)
    
    if not code:
        return jsonify({"error": "Code is required"}), 400
    
    enhancement_prompt = get_enhancement_prompt(enhancement_type)
    messages = enhance_prompt(enhancement_prompt, existing_code=code)
    dna = build_design_dna(prompt) if prompt else build_design_dna(enhancement_type)
    
    return Response(
        stream_from_ollama(messages, dna_css=dna['css'], model=model),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )


@app.route('/api/validate', methods=['POST'])
def validate():
    """Validate generated HTML code"""
    data = request.json
    code = data.get('code', '')
    
    result = validate_html(code)
    return jsonify(result)


@app.route('/api/fix', methods=['POST'])
def fix():
    """Auto-fix common HTML issues using prompt as DNA context"""
    data = request.json
    code = data.get('code', '')
    prompt = data.get('prompt', '')
    
    fixed_code, validation = full_fix(code, prompt)
    
    return jsonify({
        "code": fixed_code,
        "validation": validation
    })


@app.route('/api/design-info', methods=['POST'])
def design_info():
    """Get design DNA info for a prompt (useful for frontend)"""
    data = request.json
    prompt = data.get('prompt', '')
    
    dna = build_design_dna(prompt)
    return jsonify({
        "category": dna["category"],
        "palette_name": dna["palette"]["name"],
        "colors": {
            "primary": dna["palette"]["primary"],
            "secondary": dna["palette"]["secondary"],
            "accent": dna["palette"]["accent"],
        }
    })


@app.route('/api/generate_title', methods=['POST'])
def generate_title():
    """Generate a short chat title via AI"""
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"title": "Yeni Proje"})
    
    try:
        model = data.get('model', DEFAULT_MODEL)
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Sen bir baslik olusturucusun. Kullanicinin mesajina gore 2-4 kelimelik kisa ve aciklayici bir Turkce baslik olustur. Sadece basligi yaz, baska hicbir sey ekleme."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 30
            }
        }
        
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        
        result = response.json()
        title = result.get('message', {}).get('content', '').strip()
        # Clean up title
        title = title.strip('"\'').strip()
        if len(title) > 40:
            title = title[:40] + '...'
        if not title:
            title = prompt[:30] + ('...' if len(prompt) > 30 else '')
        
        return jsonify({"title": title})
    except Exception as e:
        # Fallback: use prompt snippet
        title = prompt[:30] + ('...' if len(prompt) > 30 else '')
        return jsonify({"title": title})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  [*] SeekSite - Local AI Website Builder")
    print("  Powered by Ollama + Design DNA")
    print("="*50)
    print(f"\n  >> http://localhost:{PORT}\n")
    app.run(debug=DEBUG, host=HOST, port=PORT)
