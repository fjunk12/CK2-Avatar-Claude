# ATLA Fixes builder: copies the affected files from Avatar - Four Nations Restored and applies anchored fixes.
import os, re, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
LOG = []
CRLF = {}
TXT = {}
def rd(rel):
    if rel in TXT: return TXT[rel]  # round 2 edits stack on round 1 edits
    t = open(os.path.join(SRC, rel), 'rb').read().decode('latin-1')
    CRLF[rel] = '\r\n' in t
    return t.replace('\r\n', '\n')
def wr(rel, t):
    TXT[rel] = t
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    if CRLF.get(rel): t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('latin-1'))
def sub1(t, old, new, what):
    n = t.count(old); assert n == 1, (what, n)
    LOG.append(what); return t.replace(old, new)
def block_end(t, i):
    # i points at the '{' ; return index after matching '}'
    d = 0
    for j in range(i, len(t)):
        if t[j] == '{': d += 1
        elif t[j] == '}':
            d -= 1
            if d == 0: return j + 1
    raise ValueError
def event_span(t, eid):
    m = re.search(r'\n\s*id\s*=\s*%s\s*\n' % re.escape(eid), t); assert m, eid
    s = t.rfind('_event = {', 0, m.start()); s = t.rfind('\n', 0, s) + 1
    return s, block_end(t, t.index('{', s))

# 1 Team Avatar: third party must be of the SENDER's dynasty and court (FROM), not the Avatar's (ROOT)
f = 'decisions/ATLA_avatar_decisions.txt'; t = rd(f)
t = sub1(t, '\t\t\tdynasty = ROOT\n\t\t\thost = { character = ROOT }', '\t\t\tdynasty = FROM # ATLA Fixes: was ROOT (the Avatar)\n\t\t\thost = { character = FROM } # ATLA Fixes: was ROOT (the Avatar)', 'send_to_avatar: candidate must be FROM dynasty/court')
wr(f, t)

# 2 Combustion bending is wiped by sub-bending grants (opposites): guard every grant
GR = re.compile(r'^(\s*)add_trait = (lightningbender|blueflames|smokebender|innerflame\w*)\s*$', re.M)
for f in ['events/ATLA_bending.txt', 'events/ATLA_bloodline_events.txt', 'events/ATLA_society_agni_kai.txt', 'events/ATLA_random_events.txt', 'events/ATLA_special.txt']:
    t = rd(f); n = len(GR.findall(t)); assert n, f
    allc = len(re.findall(r'add_trait = (?:lightningbender|blueflames|smokebender|innerflame\w*)\b', re.sub(r'#[^\n]*', '', t))); assert allc == n, (f, n, allc)
    t = GR.sub(lambda m: '%sif = { limit = { NOT = { trait = combustionbender } } add_trait = %s } # ATLA Fixes: would delete combustion bending' % (m.group(1), m.group(2)), t)
    LOG.append('%s: %d sub-bending grants guarded' % (f, n)); wr(f, t)

# 3 Spiritual journey: no longer blocked forever by HYW_0; Tui and La (Northern Water Tribe) added
f = 'decisions/ATLA_religious_decisions.txt'; t = rd(f)
s = t.index('spiritual_journey = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\t\t\t\t\thas_global_flag = HYW_0\n', '\t\t\t\t\t\t# has_global_flag = HYW_0 # ATLA Fixes: never cleared, blocked journeys for the rest of the game\n', 'spiritual_journey: HYW_0 block removed')
b = sub1(b, '\t\t\t\treligion = southern_spirituality\n', '\t\t\t\treligion = southern_spirituality\n\t\t\t\treligion = tui_and_la # ATLA Fixes: Northern Water Tribe\n', 'spiritual_journey: tui_and_la allowed')
t = t[:s] + b + t[e:]; wr(f, t)

# 4 Avatar system: reincarnation guards, no ownerless spawn province, single source of truth for the new Avatar
f = 'events/ATLA_avatar_system.txt'; t = rd(f)
s, e = event_span(t, 'NAE.002'); b = t[s:e]
b = sub1(b, '\ttrigger = {\n\t\tis_variable_equal = {', '\ttrigger = {\n\t\tNOT = { persistent_event_target:the_avatar = { is_alive = yes } } # ATLA Fixes: no second Avatar next to a living (canon) one\n\t\tis_variable_equal = {', 'NAE.002: only while no Avatar is alive')
t = t[:s] + b + t[e:]
s, e = event_span(t, 'NAE.004'); b = t[s:e]
b = sub1(b, '\tis_triggered_only = yes\n', '\tis_triggered_only = yes\n\t\n\ttrigger = { NOT = { persistent_event_target:the_avatar = { is_alive = yes } } } # ATLA Fixes\n', 'NAE.004: only while no Avatar is alive')
n = b.count('\t\t\t\trandom_province = {\n'); assert n == 4, n
b = b.replace('\t\t\t\trandom_province = {\n', '\t\t\t\trandom_province = {\n\t\t\t\t\tlimit = { has_owner = yes } # ATLA Fixes: never spawn the Avatar in an empty province\n')
LOG.append('NAE.004: spawn province must have an owner (4 elements)')
# drop the stale new_character block (the Avatar is created and set up in NAE.0041)
i = b.index('\t\tnew_character = {'); j = block_end(b, b.index('{', i))
gender = re.search(r'\t\t\ttrigger_switch = \{\n\t\t\t\ton_trigger = culture\n.*?\n\t\t\t\}\n', b[i:j], re.S).group(0)
b = b[:i] + '\t\t# ATLA Fixes: the new Avatar is created and set up in NAE.0041 (new_character here had no character to refer to)\n' + b[j:]
LOG.append('NAE.004: stale new_character block removed')
t = t[:s] + b + t[e:]
s, e = event_span(t, 'NAE.0041'); b = t[s:e]
b = sub1(b, '\t\t\tnarrative_event = { id = NAE.006 days = 3 }\n', '\t\t\tnarrative_event = { id = NAE.006 days = 3 }\n\t\t\t# ATLA Fixes: air nomad gender rule moved here from NAE.004\n' + gender, 'NAE.0041: air nomad gender rule')
t = t[:s] + b + t[e:]; wr(f, t)

