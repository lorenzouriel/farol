---
name: ig-reel-producer
description: >
  Produces a complete Instagram Reel in 3 phases: structured script with cut timing,
  FFmpeg commands for video assembly, and a Remotion animated overlay with intro card,
  key-point cards, and CTA — all in the company's visual identity.
  Activate when the user asks to create a Reel, short video, or vertical video content.
---

# Reel Producer

> Produces Reels in 3 phases: script → FFmpeg → Remotion.
> Read the BRAND BLOCK below before starting. If any `[FILL IN]` markers remain, stop and ask the user to complete the BRAND BLOCK first.

---

## BRAND BLOCK (customize once — source of truth for all reels)

> Replace every `[FILL IN ...]` placeholder with your company's details.
> Once filled in, never change per-reel — only update when the brand identity changes.

### Identity

**Company name:**
`[FILL IN — e.g. Acme Corp]`

**Tagline / category line (shown in intro animation):**
`[FILL IN — e.g. FINANCIAL CONSULTING | INNOVATION]`

**Logo path:**
`[FILL IN — absolute path to logo file, e.g. /Users/you/company/resources/identity/assets/logo.png]`

### Colors (hex)

**Primary (dark background):**
`[FILL IN — e.g. #1C3E5A]`

**Secondary / accent (highlight color):**
`[FILL IN — e.g. #C2CDFF]`

**Mid tone (gradient stop or card background):**
`[FILL IN — e.g. #201F7D]`

**Gradient direction and stops:**
`[FILL IN — e.g. linear-gradient(90deg, #0B0B2D 0%, #201F7D 55%, #2B29A6 100%)]`

**Text on dark background:**
`[FILL IN — e.g. #FFFFFF]`

### Typography

**Display font (headline, tagline, CTA):**
`[FILL IN — e.g. Georgia, serif]`

**Body font (card text, captions):**
`[FILL IN — e.g. Arial, Helvetica, sans-serif]`

### Voice & Tone

**How this brand speaks:**
`[FILL IN — e.g. Empathetic, technical, calm authority. Explains complex topics so a non-expert understands without feeling talked down to.]`

**Vocabulary level:**
`[FILL IN — e.g. Professional but accessible. Use domain-specific terms and immediately clarify them.]`

**What this brand never says or promises:**
`[FILL IN — e.g. Never guarantee outcomes. Never use urgency tactics or aggressive imperatives.]`

### CTA

**Default CTA text:**
`[FILL IN — e.g. Talk to us | Link in bio]`

**CTA destination:**
`[FILL IN — e.g. WhatsApp link, website, link in bio]`

### Output

**Output directory:**
`[FILL IN — absolute path, e.g. /Users/you/company/areas/marketing/reels/]`

---

## Phase 0 — Briefing

Ask the user (one question at a time if any is missing):

1. **Topic** — what subject will the reel cover?
2. **Audience** — who is the target viewer?
3. **Target duration** — 30s, 45s, or 60s?
4. **Available footage** — any recorded clips? If yes, how many and what duration each?
5. **Music** — is there an audio file? If not, suggest a neutral instrumental track.

If the user already provided the topic, skip directly to Phase 1.

---

## Phase 1 — Script + Cut Structure

Generate the script in this format:

```
REEL: [Topic]
Duration: [X]s | Audience: [audience] | Format: 9:16 vertical

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK (0s–3s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Opening line — generate curiosity or immediate tension]
Scene: [what appears on screen]
Remotion visual: ANIMATED INTRO (see Phase 3)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POINT 1 — [title] ([Xs]–[Xs])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line: "[spoken text]"
Scene: [clip N, cut at Xs]
Remotion visual: ANIMATED CARD — "[card text]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POINT 2 — [title] ([Xs]–[Xs])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line: "[spoken text]"
Scene: [clip N, cut at Xs]
Remotion visual: ANIMATED CARD — "[card text]"

[repeat for each point — max 4 points for 60s]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CTA ([Xs]–end)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line: "[CTA spoken — direct, no pressure]"
Remotion visual: CTA CARD — "[BRAND default CTA text]"
```

### Script rules (apply BRAND BLOCK voice)
- Hook: opens with a question, a consequence, or a surprising fact about the topic
- Points: match the BRAND vocabulary level — expert understands, non-expert follows
- Honor BRAND "what this brand never says"
- CTA always soft — directs to the BRAND CTA destination without aggressive imperative

---

## Phase 2 — FFmpeg Commands

Generate commands to assemble the video from available clips.

### Output spec
```bash
# Resolution: 1080x1920 (9:16 vertical)
# FPS: 30
# Codec: H.264 (libx264), AAC audio
# Video bitrate: 8M | Audio: 192k
```

