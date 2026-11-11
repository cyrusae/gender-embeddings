# History map: monorepo to standalone repo

This repo was made from the monorepo `gender` (`/Users/watcher/GitHere/gender`) with
`git subtree split -P embeddings` (monorepo branch `embeddings-split`), then `git pull` into a fresh
repo. The history of `embeddings/` is kept commit for commit, so each old commit has a new
hash. The two sides were paired by order (topological, oldest first). For every pair, the
`embeddings/` tree hash in the monorepo commit equals the root tree hash of the new commit, so
the pairing is verified by content, not by order alone.

Commits added after the split (scaffolding, PROVENANCE, README, paths) are not in the table below.

Prereg hashes quoted in `docs/*prereg*.md` (monorepo hash to new hash):

- `1be8c7a` -> `1147fcb`  C1 analysis script (before first run)
- `20a066e` -> `d9e6980`  Gender ValNorm Addendum B runner (before first run)
- `3dbc629` -> `f9e155e`  Word-pair mechanism scoring script (before any Part B score)
- `48f47a6` -> `1b4f578`  Crime probe ADOPTED; lists frozen; scoring script committed before any
- `52cc9ed` -> `e593a25`  Generic-masculine prereg ADOPTED; pairs frozen; scoring script before 
- `64b4b4e` -> `e537939`  Gender ValNorm Omrani-arm analysis script (before results)
- `a40cd18` -> `bfd71b0`  Zhou zero-point scoring script (before any score)
- `b9cd402` -> `8f6998d`  Gender ValNorm MUSE-arm runner (before first run)
- `cd7693c` -> `110e7f9`  Zhou word-pair rerun: reconstruction, fixed, feminine cues; Z17 update
- `fc382f4` -> `7c01865`  C1 runner generalised to French (Addendum A), before the French run

Full mapping (monorepo hash, new hash, subject):

