# P.4 - the two readings of "wind"

Checked on 2026-10-09 with the five candidate voices. Chosen voices: `af_heart` and `am_adam`.

Kokoro turns text into sounds before a voice is applied. So the sound string is the same for all
five voices, and this result holds for both chosen voices.

| Input | Sound string from Kokoro | Expected | Result |
| --- | --- | --- | --- |
| `wind`, alone | `wˈɪnd` | contains `wˈɪnd`, the noun, `w:wind#1` | pass |
| `Please wind the clock before you leave the kitchen.` | `plˈiz wˈInd ðə klˈɑk bəfˈɔɹ ju lˈiv ðə kˈɪʧᵊn.` | contains `wˈInd`, the verb, `w:wind#2` | pass |

In Kokoro's own symbols the letter `I` stands for the sound /aɪ/. So `wˈInd` is /waɪnd/.

What this means for task P.10:

- Alone, "wind" is always the noun. To get the verb sound for the card `w:wind#2`, the word must
  be spoken inside a verb sentence and cut out, or the sound string must be given to Kokoro directly.
- A noun sentence was also in the set: `The cold wind and rain left everyone exhausted.` gave
  `wˈɪnd`, the noun. Context decides, and it decided right in both sentences tried.
- Two sentences are not proof for every sentence. P.10 should check the sound string of every
  audio it makes for a word with two readings.

By ear: the listener scored the four samples below without knowing the voice. The scores say the
samples were clear. They do not say which reading was heard; that needs one direct listen.

| Sample | Voice | Text | Clarity, natural in sittings R1, R2, R3 |
| --- | --- | --- | --- |
| `s025` | `af_heart` | wind | 5,4 · 5,4 · 4,4 |
| `s037` | `af_heart` | Please wind the clock... | 5,4 · 5,5 · 5,5 |
| `s121` | `am_adam` | wind | 5,3 · 5,4 · 4,4 |
| `s090` | `am_adam` | Please wind the clock... | 4,3 · 5,3 · 3,3 |
