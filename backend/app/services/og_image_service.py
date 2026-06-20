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
      @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&amp;family=JetBrains+Mono:wght@700&amp;family=Quicksand:wght@700&amp;display=swap');
      .title {{ font-family: 'Quicksand', sans-serif; font-weight: 700; fill: #ffffff; }}
      .text {{ font-family: 'Be Vietnam Pro', sans-serif; fill: #e4e1e9; }}
      .mono {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}
    </style>
    
    <linearGradient id="neon-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ddb7ff" />
      <stop offset="100%" stop-color="#5de6ff" />
    </linearGradient>
    <linearGradient id="primary-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ddb7ff" />
      <stop offset="100%" stop-color="#b76dff" />
    </linearGradient>
    
    <clipPath id="avatar-clip">
      <circle cx="200" cy="220" r="90" />
    </clipPath>
  </defs>

  <!-- Obsidian Base Background -->
  <rect width="100%" height="100%" fill="#131318" />
  
  <!-- Neon Glow Blobs -->
  <circle cx="200" cy="220" r="300" fill="#b76dff" opacity="0.07" filter="blur(60px)" />
  <circle cx="1000" cy="315" r="250" fill="#00cbe6" opacity="0.07" filter="blur(55px)" />
  
  <!-- Border outline glow -->
  <rect x="25" y="25" width="1150" height="580" rx="24" fill="transparent" stroke="url(#neon-grad)" stroke-width="2" opacity="0.2" />

  <!-- Avatar Rendering with circular crop -->
  <circle cx="200" cy="220" r="95" fill="transparent" stroke="url(#primary-grad)" stroke-width="4" />
  <image href="{avatar_url}" x="110" y="130" width="180" height="180" clip-path="url(#avatar-clip)" />

  <!-- Profile Identity details -->
  <text x="330" y="190" class="title" font-size="48" fill="#ffffff">{display_name}</text>
  <text x="330" y="235" class="mono" font-size="28" fill="#5de6ff">@{username}</text>
  <text x="330" y="280" class="text" font-size="20" fill="#cfc2d6" opacity="0.6">Joined GitHub in {joined_year}</text>

  <!-- Biography section (neatly split) -->
  <text x="110" y="380" class="text" font-size="20" fill="#cfc2d6" font-style="italic">{bio_line1}</text>
  <text x="110" y="415" class="text" font-size="20" fill="#cfc2d6" font-style="italic">{bio_line2}</text>

  <!-- Stats Sidebar Grid -->
  <!-- Stars -->
  <g transform="translate(680, 100)">
    <rect width="410" height="120" rx="16" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.06)" stroke-width="1" />
    <text x="30" y="45" class="text" font-size="16" fill="#cfc2d6" letter-spacing="2" opacity="0.6">TOTAL STARS</text>
    <text x="30" y="95" class="mono" font-size="40" fill="#ddb7ff">⭐ {total_stars}</text>
  </g>

  <!-- Top Language -->
  <g transform="translate(680, 245)">
    <rect width="410" height="120" rx="16" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.06)" stroke-width="1" />
    <text x="30" y="45" class="text" font-size="16" fill="#cfc2d6" letter-spacing="2" opacity="0.6">TOP LANGUAGE</text>
    <text x="30" y="95" class="title" font-size="36" fill="#5de6ff">{top_language}</text>
  </g>

  <!-- Persona Heuristics -->
  <g transform="translate(680, 390)">
    <rect width="410" height="120" rx="16" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.06)" stroke-width="1" />
    <text x="30" y="45" class="text" font-size="16" fill="#cfc2d6" letter-spacing="2" opacity="0.6">CODING PERSONA</text>
    <text x="30" y="95" class="title" font-size="30" fill="#ffb0cd">{personality}</text>
  </g>

  <!-- Footer Branding -->
  <text x="110" y="550" class="title" font-size="28" fill="#ffffff">🛰️ Orbit</text>
  <text x="200" y="550" class="text" font-size="20" fill="#cfc2d6" opacity="0.4">/ {username}</text>
  
  <text x="1090" y="550" class="mono" font-size="18" fill="#5de6ff" text-anchor="end">orbit.dev</text>
</svg>"""
    return svg_template
