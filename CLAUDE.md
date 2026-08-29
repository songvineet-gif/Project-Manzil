# Project Manzil — Website Build Notes

This file is read automatically by Claude Code every time it's opened in this
folder. It exists so you don't have to re-explain the project each session —
just tell Claude Code which step to work on.

## What this business is

Project Manzil is a one-step mortgage/home-loan advisory service in the UAE.
The pitch: tell us what you need once, we compare offers across banks and
negotiate on your behalf, and you get the best deal with a clear timeline —
no chasing banks yourself.

## Design reference — read before touching styling

We are building this site "in the spirit of" mortgagefinder.ae — same category
of site, same kind of features (rate/affordability calculator, bank partner
grid, step-by-step journey, testimonials, FAQ, lead capture). We are **not**
copying their logo, exact wording, or visual identity — that's their
trademarked property. Match the *functionality and structure* of a
professional mortgage-advisory site, not their specific design.

## Current design system (already in index.html — keep consistent)

- Colors: navy `#081226` / `#0b1a33` / `#12274a` (backgrounds, header, footer),
  gold `#c99a3c` / `#d9b25c` (accent, CTAs, highlights)
- Font: Inter (Google Fonts)
- Style: clean, trustworthy, fintech-leaning. Rounded cards, soft shadows,
  generous whitespace.
- Single file: everything lives in `index.html` — inline `<style>` and
  `<script>`, no build step, no framework. Keep it that way unless asked to
  change it.

## Contact details — current state

- Email: `info@manazil.com` — real, keep as-is unless told otherwise.
- Phone / WhatsApp: `505051234` — **this is a placeholder**. The user will
  provide the real WhatsApp number separately. Ask before replacing it, and
  don't assume the placeholder is correct.

## Rule on stats, reviews, and claims — important

Do **not** invent specific real-sounding business claims (e.g. "1,600+
five-star reviews," "20+ years experience," named bank partnerships,
fabricated testimonials attributed to named people). Those are the kind of
concrete factual claims real visitors would rely on, and inventing them would
be misleading once the site is live.

Where the user hasn't given real numbers/testimonials/partners yet:
- Use clearly generic, round placeholder numbers (e.g. "500+", "10+ years") —
  the user will personally replace these with their real figures before
  launch. Do not present placeholders as if verified.
- For testimonials, use a couple of short generic placeholder quotes with
  placeholder names (e.g. "A. Khan — Dubai"), and note in a code comment that
  these need to be swapped for real client quotes before launch.
- For bank partners, don't claim a specific named bank as a partner unless
  the user has confirmed it. Generic wording like "UAE's leading banks" is
  fine; a logo grid of specific real banks is not, unless confirmed.

## Hosting / deploy pipeline (already working — don't change)

- Repo: `github.com/songvineet-gif/Project-Manzil`, branch `main`.
- Netlify project `projectmanzil` deploys from this repo automatically on
  every push to `main`. No build command, publish directory is repo root.
- Netlify Forms is wired on the contact form (`data-netlify="true"`) —
  submissions land in the Netlify dashboard under Site → Forms.
- Workflow: edit `index.html` → `commit my changes with a descriptive
  message and push` → Netlify redeploys within ~30-60s.
- **Do not deploy/push until the user explicitly says the site is ready** —
  they want to review the whole build locally first, then deploy once. Still
  commit each step's changes to git as you go, but confirm with the user
  before the final push if they've said they want to hold off.

## Build plan — work through one step at a time

Check off a step here once it's done, and don't move to the next one until
the user confirms they're happy with the current one.

- [x] Step 0: Base landing page (hero, how it works, timeline, why-us,
      contact form) — already built, this is the current `index.html`.
- [x] Step 1: Hero + trust bar — headline, CTA, and a row of trust stats
      (rating, years active, deals closed — real figures confirmed by user:
      5/5 Google rating, 3+ years, 100+ deals closed).
- [ ] Step 2: How it works — expand to a 4–5 step visual journey (currently
      3 steps).
- [ ] Step 3: Interactive mortgage calculator — property price, down
      payment, loan term, rate → estimated monthly payment, client-side JS,
      no backend.
- [ ] Step 4: Bank partners section — generic wording unless the user
      confirms real partner banks (see rule above).
- [ ] Step 5: Why Manzil / advantages — differentiator cards.
- [ ] Step 6: Services section — cards per loan type (resident,
      non-resident, refinance, commercial — confirm which apply).
- [ ] Step 7: Testimonials + FAQ — placeholder testimonials (see rule
      above) + FAQ answering common mortgage questions.
- [ ] Step 8: Stronger lead capture + full footer (legal links, contact,
      social) — extend the existing Netlify-Forms contact form.

## How to work each session

1. Read this file's checklist to see what's next.
2. Ask the user to confirm which step to tackle if it's not obvious.
3. Make the change directly in `index.html`.
4. Update the checkbox above for the completed step.
5. Commit locally. Only push to `main` if the user has said to, or if this
   is a step they've explicitly asked to see live.
