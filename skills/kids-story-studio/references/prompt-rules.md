# Prompt Rules (visual consistency)

## Fixed style line (prefix EVERY image and video prompt with it)
Defined in `channel.md` as `STYLE_LINE`. Default until the user picks one:
"Soft 3D children's animation style, rounded friendly shapes, bright pastel
colors, warm soft lighting, clean simple backgrounds, gentle expressions,
16:9, high detail, no text, no logos."

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
