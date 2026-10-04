---
name: "plain_language"
description: "Write and review user-visible copy in Sebastian's adopted plain-language standard (GOV.UK + US federal plain language, Microsoft/Mailchimp tone, CEFR B1 reader); use when drafting, editing, auditing, or linting product strings, onboarding text, chat copy, error messages, marketing copy, or any prose a user will read."
---

# Plain Language

## Purpose
Make user-visible copy direct and relaxed by adhering to an adopted external standard instead of ad-hoc taste rules. Apply this skill whenever copy is written, rewritten, reviewed, or linted: app strings, onboarding, coach/chat text, errors, paywalls, help, emails, landing pages, and marketing lines.

## The standard (adopted 2026-10-03)
Plain language, UK/US federal style, with a conversational product voice:

- Umbrella definition: ISO 24495-1:2023 - readers can find, understand, and use the text.
- Rule source: GOV.UK clear language + A-to-Z style guide; US federal plain-language guidance (Digital.gov, Plain Writing Act tradition).
- Tone source: Microsoft style guide ("write like you speak") and the Mailchimp voice guide.
- Target reader: CEFR B1 (confident intermediate). If a B1 reader would stall, simplify.
- Long-form tripwire: Shopify Polaris aims at grade 7; the house bar is US grade 8 or Flesch Reading Ease 60+ on surfaces of 100 words or more only.
- Spelling: US by default. GOV.UK substitution lists still apply regardless of spelling.

Project house laws sit on top of this standard and win on their own surfaces (for example Prelude: no em dashes, never the word "soft", the saved-words feature is called "What I'll say").