### Command template

```bash
# 1. Trim clips (one per script point)
ffmpeg -i clip1.mp4 -ss [start] -t [duration] -c copy point1.mp4
ffmpeg -i clip2.mp4 -ss [start] -t [duration] -c copy point2.mp4
# ... repeat for each clip

# 2. Resize to 9:16 with centered crop
ffmpeg -i point1.mp4 -vf "scale=1920:1080,transpose=1,crop=1080:1920" point1_vertical.mp4
# OR if already vertical:
ffmpeg -i point1.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" point1_vertical.mp4

# 3. Create concat list
echo "file 'point1_vertical.mp4'
file 'point2_vertical.mp4'
file 'point3_vertical.mp4'" > list.txt

# 4. Concatenate
ffmpeg -f concat -safe 0 -i list.txt -c copy raw_concat.mp4

# 5. Add background music (ducking: music at 15% under speech)
ffmpeg -i raw_concat.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k \
  video_with_music.mp4

# 6. Overlay Remotion composition on video (after Phase 3 render)
ffmpeg -i video_with_music.mp4 -i remotion_overlay.mp4 \
  -filter_complex "[0:v][1:v]overlay=0:0[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset fast -crf 18 -c:a copy \
  reel_final.mp4

# 7. Final export optimized for Instagram
ffmpeg -i reel_final.mp4 \
  -c:v libx264 -preset slow -crf 18 -b:v 8M \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  -vf "scale=1080:1920" \
  [BRAND output_directory]/Reel_[Topic]_[DDMMYYYY].mp4
```

### FFmpeg notes
- If no footage available: skip steps 1–6 and use only the Remotion composition as the full video
- To add subtitles: `ffmpeg -vf subtitles=caption.srt`
- `.srt` caption file can be generated in Phase 3

---

## Phase 3 — Remotion Composition

Generate a complete Remotion project ready for `npx remotion render`.

### Project setup
```bash
npx create-video@latest reel-[topic]
cd reel-[topic]
npm install
```

### File structure
```
reel-[topic]/
├── src/
│   ├── Root.tsx
│   ├── Reel.tsx
│   ├── components/
│   │   ├── Intro.tsx
│   │   ├── PointCard.tsx
│   │   ├── CTACard.tsx
│   │   └── Caption.tsx
│   └── tokens.ts
└── public/
    └── logo.png   ← copy from BRAND logo path
```

### `src/tokens.ts`
Populate with BRAND BLOCK values:
```typescript
export const BRAND = {
  primary:    '[BRAND primary color]',
  secondary:  '[BRAND secondary/accent color]',
  mid:        '[BRAND mid tone color]',
  text:       '[BRAND text on dark]',
  gradient:   '[BRAND gradient]',
  fontDisplay: '[BRAND display font]',
  fontBody:    '[BRAND body font]',
  fps: 30,
  width: 1080,
  height: 1920,
} as const;
```

### `src/Root.tsx`
```typescript
import { Composition } from 'remotion';
import { Reel } from './Reel';
import { BRAND } from './tokens';

export const RemotionRoot = () => (
  <Composition
    id="Reel"
    component={Reel}
    durationInFrames={[TOTAL_DURATION_IN_FRAMES]}  // e.g. 60s × 30fps = 1800
    fps={BRAND.fps}
    width={BRAND.width}
    height={BRAND.height}
    defaultProps={{
      points: [
        { label: '[Point 1 from script]', frame: [entry frame] },
        { label: '[Point 2 from script]', frame: [entry frame] },
        { label: '[Point 3 from script]', frame: [entry frame] },
      ],
      ctaText: '[BRAND default CTA text]',
      ctaFrame: [CTA entry frame],
    }}
  />
);
```

### `src/components/Intro.tsx`
```typescript
import { useCurrentFrame, interpolate, Easing, Img, staticFile } from 'remotion';
import { BRAND } from '../tokens';

export const Intro = () => {
  const frame = useCurrentFrame();

  const logoOpacity = interpolate(frame, [10, 25], [0, 1], { extrapolateRight: 'clamp' });
  const logoY      = interpolate(frame, [10, 25], [40, 0], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const lineWidth  = interpolate(frame, [20, 45], [0, 320], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const taglineOpacity = interpolate(frame, [35, 50], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      width: '100%', height: '100%',
      background: BRAND.gradient,
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{ opacity: logoOpacity, transform: `translateY(${logoY}px)` }}>
        <Img src={staticFile('logo.png')} style={{ width: 240, marginBottom: 24 }} />
      </div>
      <div style={{ width: lineWidth, height: 2, background: BRAND.secondary, marginBottom: 20 }} />
      <div style={{
        opacity: taglineOpacity,
        color: BRAND.secondary,
        fontFamily: BRAND.fontDisplay,
        fontSize: 28, letterSpacing: 6,
        textTransform: 'uppercase', textAlign: 'center',
      }}>
        [BRAND tagline]
      </div>
    </div>
  );
};
```

