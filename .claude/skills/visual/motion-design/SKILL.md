---
name: motion-design
description: >
  Turns Claude Code into a motion-design studio using Remotion. Scaffolds a Remotion
  project, builds animated video compositions from a plain-language description, lets the
  user iterate by conversation in the live preview, and renders a final mp4 — all in the
  company's visual identity. Activate when the user asks for an animated video, motion
  graphic, logo animation, animated intro/outro, kinetic text, or "make a video from this".
---

# Motion Design (Remotion)

> Claude writes the animation, the user directs it. No keyframes, no heavy editor.
> Describe the scene → Claude builds the Remotion composition → iterate in the live
> preview → render an mp4.
>
> Read the BRAND BLOCK below before starting. If any `[FILL IN]` markers remain, stop and
> ask the user to complete the BRAND BLOCK first.
>
> For a full Instagram Reel (script + footage + FFmpeg assembly), use the
> `ig-reel-producer` skill instead. This skill is for standalone animated pieces:
> intros, outros, kinetic text, logo animations, explainers, ad bumpers, title cards.

---

## BRAND BLOCK (customize once — source of truth for all motion pieces)

> Replace every `[FILL IN ...]` placeholder with your company's details.
> Pre-fill colors and fonts from `resources/identity/design-guide.md`. Once filled in, never change
> per-video — only update when the brand identity changes.

### Identity

**Company / brand name (shown in animations):**
`[FILL IN — e.g. Acme Corp]`

**Tagline / category line:**
`[FILL IN — e.g. FINANCIAL CONSULTING | INNOVATION]`

**Logo path:**
`[FILL IN — absolute path to logo file, e.g. /Users/you/company/resources/identity/assets/logo.png]`

### Colors (hex)

**Primary / background:**
`[FILL IN — e.g. #0B0B2D]`

**Accent / highlight:**
`[FILL IN — e.g. #FF5000]`

**Text on background:**
`[FILL IN — e.g. #FFFFFF]`

**Secondary / card or mid tone:**
`[FILL IN — e.g. #201F7D]`

**Gradient (if used):**
`[FILL IN — e.g. linear-gradient(90deg, #0B0B2D 0%, #2B29A6 100%) — or leave blank]`

### Typography

**Display font (headlines, logo lockup, CTA):**
`[FILL IN — e.g. Georgia, serif]`

**Body font (captions, labels):**
`[FILL IN — e.g. Arial, Helvetica, sans-serif]`

> Custom fonts: drop the file in `public/fonts/` and load with `@remotion/google-fonts`
> or a local `@font-face`. State the exact font name so Claude wires it correctly.

### Motion style

**Animation personality:**
`[FILL IN — e.g. Calm and editorial: slow fades, gentle springs, no bounce. OR punchy and energetic: fast cuts, overshoot springs, snappy scale-ins.]`

**Default easing:**
`[FILL IN — e.g. Easing.out(Easing.cubic) for editorial, Easing.out(Easing.back(1.5)) for punchy]`

**What the motion never does:**
`[FILL IN — e.g. No flashing, no spinning logos, no more than 2 effects on screen at once.]`

### Output

Everything lives in a **content working folder** (the same convention carousels use):

```
areas/marketing/content/<YYYY>/<MM>/WEEK <NN>/<platform>/<name>/
```

`<platform>` = `instagram`, `youtube`, `tiktok`, or `video` if platform-agnostic. The full
Remotion project is scaffolded **inside** this folder and the rendered `<name>.mp4` is
written to the folder root. When the user approves the video, run **`motion-approved`** to
delete the whole project and keep only the `.mp4`.

> Adapt the path if this workspace organizes content differently.

---

## Phase 0 — Project setup

Remotion needs **Node.js installed**. Confirm with `node --version` if unsure.

1. **Resolve the content working folder** for this video:
   `areas/marketing/content/<YYYY>/<MM>/WEEK <NN>/<platform>/<name>/` (create it if missing).
   Confirm the path with the user before scaffolding.

2. **Scaffold the Remotion project inside that folder:**
   ```bash
   npx create-video@latest .
   ```
   Pick the **"Hello World"** (blank) template, then `npm install`. Reuse `node_modules`
   from a recent video folder when possible — no need to reinstall every time.

3. Copy the BRAND logo into the project's `public/` folder so `staticFile('logo.png')`
   resolves at render time.

If the user is brand new to this, explain the layout in one line: `src/Root.tsx` registers
compositions, `src/` holds the components, `public/` holds assets, the rendered `.mp4` sits
at the content folder root.

---

## Phase 1 — Brief

Get these before writing any code (ask only for what's missing — if the user already
described the scene in detail, skip straight to Phase 2):

1. **Format / dimensions** — vertical 1080×1920 (Reels/TikTok/Stories), square 1080×1080
   (feed), horizontal 1920×1080 (YouTube/web), or custom.