| monorepo | standalone | subject |
|---|---|---|
| `98cac54d891be0cf9d5ee12382e8fceec8ab0d25` | `a7ecd1128573a3d62483fc9c930367898acb9008` | Reorganise for navigation: preregs grouped by study (base/followups/instruct), design PDF moved under docs/design/base, README study map, embeddings/ study scaffold |
| `9e1349689b31ed30b3e423b1229abcd2df889162` | `eeff229b43f72937d5fe79c57c45625d5ce39e06` | embeddings: note cloned GG_Disentangling (Omrani Sabbaghi & Caliskan 2022) |
| `b792a0441577c054e853c3bb9fa2e54b03e016b4` | `ac4b1c5ef5ebcd85063081416e372fb5311681a3` | embeddings: fetch script for MUSE + fastText CC vectors (to the store); orientation notes on both upstream repos |
| `bd321f5434847e266425a9bf393a1832795987da` | `d8248a61acdab8d4a82107e11bc77afab49b2620` | embeddings: Spanish rerun of the GG_Disentangling notebook reproduces upstream outputs |
| `086ff18d6feda9ecbd21d1a7c7bfa8f34f6c0588` | `7373da9a59f47ff74ddfdbb5b8ae042f724421f3` | repro README: note discarded Results files |
| `885cfe7dc30c09e57bd23456ed24f292aa8d45c2` | `64a506f8cb96617ac2cbe9a89d626b269032adf3` | embeddings: held-out check script for the GG_Disentangling SC-GG-WEAT (exploratory) |
| `ee40de8a4ce24e79a2db7e45b1b2abf495bdee95` | `7d559fb2335292cf1653afc3c9834a4cb063b78e` | embeddings: rebuild Zhou et al. Spanish Shift Ori; Table 1 statistic reproduces (3.6918; 0.3087 vs 0.3090), p-value doesn't |
| `c83696c17977936c8c8621f7a11d540a3ae7f807` | `4f33710c93fad094da05d5d811f9ace09f6ce68c` | gg_heldout: exclude held-out words that are also training words (their lists have duplicates); score accuracy on real rows only |
| `e4d4f222de16ae663f415acf0eb6b250f20e0aac` | `5956d91e6d02108a294e01b509e5096ff4323033` | embeddings: consolidated upstream-issues log (12 Omrani, 8 Zhou) + rule to log findings there |
| `45fedb5f4d72f0d18d1f9f31cf922be473f1bb8e` | `e6d270a5c3066eda1293f99674043543ee031af4` | upstream issues: ValNorm coverage + Unicode NFD bug verified; contradictory/duplicate training labels (O13–O16) |
| `d334187e8e2fd56273975e864c41790e96289394` | `0d8e9d857a335dc116210c830a5b499a9aafdcec` | Held-out check (14 iter): Omrani SC-GG-WEAT effect generalises to unseen nouns; padded accuracy bug low impact |
| `cbac67ffb15dcaf0ca869ba5b2966ee1686f6805` | `ddbd08f2f5c19d0068124975e74d1decbab7f20c` | gg_heldout: --minfix mode (dedup lists, drop both-gender words, unpadded accuracy, NFC ValNorm) — bugs fixed, method unchanged |
| `16569e6d01a6af04be19ecef8cb1f2ef8c8b48b4` | `a966aff5393cfcadd61b3a879f3e3d797bc0c4c7` | embeddings: label audit vs Wiktionary + ending-exception test (Spanish, both papers) |
| `bec5ec91b6d7d8392ef4fbbbe9d3f6ee7c57a20c` | `bf8eac6d47b6691ecdc5c43010b7cb7874daa7a8` | Held-out check at 28 iterations: same conclusion |
| `9f22f0bbc033b349d50b02c628e6e1f7a2b656cc` | `2d2db35a9a154e980d6cf70da309abb6a3bf2964` | Minimal-fix rerun (14 iter): bugs don't change Omrani's GG-WEAT/SC-GG-WEAT conclusions; ValNorm 0.796/0.833 |
| `99b3461ea108c204e2c92da8fc0610090b57f01d` | `8563d6f0145de4ec7d87cc469484330273adfbfe` | Minimal-fix rerun at 28 iterations |
| `d88b8353aa4a23e75dffd1f97721fee28ab1b9a7` | `8702e28fa409b0c5258fa9741de7da6d25e4cb01` | embeddings: C1 pre-registration DRAFT (Zhou inanimate score after Zhou mitigation) |
| `6a8f0a2da0e5ce3ea1fae79599cc3fa58e4951de` | `c3460e16a70fce9091a6b9b799c793b6075f573b` | C1 prereg ADOPTED (PI); test-noun list frozen (2,459 at 50k / 8,126 at 200k); embeddings decisions log |
| `dad44699d64b6c5eda6bede95ed4a2f23ee90f09` | `00efc40e5c2565f124b348a1c767015495af3d3f` | Zhou De-Align/Hybrid Ori rebuilt: Hybrid=Shift by construction under orthogonal alignment; MWEAT post-mitigation p-values are tie artefacts (Z10, Z11) |
| `1be8c7a1b902fb55862f8f2110a7d3ff78ab9884` | `1147fcb971a0c7214d8676bb8c1da58dee80ea80` | C1 analysis script (before first run) |
| `973c3a142414d9ee1b6455da0310329db186902c` | `c9a238b82816c14ec527bf9ff71b34ebee9d97cf` | C1 results: inanimate-noun gender gap survives all Zhou mitigations (8/8); Z12 |
| `bf5be7ce628f2e7648db1a7eb076d3527ec37f77` | `2c00c851a7fd922993a1326ad838829e9d7c6f2e` | Gender ValNorm prior-art check (English done by Lewis & Lupyan 2020, Valentini et al. 2023; not in gendered languages) |
| `ce27a31320470b67de93a3baa0d3edd82ca92100` | `3c5af6d0bb277401d28ced43904d86f4bd07af46` | Gender ValNorm English pilot: r = 0.584 on MUSE Wikipedia fastText (Lewis & Lupyan: 0.59), 0.639 on Common Crawl |
| `1ab9c7c8f6e4ee745beb09e02d273a1f19f4acd9` | `cf4438efb2a7e7c8c3add6ad1335614a30b054a2` | Zhou French Table 1: rebuild matches the notebook's saved output (0.0649), not Table 1 (0.2446); Z13; Shift script parametrised by language and reports tie share; Zhou downstream-reuse scan |
| `cd4aee642b55337533ad13d3a6bb925d70afb675` | `3ae30847ac651a383c4e5d9a43665cb65747a35c` | Gender ValNorm (Spanish inanimate nouns) prereg DRAFT |
| `345d57936de01395e33c917dab22196f5d003d91` | `4145a06150d1f66f535a4f35a3759911e54b7473` | Gender ValNorm prereg ADOPTED (PI): 50k/200k, Omrani erasure arm; French lexicon next |
| `8e08819d7c1a2a05af123fea454c079804ca8885` | `d0820c0c8bc4f83fed58a7dd2fcd228124f8ad2a` | French addenda to C1 and gender-ValNorm preregs; French C1 noun list frozen (3,505 at 50k / 8,446 at 200k) |
| `fc382f49c39690d9e8ec493982bc3d8a89000d3c` | `7c018659f5a4124842f5ff63c51c2ace0a5c83a0` | C1 runner generalised to French (Addendum A), before the French run |
| `61a301d551235680e85a6343a3720fafce94e60a` | `4bc310a425bcb0ac12032a9fb5ee559369fd7ec9` | c1_run: fix syntax slip from generalisation (before any French run) |
| `798ad3d7d68e9ecaf4b85e787b679dbc483bf929` | `cc8afc31291fd6f879ca60d163e08b8a1933a8a0` | c1_run: per-noun output columns per language (+concept_en, zipf for gender ValNorm) |
| `b9d854d082bc3fa620de4e09d49dbecfb2d735a7` | `3070db510b67a9a9a74cc49eb79252385b55b975` | French C1 results: 8/8 survives; English-attribute gap only in suffix-less nouns |
| `b9cd4024c6b0a761d334b92037a819e786bb1071` | `8f6998d5ec44d5957fe5b16cd76b1c82e069f33d` | Gender ValNorm MUSE-arm runner (before first run) |
| `000a3a41ba43c0b12f11e0cb95155fdd3e418daf` | `ce221ef51e7c39b9a81770d562b613548cb22f84` | Gender ValNorm results (MUSE arms, ES+FR): human-rated component present, removed/reduced by Zhou mitigation; grammatical part survives |
| `f137d01b71dd7131e199b97628ca02c37e899ffa` | `8085c48c7db56185ae286355d8942ceb6ce8b03c` | Omrani erasure arm: vector dump driver for gender ValNorm (before run) |
| `64b4b4e61ce4be64f1ec8b4387c32aa091493e06` | `e537939f25601137609e34738ffc8d5b64e50f3a` | Gender ValNorm Omrani-arm analysis script (before results) |
| `58dc2c6f2f16073b31e08f40d03452eeb637aff2` | `d1af7bd9f44a32b3877f30e7cfb28f9870826d85` | Z14: Zhou Shift Ori MWEAT drop is an algebraic identity (post-Shift stat = original stat with attribute axis' ds-part deleted, exact) |
| `63c581244d256c4bd27c536975bb8af94b9ab63a` | `3b316b1b9f9359dd8cfe62ef466d7361ae3cfffe` | Gender ValNorm Addendum B (PI): ds-orthogonal yardstick, frozen before scoring |
| `20a066ee3d544d4ef1f5dc4e68838089b4957016` | `d9e69801ffeeec18c12a65d094bdc7a834c5d40e` | Gender ValNorm Addendum B runner (before first run) |
| `1be6bdc6a734241dac3625652c7734c598b40f4e` | `93d0f6dc1a9744db5571f786382a07ee99402ef4` | Gender ValNorm Addendum B results: off-axis stereotype signal only with English yardstick; Hybrid's removal comes from hard-debiased English |
| `d178ccf9bf656be10e1ac41b9de43649e2719aae` | `5d4a35d26f2bc5e5626aff9ca0ee05cfebcf92f0` | Zhou Shift: cell/line map, derivation of the MWEAT identity (with sign condition), Z15; withdraw 'as implemented' claim (it's our reconstruction) |
| `4de4b19fc72340b194cf8f791b949a65a2c7f9c5` | `821952dc9066d6e4d472c98c391278d4525cfeb2` | Gender ValNorm Addendum C: fixed English yardstick for Hybrid (frozen before scoring) |
| `226fcf702719bba61449bfecf41a47b91ae587f8` | `6225cdbddd004745a0133d3c48d5f36f4bb7ffba` | gvalnorm_orth: --fixed-en (Addendum C), before run |
| `edd85f91d94d6a676aee35ac1838f614675eaade` | `7180c612782cb1b9d18c9f79bf9f225e16a3bff9` | Gender ValNorm Addendum C results: Hybrid's off-axis removal persists with a fixed English yardstick |
| `00aac39d095f80e28802df4f0b3feee091437877` | `5c8d1d8f4a6e93e73f72d13ca9c618a3b45baff2` | Zhou identity doc: blind-check refinements (same-sign branch, raw-dot condition, attribute words shifted via defs); Z16 |
| `8983750c0f6ec579e77e9f99de3dbffd4088b961` | `372fb8456376d9ffa5a32d65164374bddc964a17` | upstream-issues: severity column; Z-entries updated with blind-check refinements; table order fixed |
| `951ee05179adf6edbc0a7894b564c465bad2dfc2` | `cd1d7936e6560a06a15751637f779faf2a11b9c4` | Gender ValNorm Omrani arm, Spanish: erasure cuts raw gap 72%, stereotype component unchanged in raw units |
| `b9842048b562c58851fd985e516a1ecf2c59daf9` | `77de695db443cde1e194967e7325ae33925a2105` | Gemini blind check folded in: Zhou original MWEAT p=0 is also guaranteed (observed stat = permutation max); LDA crashed in their notebook (Z1) |
| `9eaa374eb2dd5effd34da12c5ff21d4b9323977f` | `68705e4f5e958b9b28f57aa0140e5ce6312d83ec` | Zhou zero-point prereg DRAFT + candidate reference lists (epicene/common/inanimate, ES+FR, for PI review); correct 'not the asymmetry' wording |
| `87a48d1e1e7cb19cb5713b033e6eeefcaf340d63` | `40b0c0e051e758ecc91c1d731302ab9152b4b056` | Gender ValNorm Omrani arm, French: grammatical gap removed (-95% raw), stereotype component unchanged |
| `a6d3b49323aa3ca45e5f54aadc79106e02e25c3b` | `71ec1a865b1ef8df14c2519464977b30855b70fd` | Zero-point reference pools: persons only, WordNet person-majority rule (licuado 'smoothie' was a person via WordNet's first sense) |
| `f9c2aae6291658a5914687e60b588a29fa9c04eb` | `9f629d4c9d62eebb8af297cf4f386716d0bd16eb` | Zero-point: PI's Spanish epicene additions (separate file; merge after PI review) |
| `ad821858530b66e341869c2870f454f2fd817b91` | `b37a38ee5b2116e4f06ed29c2535d23ae71dd7a1` | fix note |
| `e436d53074728e85c9ffce500ed5db00906ae876` | `1a44e9d1693ac581526077fb2544904480c1aa35` | Zero-point draft: strict/broad tiers; PI additions updated (eminencia, bebé, broad-tier words) |
| `858f456a729429303bf88d35d1297d231731565b` | `306f0d867c228e91dd4ca84d0e66941e553473a7` | Zero-point draft: floor 15 + leave-one-out rule (PI) |
| `607b5a8583f8ba9e2aadd3020aee01690f84811a` | `9bf7db529f3fb31058662ab2204f90810abe3fe6` | Zero-point: PI review files; French v1 (English-only exclusions reinstated); sensitivity checks S1-S7 in draft |
| `9d0ce646a315429e5be0cbb04930057fa905d783` | `4bbd80d1346dc35865a49897c5ed902df77239e2` | Zero-point: PI decisions on loanwords (ES v1: punk/alien/gurú/coach/sheriff reinstated; FR shérif in, barman/gangster/imam/apache out) |
| `3282ec5af03c2e04daa7c84a038a38ca4851a4c1` | `04e8e5a569d12c070c325aec6b8b86e1b523b64c` | Zero-point: PI additions aristócrata (common), élite and espíritu (broad), gánster not usable; hada confirmed epicene |
| `ebd47b112dc5331e4db7df1d91b45cab4c16db71` | `2757017b9740c61bfc23e7ff1fbb511ee13a0299` | Zhou zero-point prereg ADOPTED; reference lists frozen (ES/FR) |
| `a40cd186f7f3788afeb05de494814ec2df744223` | `bfd71b05555dd4ab757ea900ae47268febf958bb` | Zhou zero-point scoring script (before any score) |
| `fd9e05c14e20527bd0f79179ac32d9fc29a6e7ba` | `2a176a9eeb74e27af7dd138e0e91848b90bc82c2` | Zhou zero-point results: FR asymmetry survives, ES inconclusive |
| `b98cf413931a15d3c198b80d3f9af40cb30dd731` | `49422e6b4d5c24f6e6b44452a55765cbd4713ffc` | Crime-noun probe: DRAFT prereg + candidate lists for PI review |
| `0eeb48ddaea1a8066028401f7ae574e06327c91f` | `d293f2f504e9cd632d0e8f6ea6d5aa71c588ca01` | Crime probe draft: act-dominant words as a separate sensitivity set (PI) |
| `48f47a65a0d199318ca917f5033057a4951a46e8` | `1b4f5781e68148fca1ccccbd8f8883f6733c6762` | Crime probe ADOPTED; lists frozen; scoring script committed before any score |
| `a7906a50e3a838cc95f5febce4aa752b773719ef` | `00394934e523b80d072e85f9590a451314628bee` | Crime probe results: ES male-leaning, FR borderline, not crime-specific |
| `442b82723f4ae032d1073d8163f830b48a47e92e` | `1953753e28383ba197093348a48950a264f25f13` | Zhou Figs 1-2 redrawn: as published and with corrected inputs, all 58 pairs, epicene zero point (exploratory) |
| `49899ce4f8c50a7f60c51fc666637caccbad5c0c` | `505fc0bfb48c6154908232fb7c18fc7b8a0bdd0e` | Generic-masculine prereg DRAFT (Zhou skew: singular vs plural shrink) |
| `c0b160bed92f7513f69894dd94847c7bed9e1805` | `650414c82d4e5787592e06ff70901dae436000c1` | Z17 (PI): Zhou Table 2 word-pair translation uses only masculine/invariant adjective cues; MRR misses dropped; ES Hybrid cell interrupted |
| `d5599b6402fc96661667d2fe247f026748ace3ac` | `80aa36906839e451a92f08fcab934e77e6b247ed` | Z16: quantify cell-274 FR offset bug; our rebuild unaffected |
| `1b30ae9e401fc0a6b413ad145d19fd7e40c89c7a` | `930154442473d8ee8d1cf40c84d253c802161db6` | Zhou Table 2 word-pair test: reconstruction / fixed / with feminine cues (script before scores) |
| `cd7693cc816d2af14ce5d0766a9975c879f12f29` | `110e7f9bc72c576da7226b132aa36da2172a0630` | Zhou word-pair rerun: reconstruction, fixed, feminine cues; Z17 updated |
| `6af6a7cdfcee53b7944b1f99d3349dc084f35178` | `2469a145411cd8f223d13bb2a2a95169c8e3ef24` | Word-pair intervals + mechanism prereg DRAFT |
| `41dee7e7ebf5daab018d6359dbd76c312fdc170e` | `cc6f06d1558dd8ac3af700dcd34ea17664c8fa43` | Word-pair prereg: PI decisions (clean list primary, FR descriptive) |
| `5dacfd11d5d56e0972f180a3299ee7cc280de490` | `65a00ada837a7639b3f6e94aee3484d3d6437f05` | Occupation-to-labor-statistics mapping v0 for PI review (BLS 2025, Eurostat 2-digit 2024) |
| `3bc23f062d78058e6afcab63786b78a414522307` | `e00f2b16f45707700469d98b192cf1cba37d48e2` | Occupation mapping v1 (PI: generic worker/employee = workforce share; jefe = all managers); homograph predictor |
| `ce61bfc05f6b40780740a5c38c997ab4720df344` | `9b1cfdd7f35da895793d73a1930aa58f5662c2f7` | Occupation mapping v1 file (PI changes applied) |
| `bdd830fe4b563a9c2b417332bc9b13168c0db96b` | `6151e1e8a7c1133d6ddd2b4ed8d447bacc386efe` | Word-pair prereg: stereotype sources fixed |
| `e928283c624321a7128beeed1553f1d311ce940e` | `2003a1aea22a45f89c0207c196c534e433417bae` | Word-pair mechanism prereg ADOPTED; mapping v1 frozen |
| `3dbc629fe57589ee13b7afa082aada5530fc6f2e` | `f9e155ebe637d9ddb178dcbc7c40e2296b0a82cc` | Word-pair mechanism scoring script (before any Part B score) |
| `2ba5cb81a775509a23b7eacb4f574e5d6997347a` | `4c5f3c9ff0532b0c62b1c02156d402c8a63ab56c` | Word-pair mechanism results recorded |
| `9e92de211018ce6d6fc210e4456d1a7ae3dfd843` | `1b77f5abc3f408b807e5f7009520ae4d6abd7e3e` | Generic-masculine prereg: clean list primary, ES plural rule fix, coverage counts (ES 43/54, FR 16/22) |
| `74f0408584bb20654f0c31b251f8f2c81f8594fb` | `11d98d17c794552ec5a5f56e4e8058ec8690d7e3` | Generic-masculine: plural list v0 + French extra pairs by rule, for PI review |
| `8e64c5fa10c9e161034f33f7fa511589242a9488` | `1ca8a8a9826f4bebefee27248a469a6f65c82d4a` | Generic-masculine prereg: relative margin, French extras (travailleur dropped) |
| `52cc9ed0c86b92a5b9ac87a11f4b26402ae5173c` | `e593a25612e7722bb28bba6c6fe32032d1f5af43` | Generic-masculine prereg ADOPTED; pairs frozen; scoring script before any score |
| `6b0e258a9e1abd9b145a875d593be247c847d58a` | `166b9cd991e69267d689e9992b332891c78ebd62` | Generic-masculine results recorded |
| `04212900cd9070716ad44f7397922cdba913ba10` | `9e717b81eb09394c652e79ae806cdeba25dc9bf7` | Zhou §4.3 translation + §4.4 correlation check script (before scores) |
| `ce051987c9ddc1f954f847b77e5c05f519f03803` | `bcba630362fb09a6cbe3516e59e5cb7a57413e49` | Zhou §4.3/§4.4 results; Z18 (candidate-set artefact in Table 2 translation) |
| `407c643ffe03e4171c94f8bfb02a12c64d58106e` | `b62ff96035166a8e82d09afa552f4ded46e4c796` | Zhou summary for write-up; draft issue list for authors (not sent) |
| `39ef36a2d94529baac65768673829bf7fb3c3771` | `6f4d146d3cb27a11f87482306f4998f008ca5fd1` | Plain-language summary of inanimate-noun findings |