# 5 Sozin's Comet (ATLAE.23): a Fire Lord holding e_fire_nation before HYW_15 (or the reverse) had no option
f = 'events/ATLA_hundred_year_war.txt'; t = rd(f)
s, e = event_span(t, 'ATLAE.23'); b = t[s:e]
old = '\t\t\tNOR = {\n\t\t\t\thas_landed_title = e_fire_nation\n\t\t\t\thas_global_flag = HYW_15\n\t\t\t}\n'
assert b.count(old) == 2, b.count(old)
b = b.replace(old, '\t\t\tNOT = { AND = { has_landed_title = e_fire_nation has_global_flag = HYW_15 } } # ATLA Fixes: was NOR, left some Fire Lords with no option\n')
LOG.append('ATLAE.23: options A/B now cover every case option C does not')
b = sub1(b, '\t\t\tadd_character_modifier = { name = power_of_the_comet duration = 4000 }\n\t\t\tadd_character_modifier = { name = agni_blessing duration = -1 }\n\t\t\tcharacter_event = { id = ATLAE.27 }',
         '\t\t\tif = { # ATLA Fixes: only firebenders draw power from the comet\n\t\t\t\tlimit = { trait = firebender }\n\t\t\t\tadd_character_modifier = { name = power_of_the_comet duration = 4000 }\n\t\t\t\tadd_character_modifier = { name = agni_blessing duration = -1 }\n\t\t\t}\n\t\t\tcharacter_event = { id = ATLAE.27 }', 'ATLAE.23: comet buff for firebenders only')
t = t[:s] + b + t[e:]; wr(f, t)

# 6 Water tribes can convert tribal holdings to castles; water vassals answer the call to arms
f = 'decisions/settlement_decisions.txt'; t = rd(f)
s = t.index('convert_tribal_to_castle = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\t\tis_feudal = yes\n', '\t\t\tOR = { is_feudal = yes government = water_tribe_government } # ATLA Fixes: water tribes can build castles but could not convert\n', 'convert_tribal_to_castle: water tribe government allowed')
t = t[:s] + b + t[e:]; wr(f, t)
f = 'common/governments/tribal_governments.txt'; t = rd(f)
s = t.index('\twater_tribe_government = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\tvassal_call_to_arms = {\n\t\t\ttribal_government\n\t\t}', '\t\tvassal_call_to_arms = {\n\t\t\ttribal_government\n\t\t\twater_tribe_government # ATLA Fixes: GitHub #125, water vassals ignored rally demands\n\t\t}', 'water_tribe_government: can call water vassals to arms')
t = t[:s] + b + t[e:]; wr(f, t)

# 7 Warrior lodge duel called a non-existent event
f = 'decisions/hf_warrior_lodge_decisions.txt'; t = rd(f)
t = sub1(t, 'character_event = { id = HF.10095 days = 1 }', 'character_event = { id = HFP.10095 days = 1 } # ATLA Fixes: HF.10095 does not exist', 'warrior lodge duel: HF.10095 -> HFP.10095')
wr(f, t)

# 8 Air nomad CBs: law check from the ruler's primary title (as the mod's own events do), not 'realm'
f = 'common/cb_types/03_cb_types_ATLA.txt'; t = rd(f)
n = len(re.findall(r'\n\t+realm = \{', t)); assert n == 5, n
t = re.sub(r'\n(\t+)realm = \{', lambda m: '\n%sprimary_title = { # ATLA Fixes: was realm' % m.group(1), t)
LOG.append('air CBs: %d law checks moved to primary_title' % n); wr(f, t)

# 9 Avatar help events: new_character effects hidden from tooltips (character does not exist while hovering)
f = 'events/ATLA_avatar_interfere_events.txt'; t = rd(f)
L = t.split('\n'); idxs = [i for i, l in enumerate(L) if re.match(r'^\s*new_character = \{\s*$', l)]
count = 0
for i in reversed(idxs):
    pre = '\n'.join(L[max(0, i - 8):i])
    if not re.search(r'spawn_great_commander_effect = yes|create_random_\w+ = \{|create_character = \{', pre): continue
    off = sum(len(x) + 1 for x in L[:i]); k = t.index('{', off); end = block_end(t, k)
    ind = re.match(r'^(\s*)', L[i]).group(1)
    blk = t[off:end]
    t = t[:off] + ind + 'hidden_tooltip = { # ATLA Fixes: hovering this option could crash (no character exists yet)\n' + blk + '\n' + ind + '}' + t[end:]
    L = t.split('\n'); count += 1
LOG.append('Avatar help events: %d new_character tooltips hidden' % count); wr(f, t)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'round2.py')).read())
print('\n'.join(LOG))
