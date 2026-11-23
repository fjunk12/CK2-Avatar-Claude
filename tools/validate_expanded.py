# Static checks for ATLA Expanded: brace balance, undefined scripted effects/triggers, missing events,
# missing event modifiers, flags set but never checked (and the reverse), casus belli references, missing loc keys.
# Usage: python3 tools/validate_expanded.py "ATLA Expanded"
import re, glob, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else 'ATLA Expanded'
os.chdir(ROOT)
txt = {f: open(f, encoding='cp1252').read() for f in glob.glob('**/*.txt', recursive=True)}
strip = lambda s: re.sub(r'#[^\n]*', '', s)
ok = True
def report(name, items):
    global ok
    items = sorted(items)
    print('%-28s %s' % (name + ':', items if items else 'ok'))
    if items: ok = False
report('brace imbalance', ['%s (%+d)' % (f, strip(s).count('{') - strip(s).count('}')) for f, s in txt.items() if strip(s).count('{') != strip(s).count('}')])
allt = strip('\n'.join(txt.values()))
part = lambda key: strip(''.join(v for k, v in txt.items() if key in k))
defs = set(re.findall(r'^(atx_\w+_(?:effect|trigger))\s*=\s*\{', part('scripted_'), re.M))
used = set(re.findall(r'\b(atx_\w+_(?:effect|trigger))\s*=\s*(?:yes|no)', allt))
report('undefined scripted', used - defs)
evs = set(re.findall(r'id\s*=\s*(atlaexp\.\d+)\s*\n', part('events')))
refs = set(re.findall(r'id\s*=\s*(atlaexp\.\d+)\s*(?:days|\}|random)', allt)) | set(re.findall(r'^\s*(?:\d+\s*=\s*)?(atlaexp\.\d+)\s*$', allt, re.M))
report('missing events', refs - evs)
mods = set(re.findall(r'^(atx_\w+)\s*=\s*\{', part('event_modifiers'), re.M))
usedm = set(re.findall(r'(?:has_character_modifier|remove_character_modifier|has_province_modifier|remove_province_modifier)\s*=\s*(atx_\w+)', allt))
usedm |= set(re.findall(r'add_(?:character|province)_modifier\s*=\s*\{\s*(?:name|modifier)\s*=\s*(atx_\w+)', allt))
report('missing modifiers', usedm - mods)
setf = set(re.findall(r'set_(?:global|character)_flag\s*=\s*(atx_\w+)', allt))
chk = set(re.findall(r'(?:has_global_flag|has_character_flag|clr_global_flag|clr_character_flag)\s*=\s*(atx_\w+)', allt)) | set(re.findall(r'flag\s*=\s*(atx_\w+)', allt))
report('flags checked, never set', chk - setf)
report('flags set, never checked', setf - chk)
cbs = set(re.findall(r'^(atx_cb_\w+)\s*=\s*\{', part('cb_types'), re.M))
report('unknown casus belli', set(re.findall(r'(?:casus_belli|using_cb)\s*=\s*(atx_\w+)', allt)) - cbs)
loc = set()
for f in glob.glob('localisation/*.csv'):
    for l in open(f, encoding='cp1252').read().splitlines():
        p = l.split(';')
        if len(p) > 1: loc.add(p[0])
        if ';' in l and len(p) < 3: print('suspicious loc line:', l[:80])
keys = set(re.findall(r'(?:text|name|desc|war_name)\s*=\s*([A-Za-z_][\w.]*)', allt))
keys |= mods | {m + '_desc' for m in mods}
for f, s in txt.items():
    if f.startswith('decisions'):
        for d in re.findall(r'^\t(atx_\w+)\s*=\s*\{', strip(s), re.M): keys |= {d, d + '_desc'}
targets = set(re.findall(r'save_(?:persistent_)?event_target(?:_as)?\s*=\s*(?:\{\s*name\s*=\s*)?(\w+)', allt))
report('missing loc keys', {k for k in keys if k not in loc and k not in targets and re.match(r'(atx|atlaexp|CB_|WAR_)', k)})
sys.exit(0 if ok else 1)
