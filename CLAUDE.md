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
- Font: Times New Roman (serif)
- Style: clean, trustworthy, fintech-leaning. Rounded cards, soft shadows,
  generous whitespace.
- Single file: everything lives in `index.html` — inline `<style>` and
  `<script>`, no build step, no framework. Keep it that way unless asked to
  change it.

## Contact details — current state

- Email: `info@manazil.com` — real, keep as-is unless told otherwise.
- Phone / WhatsApp: real number confirmed by user — `+971 50 569 6741`
  (displayed formatted; wa.me/tel links use `971505696741`).
- Legal entity: registered/legal name is **Manazil**, based in Dubai, UAE.
  "Project Manzil" is kept as the on-site brand/trading name; footer states
  "Project Manzil is a trading name of Manazil". User confirmed Manazil is a
  licensed, independent mortgage broker registered with a UAE regulator (no
  specific license number given — don't invent one, use generic "licensed
  and registered" wording only).
- Business model: **free to the client** — Manazil earns commission from the
  bank on completed loans, not from the customer. Site copy should reflect
  this (hero trust bullet, contact section, footer, FAQ) rather than generic
  "no cost to compare" wording.
- Instagram: `@Manazil.DXB` (https://instagram.com/Manazil.DXB) — real,
  linked in footer.

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
- [x] Step 2: How it works — expanded to a 5-step visual journey.
- [x] Step 3: Interactive mortgage calculator — property price, down
      payment (slider), loan term (slider), rate (slider) → estimated
      monthly payment, total interest, total repayment. Client-side JS only.
- [x] Step 4: Bank partners section — real UAE bank names shown as
      **text-only badges** (Emirates NBD, ADCB, Mashreq, ADIB, DIB, HSBC UAE,
      FAB, RAKBANK), not their actual trademarked graphic logos (no logo
      image assets were sourced/used). User said real bank names/logos are
      fine for this dummy build and not to worry about legal risk for now —
      if this site goes live to real customers, real bank logos should not
      be used without permission; text badges avoid that risk either way.
- [x] Step 5: Why Manzil / advantages — expanded to 6 differentiator cards
      (added "Free for you, always" and "Licensed & independent" reflecting
      the confirmed business model).
- [x] Step 6: Services section — 4 cards: Resident, Non-Resident,
      Refinancing, Commercial mortgages (user confirmed all four apply).
- [x] Step 7: Testimonials + FAQ.
      Testimonials: 3 generic placeholder quotes with placeholder-style
      names (e.g. "S. Ahmed — Dubai"), flagged in an HTML comment to be
      swapped for real, permissioned client quotes before launch. **Note:**
      the user asked for testimonials deliberately engineered to look like
      genuine reviews (mismatching real people's first/last names so they
      "look real"). That was declined — presenting fabricated reviews as
      genuine on a live financial-services site is deceptive/potentially
      unlawful, which is exactly what this file's own rule above is meant to
      prevent. Kept these clearly generic and swap-before-launch instead.
      FAQ: 13 Q&As across 5 categories (General, Costs & Fees, Eligibility,
      Process & Timeline, Rates & Terms, About Us) — written generically
      (e.g. down-payment %, documents needed) without inventing precise
      figures that could go stale or wrong.
- [x] Step 8: Stronger lead capture + full footer — added Instagram link,
      real WhatsApp number, Privacy Policy (`privacy.html`) and Terms &
      Conditions (`terms.html`) as new standalone pages (drafted generically
      for a UAE mortgage-broker site; both carry an on-page note that a
      lawyer should review before real launch), commission/licensing
      disclosure line in footer and contact section.
- [x] Step 9: Mortgage calculator upgraded to market standard, then to
      CBUAE-accurate. Buyer type is nationality-based (UAE national /
      expat resident / non-resident) because Reg 31/2013 keys LTV off
      nationality, not residency. Property type (first / second /
      off-plan) also changes the cap. Full matrix: nationals 80/70/65,
      expats 75/65/60, off-plan 50 for everyone. Non-resident figures
      are bank policy, NOT a Central Bank cap — labelled as such on the
      site. Also added upfront-cost breakdown (DLD 4%+580, mortgage reg
      0.25%+290, valuation, arrangement fee) and a yearly amortisation
      schedule.
- [x] Step 10: "How much can you borrow" affordability block. Models the
      50% Debt Burden Ratio, counts credit cards at 5% of *limit* (not
      balance) as UAE banks do, applies the income multiple cap (8x
      nationals / 7x expats), and names which of the three ceilings
      binds. Rule constants live in BUYER_RULES / DBR_CAP /
      CARD_LIMIT_FACTOR in index.html — update there if rules change.
- [x] Step 11: Scroll motion design. Columns reveal from their own side
      of the grid, staggered across each row; cards lift on hover
      (pointer devices only); hero card parallax. Reveal classes are
      applied from JS, never in markup, so a script failure cannot leave
      the page blank — keep it that way. Honours prefers-reduced-motion.
      body has overflow-x:clip (not hidden — hidden would break the
      sticky header) because sideways reveals otherwise cause horizontal
      scroll on mobile.

## How to work each session

1. Read this file's checklist to see what's next.
2. Ask the user to confirm which step to tackle if it's not obvious.
3. Make the change directly in `index.html`.
4. Update the checkbox above for the completed step.
5. Commit locally. Only push to `main` if the user has said to, or if this
   is a step they've explicitly asked to see live.
