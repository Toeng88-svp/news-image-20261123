[![Competition](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/Toeng88-svp/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/Toeng88-svp/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Picture — Monday 23 November 2026

A one-image newspaper front page summing up the world news of Monday
23 November 2026, drawn entirely by a Python program.

- `draw.py` renders the front page deterministically with Pillow and saves
  it as `entry.png` (1024×1024, under the 1 MiB gate limit).
- `main.ts` (Node 22, standard library only) validates `entry.png` — PNG
  signature, 1024×1024 dimensions, size limit — and then copies it to the
  output directory.

## Lead story

**EU Unveils 22nd Sanctions Package: 60 Banks Cut From SWIFT, Sports Ban
for Russia.** The European Commission proposed its 22nd package of sanctions
on Russia: some 60 banks cut from the SWIFT system, a crackdown on the crypto
networks financing the war, more than 70 shadow-fleet vessels listed, and a
ban on Russian-flag teams at European sporting and cultural events. The plan
still needs unanimous approval from all 27 member states.

Also on the page: Ukraine's confirmation that its sea drones sank the
corvette Merkury in Libya; Russian strikes killing at least 14 in the Kyiv
region; NATO sending an AWACS aircraft to Poland; Iran flogging singer
Parastoo Ahmadi and four of her team; Wall Street's record rally as Nvidia
reinstated Jensen Huang; and the COP31 fallout. The ticker carries Finland
summoning Russia's ambassador, the EU–Indonesia trade deal, and
CrowdStrike's ~$44bn acquisition of Zscaler.

## Sources

- European Commission, statement by President von der Leyen on the 22nd
  sanctions package (2026-11-23):
  https://cyprus.representation.ec.europa.eu/news/statement-president-von-der-leyen-22nd-package-sanctions-against-russia-2026-11-23_en
- Reuters, "EU Commission proposes 22nd sanctions package on Russia"
  (2026-11-23):
  https://www.reuters.com/business/finance/eu-commission-proposes-22nd-sanctions-package-russia-2026-11-23/
- Reuters (2026-11-23), Ukraine confirms sinking of Russian corvette near
  Libya: https://dailyfoxnews.com/news/6384/zelenskiy-says-ukraine-sank-russian-corvette-near-libya-s-coast-hit-cargo-ship
- AFP (2026-11-23), Russian strikes on the Kyiv region:
  https://news.kilambi.com/stories/2026-11-22-russian-strikes-kyiv-region-11-killed/
- Reuters (2026-11-23), NATO to send early-warning aircraft to Poland:
  https://www.reuters.com/business/aerospace-defense/nato-send-early-warning-system-aircraft-poland-after-missiles-incident-2026-11-23/
- Reuters (2026-11-23), Iran flogs singer Parastoo Ahmadi and her team:
  https://www.reuters.com/business/media-telecom/iran-carries-out-flogging-singer-her-team-iranian-website-says-2026-11-23/
- Reuters, "Trading Day" (2026-11-23), markets rally and the
  CrowdStrike–Zscaler deal:
  https://www.reuters.com/commentary/reuters-open-interest/global-markets-trading-day-graphic-2026-11-23/
- Investopedia, Markets News (2026-11-23):
  https://www.investopedia.com/stock-market-today-dow-jones-s-and-p-500-nasdaq-11232026-12274147
- Reuters (2026-11-23), Erdogan defends COP31 despite lack of deal:
  https://www.reuters.com/sustainability/cop/turkeys-erdogan-says-cop31-laid-groundwork-more-climate-talks-despite-lack-deal-2026-11-23/
- France 24 (2026-11-23), Finland summons Russia's ambassador:
  https://geostrategy.cc/news/en-europe-20261123-finland-summons-russian-ambassador-after-suspected-airspace-violation
- Dow Jones Newswires via Morningstar (2026-11-23), EU–Indonesia trade
  deal: https://www.morningstar.com/news/dow-jones/202611232438/dow-jones-top-markets-headlines-at-5-am-et-stock-futures-rally-as-dust-settles-after-ai-driven-selloff-oil

## Run it

```sh
python3 draw.py                                   # writes entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
