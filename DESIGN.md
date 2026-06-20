---
name: Vibrant Analytics
colors:
  surface: '#131318'
  surface-dim: '#131318'
  surface-bright: '#39383e'
  surface-container-lowest: '#0e0e13'
  surface-container-low: '#1b1b20'
  surface-container: '#1f1f25'
  surface-container-high: '#2a292f'
  surface-container-highest: '#35343a'
  on-surface: '#e4e1e9'
  on-surface-variant: '#cfc2d6'
  inverse-surface: '#e4e1e9'
  inverse-on-surface: '#303036'
  outline: '#988d9f'
  outline-variant: '#4d4354'
  surface-tint: '#ddb7ff'
  primary: '#ddb7ff'
  on-primary: '#490080'
  primary-container: '#b76dff'
  on-primary-container: '#400071'
  inverse-primary: '#842bd2'
  secondary: '#5de6ff'
  on-secondary: '#00363e'
  secondary-container: '#00cbe6'
  on-secondary-container: '#00515d'
  tertiary: '#ffb0cd'
  on-tertiary: '#640039'
  tertiary-container: '#f751a1'
  on-tertiary-container: '#570032'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#f0dbff'
  primary-fixed-dim: '#ddb7ff'
  on-primary-fixed: '#2c0051'
  on-primary-fixed-variant: '#6900b3'
  secondary-fixed: '#a2eeff'
  secondary-fixed-dim: '#2fd9f4'
  on-secondary-fixed: '#001f25'
  on-secondary-fixed-variant: '#004e5a'
  tertiary-fixed: '#ffd9e4'
  tertiary-fixed-dim: '#ffb0cd'
  on-tertiary-fixed: '#3e0022'
  on-tertiary-fixed-variant: '#8c0053'
  background: '#131318'
  on-background: '#e4e1e9'
  surface-variant: '#35343a'
  surface-elevated: '#16161e'
  border-subtle: rgba(255, 255, 255, 0.1)
  glass-fill: rgba(255, 255, 255, 0.03)
typography:
  display-lg:
    fontFamily: Quicksand
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Quicksand
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Quicksand
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-base:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  stat-lg:
    fontFamily: JetBrains Mono
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.05em
  stat-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-caps:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.1em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  container-max: 1440px
---

## Brand & Style

This design system establishes a "Neon-Dark" aesthetic designed to transform technical data into a captivating visual narrative. It targets developers and engineering leaders who value high-performance tools that don't sacrifice personality. 

The style sits at the intersection of **Glassmorphism** and **High-Contrast Bold**. It utilizes a deep, obsidian-like base to allow vibrant, neon accents to "pop" with maximum intensity. The emotional response should be one of discovery and energy—reminiscent of a "Spotify Wrapped" experience applied to GitHub metadata. Elements should feel fluid, luminous, and premium, avoiding the dry, utilitarian feel of traditional enterprise dashboards.

## Colors

The palette is anchored by a deep charcoal-black (#0a0a0f) to provide infinite depth. 

- **Primary (Purple):** Used for primary actions, branding, and core navigation.
- **Secondary (Cyan):** Dedicated to data visualization, activity charts, and growth metrics.
- **Tertiary (Pink):** Reserved for highlights, notifications, and critical calls to attention.
- **Surface Strategy:** Layers are built using slight variations in lightness or glass-like transparency rather than flat greys. Use gradients that transition from the primary/secondary colors to transparent for "glow" effects.

## Typography

Typography creates a hierarchy of "Playful Professionalism." 

1. **Headlines:** Use **Quicksand** for its rounded, approachable terminals. This softens the technical nature of the product.
2. **Body:** **Be Vietnam Pro** provides high legibility and a contemporary feel for descriptions and UI labels.
3. **Data/Stats:** **JetBrains Mono** is used for all numerical data, code snippets, and commit hashes. This signals technical precision and ensures numbers align perfectly in tabular layouts.

Avoid thin weights on dark backgrounds; maintain a minimum of 400 weight for body text to ensure accessibility.

## Layout & Spacing

The layout follows a **fluid grid** model with generous white space (or "dark space") to prevent the vibrant colors from feeling cluttered.

- **Grid:** 12-column system for desktop, 4-column for mobile.
- **Rhythm:** An 8px linear scale governs all padding and margins. 
- **Margins:** Desktop views should feel expansive with 48px outer margins.
- **Reflow:** On mobile, complex data cards stack vertically. Charts should maintain an aspect ratio to ensure readability on small screens.

## Elevation & Depth

This design system uses **Glassmorphism** and **Tonal Layers** instead of traditional shadows.

1. **Base:** The background is #0a0a0f.
2. **Middling (Cards):** Surfaces use a semi-transparent fill (glass-fill) with a `backdrop-filter: blur(12px)`. 
3. **Borders:** Instead of heavy shadows, use a 1px solid border with 10% white opacity. On hover, this border should transition to a gradient of the Primary or Secondary color.
4. **Luminosity:** Use soft, blurred radial gradients (blobs) in the background (z-index: -1) to create the "neon glow" behind cards and key metrics.

## Shapes

The shape language is extremely soft and organic.

- **Cards:** Use `rounded-2xl` (1.5rem) or `rounded-3xl` (3rem) for dashboard modules.
- **Interactive Elements:** Buttons and Input fields are strictly **pill-shaped** (full radius). This provides a friendly, tactile contrast to the dense data being displayed.
- **Avatars:** Always circular.

## Components

- **Buttons:** Primary buttons use a solid Purple (#a855f7) fill with white text. Secondary buttons are outlined with a Cyan border and use a "glass" background.
- **Inputs:** Pill-shaped with a dark, semi-transparent fill. On focus, the border glows with the Secondary Cyan color.
- **Cards:** Large radius (2xl). On hover, apply a subtle external glow (box-shadow: 0 0 20px rgba(168, 85, 247, 0.15)) and scale the card slightly (1.02x).
- **Chips:** Small, pill-shaped tags used for GitHub labels or language stats. Use low-opacity versions of the accent colors (e.g., 15% opacity Pink fill with 100% opacity Pink text).
- **Activity Graphs:** Line charts should use vibrant gradients (Cyan to Transparent) with a "glow" effect on the stroke. Area charts should use a very soft gradient fill under the line.
- **Lists:** Clean rows with 1px subtle dividers. Hovering over a list item should highlight the entire row with a `glass-fill`.