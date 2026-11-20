# Prompt Rules (visual consistency)

## Fixed style line (prefix EVERY image and video prompt with it)
"Hand-drawn 2D children's storybook illustration, soft colored-pencil and
crayon texture, warm muted pastel palette, cream paper tones, soft brown
outlines, rosy cheeks, gentle cozy lighting, simple uncluttered backgrounds,
flat 2D, 16:9, no text, no logos."

Always append to video prompts: "keep the flat 2D hand-drawn look and paper
texture, not 3D, no CGI, no line flicker, limited gentle animation".

## 2D animation approach (cheaper, calmer, more consistent)
- Prefer limited animation: blinking, breathing, small head tilts, arm waves,
  ears/tail wiggles, slow camera pan or push-in over the illustration.
- Many scenes can be a still illustration + gentle camera move (parallax)
  instead of a full video clip; use full video only for key actions
  (hug, dance, giving the toy). Target: ~40% of scenes as motion clips.
- Keep clips 4-6 s; avoid complex walking/turning, which breaks 2D style.

## Characters
- Always paste the locked description of each character from
  `characters/characters.md` (look, outfit, colors) in every prompt they appear in.
- Use the stored reference media ids / character sheet id for image-to-image or
  reference-guided generation whenever the tool supports it.
- Max 3 characters per scene; fewer characters = fewer consistency errors.

## Scene prompts
- One clear action per scene, described as a visible movement
  ("Milo hugs the teddy bear tightly and turns away"), plus emotion and camera
  (wide / medium / close-up). Keep camera simple: static or slow push-in.
- Video clips: 4-8 seconds, gentle motion, no fast cuts, no flashing lights.
- Negative constraints to append: "no extra limbs, no distorted hands,
  no text, no scary faces, no realistic violence".

## Consistency workflow
1. Generate (or import) one character sheet per main character once
   (`/kids-story-studio characters`) and store ids in `characters.md`.
2. For each episode: image per scene with references → animate approved images
   to video → never generate a main character from text alone.

## Episode continuity (learned from Episode 01 test)
- Lock every story prop in one sentence (e.g. "the crayon box is always a small
  wooden box with a hinged lid") and append it to every scene prompt.
- For each recurring setting (porch, kitchen, playground), first generate ONE
  empty "master background" image (no characters) and pass it as an extra
  reference in every scene set there. Store its job id in the episode's assets.json.
- Re-check small signature details in QA (e.g. Huggle's heart patch must be
  clearly heart-shaped and visible).