### `src/components/PointCard.tsx`
```typescript
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { BRAND } from '../tokens';

interface Props { label: string; index: number; entryFrame: number; }

export const PointCard = ({ label, index, entryFrame }: Props) => {
  const frame = useCurrentFrame();
  const localFrame = frame - entryFrame;

  const x       = interpolate(localFrame, [0, 20], [-500, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const opacity = interpolate(localFrame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  if (localFrame < 0) return null;

  return (
    <div style={{
      position: 'absolute',
      bottom: 280 + index * 120,
      left: 40, right: 40,
      transform: `translateX(${x}px)`,
      opacity,
    }}>
      <div style={{
        background: `${BRAND.primary}EE`,
        borderLeft: `4px solid ${BRAND.secondary}`,
        borderRadius: 8,
        padding: '16px 20px',
        display: 'flex', alignItems: 'center', gap: 16,
      }}>
        <div style={{
          width: 36, height: 36, borderRadius: '50%',
          background: BRAND.secondary,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
          color: BRAND.primary,
          fontFamily: BRAND.fontBody,
          fontWeight: 'bold', fontSize: 16,
        }}>
          {index + 1}
        </div>
        <span style={{
          color: BRAND.text,
          fontFamily: BRAND.fontBody,
          fontSize: 28, lineHeight: 1.3, fontWeight: '600',
        }}>
          {label}
        </span>
      </div>
    </div>
  );
};
```

### `src/components/CTACard.tsx`
```typescript
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { BRAND } from '../tokens';

interface Props { text: string; entryFrame: number; }

export const CTACard = ({ text, entryFrame }: Props) => {
  const frame = useCurrentFrame();
  const localFrame = frame - entryFrame;

  const scale   = interpolate(localFrame, [0, 20], [0.8, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.back(1.5)),
  });
  const opacity = interpolate(localFrame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  if (localFrame < 0) return null;

  return (
    <div style={{
      position: 'absolute', bottom: 120, left: 40, right: 40,
      opacity, transform: `scale(${scale})`,
    }}>
      <div style={{
        background: BRAND.primary,
        border: `2px solid ${BRAND.secondary}`,
        borderRadius: 12,
        padding: '20px 28px',
        textAlign: 'center',
      }}>
        <span style={{
          color: BRAND.text,
          fontFamily: BRAND.fontDisplay,
          fontSize: 30, letterSpacing: 1,
        }}>
          {text}
        </span>
      </div>
    </div>
  );
};
```

### `src/Reel.tsx` (main composition)
```typescript
import { useCurrentFrame, AbsoluteFill } from 'remotion';
import { Intro } from './components/Intro';
import { PointCard } from './components/PointCard';
import { CTACard } from './components/CTACard';

interface Props {
  points: Array<{ label: string; frame: number }>;
  ctaText: string;
  ctaFrame: number;
}

// Usage modes:
// - With footage: render with transparent background → overlay via FFmpeg (Phase 2, step 6)
// - Without footage: render as full video with gradient background

export const Reel = ({ points, ctaText, ctaFrame }: Props) => {
  const frame = useCurrentFrame();
  const INTRO_DURATION = 60; // 2s at 30fps

  return (
    <AbsoluteFill>
      {frame < INTRO_DURATION && <Intro />}
      {frame >= INTRO_DURATION && points.map((p, i) => (
        <PointCard key={i} label={p.label} index={i} entryFrame={p.frame} />
      ))}
      <CTACard text={ctaText} entryFrame={ctaFrame} />
    </AbsoluteFill>
  );
};
```

### Render commands
```bash
# Preview in browser
npx remotion studio

# Render with transparent background (for FFmpeg overlay)
npx remotion render Reel --output=remotion_overlay.mp4 \
  --codec=prores --prores-profile=4444

# OR render as standalone video (no footage)
npx remotion render Reel --output=[BRAND output_directory]/Reel_[Topic].mp4 \
  --codec=h264
```

---

## Deliverables per session

| File | Description |
|---|---|
| `[output_dir]/script_[topic]_[date].md` | Full script with timestamps |
| `[output_dir]/ffmpeg_[topic]_[date].sh` | Bash script with all FFmpeg commands |
| `[output_dir]/[topic]-remotion/` | Complete Remotion project ready to render |
