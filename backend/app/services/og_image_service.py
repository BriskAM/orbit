from datetime import datetime

def xml_escape(text):
    """
    Escapes special XML characters to prevent parsing failures in SVG rendering.
    """
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

def get_bio_lines(bio):
    """
    Wraps user bio strings into two lines of up to 45 characters each.
    """
    if not bio:
        return "", ""
    words = bio.split()
    line1 = []
    line2 = []
    
    for w in words:
        # Check line 1 length limit
        if len(" ".join(line1)) + len(w) + 1 < 45 and not line2:
            line1.append(w)
        # Check line 2 length limit
        elif len(" ".join(line2)) + len(w) + 1 < 45:
            line2.append(w)
        else:
            break
            
    return " ".join(line1), " ".join(line2)

def generate_og_image_svg(profile_data):
    """
    Generates a stylized OpenGraph share card in SVG format.
    Accepts the CachedProfile dict payload.
    """
    profile = profile_data.get('profile', {})
    metrics = profile_data.get('metrics', {})
    
    username = xml_escape(profile.get('username', ''))
    display_name = xml_escape(profile.get('display_name') or username)
    avatar_url = xml_escape(profile.get('avatar_url', ''))
    
    # Format Joined Date
    joined_date_str = profile.get('account_created_at', '')
    joined_year = 'N/A'
    if joined_date_str:
        try:
            # Parse '2011-01-25T18:44:36' or similar
            dt = datetime.fromisoformat(joined_date_str.split('+')[0])
            joined_year = dt.strftime('%B %Y')
        except Exception:
            pass
            
    # Wrap bio
    bio_line1, bio_line2 = get_bio_lines(profile.get('bio', ''))
    bio_line1 = xml_escape(bio_line1)
    bio_line2 = xml_escape(bio_line2)
    
    total_stars = profile.get('total_stars_earned', 0)
    top_language = xml_escape(profile.get('top_language') or 'None')
    personality = xml_escape(metrics.get('personality_tag') or 'Pragmatic Developer')
    
    # Return raw SVG code
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@600;700&amp;display=swap');
      .title {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-weight: 600; fill: #f0f6fc; }}
      .text {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; fill: #c9d1d9; }}
      .desc {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; fill: #8d96a0; }}
      .mono {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}
    </style>
    
    <clipPath id="avatar-clip">
      <circle cx="200" cy="220" r="90" />
    </clipPath>
  </defs>

  <!-- GitHub Dark Background -->
  <rect width="100%" height="100%" fill="#0d1117" />
  
  <!-- Outer Border -->
  <rect x="25" y="25" width="1150" height="580" rx="12" fill="transparent" stroke="#30363d" stroke-width="2" />

  <!-- Avatar Rendering with circular crop -->
  <circle cx="200" cy="220" r="92" fill="transparent" stroke="#30363d" stroke-width="3" />
  <image href="{avatar_url}" x="110" y="130" width="180" height="180" clip-path="url(#avatar-clip)" />

  <!-- Profile Identity details -->
  <text x="330" y="190" class="title" font-size="44">{display_name}</text>
  <text x="330" y="235" class="mono" font-size="28" fill="#58a6ff">@{username}</text>
  <text x="330" y="280" class="desc" font-size="20">Joined GitHub in {joined_year}</text>

  <!-- Biography section -->
  <text x="110" y="380" class="text" font-size="20" font-style="italic">{bio_line1}</text>
  <text x="110" y="415" class="text" font-size="20" font-style="italic">{bio_line2}</text>

  <!-- Stats Sidebar Grid -->
  <!-- Stars -->
  <g transform="translate(680, 100)">
    <rect width="410" height="120" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1" />
    <g transform="translate(30, 45)">
      <svg height="30" viewBox="0 0 16 16" version="1.1" width="30" fill="#e3b341">
        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97 1.9 4.167a.75.75 0 0 1-1.087.79L8 11.777l-3.766 1.98a.75.75 0 0 1-1.087-.79l1.9-4.167L1.001 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"></path>
      </svg>
    </g>
    <text x="80" y="45" class="desc" font-size="14" font-weight="600" letter-spacing="1">TOTAL STARS</text>
    <text x="80" y="85" class="mono" font-size="36" fill="#f0f6fc">{total_stars}</text>
  </g>

  <!-- Top Language -->
  <g transform="translate(680, 245)">
    <rect width="410" height="120" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1" />
    <g transform="translate(30, 45)">
      <svg height="30" viewBox="0 0 16 16" version="1.1" width="30" fill="#58a6ff">
        <path d="M10.22 1.72a.75.75 0 0 1 .116.086l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L13.94 6l-3.72-3.72a.75.75 0 0 1-.086-.116Zm-4.44 0a.75.75 0 0 1 0 1.06L2.06 6l3.72 3.72a.75.75 0 1 1-1.06 1.06L.47 6.53a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z"></path>
      </svg>
    </g>
    <text x="80" y="45" class="desc" font-size="14" font-weight="600" letter-spacing="1">TOP LANGUAGE</text>
    <text x="80" y="85" class="title" font-size="32" fill="#f0f6fc">{top_language}</text>
  </g>

  <!-- Persona Heuristics -->
  <g transform="translate(680, 390)">
    <rect width="410" height="120" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1" />
    <g transform="translate(30, 45)">
      <svg height="30" viewBox="0 0 16 16" version="1.1" width="30" fill="#2ea44f">
        <path d="M0 2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM3.22 4.22a.75.75 0 0 1 1.06 0l2.5 2.5a.75.75 0 0 1 0 1.06l-2.5 2.5a.75.75 0 1 1-1.06-1.06L5.19 7 3.22 5.03a.75.75 0 0 1 0-1.06Zm4.53 4.28h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1 0-1.5Z"></path>
      </svg>
    </g>
    <text x="80" y="45" class="desc" font-size="14" font-weight="600" letter-spacing="1">CODING PERSONA</text>
    <text x="80" y="85" class="title" font-size="28" fill="#f0f6fc">{personality}</text>
  </g>

  <!-- Footer Branding -->
  <g transform="translate(110, 525)">
    <svg height="32" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="32" fill="#8d96a0" style="display: inline-block;">
      <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.35 3.12.87 0 .68.01 1.3.01 1.49 0 .21-.15.47-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
    </svg>
  </g>
  <text x="152" y="550" class="title" font-size="28" fill="#f0f6fc">Orbit</text>
  <text x="238" y="550" class="desc" font-size="20">/ {username}</text>
  
  <text x="1090" y="550" class="mono" font-size="18" fill="#58a6ff" text-anchor="end">orbit.dev</text>
</svg>"""
    return svg_template
