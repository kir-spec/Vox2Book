# STT / OCR — candidate table (English)

> **Not loaded automatically.**  
> **Not a replacement script.** Context only — see [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md).

Other languages: [RU](STT_HOMOPHONES.ru.md) · [UK](STT_HOMOPHONES.uk.md) · [index](STT_HOMOPHONES.example.md)

---

## JSON entry format

```json
{
  "heard": "you es bee|U S B",
  "correct": "USB",
  "context_hint": "cable, port, flash drive",
  "never_replace_globally": true
}
```

---

## Classic homophones (context decides — never auto-fix)

| Heard / confused | Intended | Context |
|------------------|----------|---------|
| there | their / they're | possession vs contraction vs location |
| your | you're | possession vs you are |
| its | it's | possession vs it is |
| to / too / two | pick by meaning | direction vs also vs number |
| then | than | time vs comparison |
| hear | here | listen vs place |
| accept | except | receive vs exclude |
| affect | effect | verb vs noun (result) |
| weather | whether | climate vs if |
| right | write / rite | correct vs compose vs ceremony |
| peace | piece | calm vs fragment |
| bare | bear | naked vs animal / tolerate |
| brake | break | stopping vs fracture / pause |
| board | bored | panel vs uninterested |
| mail | male | post vs gender |
| pair | pear / pare | couple vs fruit vs trim |
| principal | principle | school head vs rule |
| stationary | stationery | not moving vs paper supplies |
| complement | compliment | complete set vs praise |
| desert | dessert | arid land vs sweet course |
| loose | lose | not tight vs misplace |
| passed | past | verb vs time/preposition |
| cite | sight / site | quote vs vision vs location |

---

## Tech, brands, STT phonetics

| Heard (STT) | Intended | Context |
|-------------|----------|---------|
| you es bee \| U S B \| usb | USB | cables, ports |
| ess ess dee \| S S D | SSD | storage |
| blue tooth \| bluetooth | Bluetooth | headphones, mouse |
| why fi \| wifi \| wi fi | Wi-Fi | network, router |
| docker \| docket | Docker | containers, DevOps |
| get hub \| git hub | GitHub | code, repo |
| get \| git | Git | version control |
| kafka \| cafka | Kafka | queues, backend |
| postgres \| post grass | PostgreSQL | database |
| sequel \| S Q L \| SQL | SQL | queries |
| react \| wrecked | React | UI (not “destroyed”) |
| no js \| node js | Node.js | backend |
| python \| pie thon | Python | language |
| java script | JavaScript | frontend |
| type script | TypeScript | typed JS |
| kubernetees \| kuber | Kubernetes | orchestration |
| engine x \| nginx | Nginx | web server |
| redis \| red is | Redis | cache |
| elastic search | Elasticsearch | search |
| mac book \| mack book | MacBook | Apple laptop |
| i phone \| eye phone | iPhone | phone |
| google \| goggle | Google | search, services |
| telegram | Telegram | messenger |
| discord | Discord | voice chat |
| prod \| production | production | deploy (not grocery) |
| dev \| develop | development | environment |
| staging \| stage in | staging | test environment |
| localhost \| local host | localhost | development |
| endpoint \| end point | endpoint | API |
| backend \| back end | backend | server |
| frontend \| front end | frontend | client |
| merge \| emerg | merge | Git |
| pull request \| P R | pull request | code review |
| A P I key \| api key | API key | integration |
| V P N | VPN | tunnel |
| D N S | DNS | domains |
| S S L | SSL/TLS | certificates |

---

## Health, home, daily life

| Heard | Intended | Context |
|-------|----------|---------|
| laying \| lieing | lying (in bed) | illness, rest — not “laying eggs” |
| fever \| temp | fever / temperature | body, not weather |
| charger \| charging | charger / charging | phone, laptop |
| mouse | mouse | computer vs animal |
| fridge \| refrigerator | refrigerator | kitchen |
| pharmacy \| farmacy | pharmacy | health (common STT typo) |

---

## Oral speech (usually keep in dialogue)

| Heard | Action |
|-------|--------|
| uh, um, like, you know | Reduce moderately |
| kinda, sorta, gonna, wanna | Keep in casual dialogue unless user wants formal |
| yeah, nah, ok | Keep tone |
| profanity | **Do not remove** without user request |

---

## Proper nouns (template — glossary_user.json)

| In source | Canonical | Notes |
|-----------|-----------|-------|
| *your name* | *canonical* | STT name errors |

---

## Whisper hallucinations — always delete

- “Subscribe to the channel”, “Thanks for watching”, “Like and subscribe”
- Subtitle credits, “Transcribed by…”, “Amara.org”
- Repeated phrase 3+ times ( `condition_on_previous_text` artifact)
- Random foreign-language inserts unrelated to speaker

---

## Chat instruction for AI

```text
Fix STT using prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md
and STT_HOMOPHONES.en.md.
Names from config/glossary_user.json.
Context-only fixes; no global replace.
```