2. **Duration** — in seconds (Claude converts to frames at 30fps unless told otherwise).
3. **Scene** — what happens, in order. Encourage concreteness: which elements, when they
   enter, how they move, what the text says, where the logo appears.
4. **Output** — final mp4, transparent overlay (ProRes 4444), or GIF.

Restate the brief as a one-line shot list before building so the user can correct it cheaply.

---

## Phase 2 — Build the composition

Translate the brief into Remotion components. Drive everything from a `tokens.ts` populated
from the BRAND BLOCK — never hardcode brand values inline.

### `src/tokens.ts`
```typescript
export const BRAND = {
  primary:     '[BRAND primary color]',
  accent:      '[BRAND accent color]',
  text:        '[BRAND text color]',
  secondary:   '[BRAND secondary color]',
  gradient:    '[BRAND gradient or "" ]',
  fontDisplay: '[BRAND display font]',
  fontBody:    '[BRAND body font]',
  fps: 30,
  width:  [from brief],
  height: [from brief],
} as const;
```

### `src/Root.tsx`
```typescript
import { Composition } from 'remotion';
import { Main } from './Main';
import { BRAND } from './tokens';

export const RemotionRoot = () => (
  <Composition
    id="Main"
    component={Main}
    durationInFrames={[seconds × BRAND.fps]}
    fps={BRAND.fps}
    width={BRAND.width}
    height={BRAND.height}
    defaultProps={{ /* text, timings from the brief */ }}
  />
);
```

### Animation rules
- Animate with `useCurrentFrame()` + `interpolate(...)` for fades/moves, and `spring(...)`
  for entrances that should feel physical. Apply the BRAND default easing.
- Build the scene as small components (e.g. `Logo`, `Headline`, `LowerThird`), composed in
  `Main.tsx` with `AbsoluteFill` and time-gated with `<Sequence from={...}>`.
- Honor the BRAND motion style and the "what the motion never does" line.
- Pull every color, font, and the logo from `tokens.ts` / `public/`.

### Minimal entrance pattern (reuse for any element)
```typescript
import { useCurrentFrame, interpolate, spring, useVideoConfig, Easing } from 'remotion';
import { BRAND } from './tokens';

export const Headline: React.FC<{ text: string; from: number }> = ({ text, from }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - from;

  const opacity = interpolate(local, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const rise = spring({ frame: local, fps, config: { damping: 200 } }); // 0 → 1 spring
  const y = interpolate(rise, [0, 1], [40, 0]);

  if (local < 0) return null;
  return (
    <h1 style={{
      opacity, transform: `translateY(${y}px)`,
      color: BRAND.text, fontFamily: BRAND.fontDisplay,
    }}>
      {text}
    </h1>
  );
};
```

---

## Phase 3 — Iterate + export

This is the loop the user lives in. Keep it conversational.

**A. Open the live preview** (hot-reloads on every code change):
```bash
npx remotion studio
```

**B. Take change requests in plain language** and edit the code — the preview updates live.
Common asks and where they land:
| Request | Change |
|---|---|
| "make the text 20% bigger" | `fontSize` on that element |
| "change the orange to blue" | `accent` in `tokens.ts` |
| "start 1s later" | bump the `from` / `Sequence from` by `1 × fps` frames |
| "make it slower / snappier" | widen/narrow the `interpolate` input range or change easing |
| "hold the logo longer" | extend that `Sequence`'s `durationInFrames` |

Text and timing iterations are free — only the final render costs compute/time.

**C. Render when approved** — render into the content folder root (run from inside it):
```bash
# Standard mp4
npx remotion render Main "[name].mp4" --codec=h264

# Transparent overlay (to composite over footage in an editor or FFmpeg)
npx remotion render Main "[name]_overlay.mov" --codec=prores --prores-profile=4444

# Animated GIF
npx remotion render Main "[name].gif" --codec=gif
```

Confirm the output path and report the rendered file location. When the user approves the
final video and wants no more changes, run **`motion-approved`** to strip the project down
to just the `.mp4`.

---

## Deliverables per session

Inside `areas/marketing/content/<YYYY>/<MM>/WEEK <NN>/<platform>/<name>/`:

| File | Description |
|---|---|
| `src/` + `public/` | Remotion project — composition, components, brand assets |
| `src/tokens.ts` | BRAND values, single source of truth |
| `<name>.mp4` | The rendered video (folder root) — the only thing `motion-approved` keeps |

---

## Notes

- One `npx remotion render` is a compute job, not an API call — but it takes real time and
  CPU. Iterate in the studio preview (free, instant) and render only when approved.
- For footage-based Reels with a spoken script, use `ig-reel-producer`.
- If a render fails, check: Node installed, `npm install` ran, logo present in `public/`,
  composition `id` matches the render command, and `durationInFrames` > 0.