## The 14 rules
1. **Audience test first.** Every string must let its reader find, understand, and use it on first read. If it needs a second read, rewrite. (US Plain Writing Act; ISO 24495-1)
2. **Write to a B1 reader.** Familiar matters, simple connected text, brief reasons. (Council of Europe B1 descriptor) Check: read it aloud; if you stumble, the reader will too.
3. **One idea, one instruction, per sentence.** Split on the second action or second idea. (Digital.gov; STE structure, borrowed)
4. **Sentence caps:** 20 words or fewer in instructions and errors, 25 anywhere. Paragraphs 5 sentences or fewer; in UI, usually 2. (STE caps; GOV.UK)
5. **Condition before action.** "If X, do Y." Warnings come before the step they guard. (STE procedural writing)
6. **Active voice, named actor, present tense.** "We could not save your changes," not "your changes were not saved." Passive only when the actor truly does not matter. (Digital.gov; GOV.UK)
7. **Address the user as "you"; the product speaks as "we."** Buttons and instructions start with a verb: "Save changes," not "You can save changes." (GOV.UK; 18F; Microsoft; Polaris)
8. **Common words; banned formal synonyms.** House law: use (not utilize/leverage), help (not assist/facilitate), buy (not purchase), start (not commence/initiate), end or stop (not terminate), about (not approximately/regarding), before (not prior to), so (not consequently), to (not in order to), make sure (not ensure), fill in (not complete a form). (GOV.UK words to avoid; 18F; Plain English Campaign) This one rule does most of the daily work.
9. **One term for one thing.** Use the word users use; never rotate synonyms for elegance across UI, chat, onboarding, help, and errors. Define any unavoidable technical term in plain words on first use. (STE one-word-one-meaning; GOV.UK; Mailchimp)
10. **No noun stacks over 3 words; no nominalizations.** Rewrite -ion/-ment nouns as verbs: "We will check," not "validation will be performed." (STE noun clusters; Digital.gov hidden verbs)
11. **Conversational, contracted, sentence case.** Contractions in body, chat, and onboarding (it's, you'll, don't). Sentence case for headings, labels, and buttons; no title case, no all-caps emphasis. Exception: in warnings about irreversible actions, spell the negative out in full: "Do not delete." (Microsoft; Mailchimp; GOV.UK contraction caution, narrowed to high-stakes strings)
12. **Direct, positive, specific. No vague boosters.** Say what happened, what it means, what to do next. Ban unquantified easy/easily, simply, just, key, robust, seamless, powerful, and empty hype. Write what the user can do, not only what they can't. (GOV.UK; Mailchimp; 18F)
13. **No idiom, slang, jokes, or wordplay in functional copy.** Humor only in low-stakes marketing or celebration copy, dry and optional, never in errors, permissions, paywalls, or destructive confirmations, and never where the text must survive translation. (Mailchimp; GOV.UK/18F)
14. **Long-form tripwire only.** Surfaces of 100 words or more (full onboarding flow, help article, paywall explainer, email) must score grade 8 or lower (or FRE 60+) and pass a Hemingway pass. Never score single strings; readability formulas are unstable under 100 words. (Polaris grade 7, softened; formula-instability evidence)

## Resolved disagreements
- **Contractions:** STE bans them; Microsoft and Mailchimp require them; GOV.UK splits. House rule: contract freely, except full negatives in high-stakes warnings (rule 11).
- **Brevity vs completeness:** STE bans omitted subjects; product UI needs 1-3 word labels. Completeness rules bind sentences; buttons and labels may be verb-first fragments (rule 7).
- **Idiom and humor:** banned in functional copy; allowed, dry and optional, in low-stakes marketing (rule 13).
- **"Easy/simply":** banned in help, errors, and instructions (it demoralizes stuck users); allowed in taglines only with a specific claim attached (rule 12).
- **Reading numbers:** reading age 9, grade 7, grade 9 are different instruments. Hold the reader constant (B1, first read) and use one numeric tripwire (grade 8, long-form only).
- **Button casing:** Mailchimp title-cases buttons; GOV.UK and Microsoft mandate sentence case. House rule: sentence case.

## What we do not use
- **ASD-STE100 as the standard.** Its structural rules (3, 5, 10) are borrowed, but its bans on contractions, present perfect, and phrasal verbs break conversational copy, and conformance requires its licensed dictionary.
- **Basic English (850 words) and Globish (1,500 words).** Frozen vocabularies that force circumlocution on modern product terms. Keep only the frequency mindset behind rules 2 and 8.

## Workflow
1. Draft in the reader's words (rule 9), B1 persona in mind.
2. First-read test (rules 1-2). Read aloud.
3. Structure pass: one idea per sentence, caps, condition-first, no noun stacks (rules 3, 4, 5, 10).
4. Voice pass: active, you/we, verb-first, contracted, positive and specific (rules 6, 7, 11, 12).
5. Words pass: substitution list, one term per thing (rules 8, 9).
6. Functional or marketing? Apply rule 13 accordingly.
7. 100 words or more: grade tripwire + Hemingway pass (rule 14).

## Review output contract
When reviewing copy, report each violation by rule number, give the rewrite, and keep the user's own words where they work. Flag idiom that will not survive translation. Never report a readability grade for a string under 100 words. If the copy is compliant, say so plainly instead of inventing improvements.

## Enforcement
- Vale at warning level in CI on the strings/i18n folder. The rule-8 substitution rule is the highest-value check; add passive-voice and sentence-length warnings next. Precedent: GOV.UK One Login runs a 15-rule Vale package in its Android build.
- A readability script + Hemingway pass on long-form files only (rule 14 surfaces).
- Read-aloud and B1-persona review for coach/chat tone; no tool checks warmth.

## Sources
- GOV.UK, Use clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- GOV.UK, A to Z style guide (words to avoid): https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- Digital.gov, plain language writing guides: https://digital.gov/guides/plain-language/writing
- Microsoft, Top 10 tips for style and voice: https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice
- Mailchimp, Voice and Tone: https://styleguide.mailchimp.com/voice-and-tone/
- 18F Content Guide, plain language: https://github.com/18f/content-guide/blob/HEAD/_pages/our-approach/plain-language.md
- Council of Europe, CEFR global scale: https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale
- ISO 24495-1:2023, plain language standard: https://www.iso.org/standard/78907.html
