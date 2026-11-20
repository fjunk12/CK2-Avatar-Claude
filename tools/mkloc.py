# Builds localisation/0000_atlafix.csv for ATLA Fixes.
# ALIAS: missing key -> existing key whose text it should show (typos / key mismatches in the base mod)
# NEW: text written for keys that have none. OVERRIDE: keys whose existing text is wrong (needs to load first).
import os, sys
M, OUT = sys.argv[1], sys.argv[2]
loc = {}
for f in sorted(os.listdir(os.path.join(M, 'localisation'))):
    if f.endswith('.csv'):
        for l in open(os.path.join(M, 'localisation', f), 'rb').read().decode('cp1252', 'replace').splitlines():
            p = l.split(';')
            if len(p) > 1 and p[0] and not p[0].startswith('#'): loc.setdefault(p[0].strip(), p[1])
ALIAS = {
    'BAR.8.A': 'BAR.8.D', 'MANDATE_PEASANT_REVOLT': 'MANDATE_PEASENT_REVOLT', 'HYW_ally_earth_kingdom': 'HTW_ally_earth_kingdom',
    'avatar_end_withdrawal': 'avatar_end_withdraw', 'avatar_end_withdrawal_desc': 'avatar_end_withdraw_desc',
    'improve_bending_event_accept': 'improve_bending_letter_event_accept', 'path_of_spirit_tooltip': 'path_of_spirits_tooltip',
    'sell_avatar_event_desc': 'event_sell_avatar_desc', 'PETS.RARE.TT': 'PETS_RARE_TT', 'fervor_cd_tt': 'racing_fervor_cd_tt',
    'NAE.517.D': 'NAE.517,D', 'NAE.610.OPTB': 'NAE.610.OPB', 'NAE.613.OPT': 'NAE.613.OPTA', 'NAE.315.OPTA': 'NAE.315.OPT',
    'agni_kai_refused_dishonor': 'agni_kai_refused_dishonour', 'duel_refused_dishonor': 'duel_refused_dishonour',
    'EVTOPTC_EK_66a': 'EVTOPTB_EK_64', 'EVTOPTC_EK_66b': 'EVTOPTA_EK_64', 'EVTOPTC_EK_66c': 'EVTOPTC_EK_64',
    'imperial_ambitions_3_desc': 'EVTDESCIMP.5',
}
for n in (1, 2, 3, 4):
    for x in ('D', 'OPTA', 'OPTB', 'OPTC', 'OPTD'):
        ALIAS['PETS.%d.%s' % (n, x)] = 'PET.%d.%s' % (n, x)
for k in ('EVTTOOLTIPBduel.1', 'EVTTOOLTIPDduel.1', 'EVTTOOLTIPBduel.2', 'EVTTOOLTIPDduel.2'):
    ALIAS[k] = '"' + k  # the base file quotes the line, so the key became "EVTTOOLTIP..., text wrapped in ""..""
NEW = {
    # Avatar cycle (new event atlafix.10)
    'atlafix.10.t': 'The Cycle Is Broken',
    'atlafix.10.d': 'The Avatar has been struck down while in the Avatar State. Every past life, from the first Avatar onward, was channelled through that body in that moment, and now the light has gone out of all of them at once.\\n\\nThere will be no reincarnation. The Air Nomads will search for a child who is not coming, and the spirits will have no bridge to the human world. Whatever comes next, the world will have to face it without the Avatar.',
    'atlafix.10.a': 'The world is on its own now.',
    # Decisions
    'airball_improve_bending': 'Airball Bending Training', 'airball_improve_bending_desc': 'Spend some of your standing in the Airball Association on a few weeks of intensive training with its best players.',
    'earthking_ra_loyalty_campaign': 'Loyalty Campaign', 'earthking_ra_loyalty_campaign_desc': 'Spend gold and Royal Authority on a campaign that brings this county to the faith of the Earth Monarchy.',
    'form_air_nation': 'Found the Air Nation', 'form_air_nation_desc': 'All four Air Temples answer to us. Unite them as one Air Nation.',
    'form_kuvira_earth_empire': 'Proclaim the Earth Empire', 'form_kuvira_earth_empire_desc': 'The Earth Kingdom has failed its people. From Ba Sing Se, proclaim a new Earth Empire under a single, unifying ruler.',
    'get_gay_married_': 'Marry Your Lover', 'get_gay_married__desc': 'Propose marriage to your lover.',
    'give_to_the_sages': 'Give to the Sages', 'give_to_the_sages_desc': 'Send this courtier to join the sages and live a life of devotion.',
    'imperial_ambitions_3': 'Expand the Colonies',
    'absorb_pirate_governor_desc': 'Bring this tributary pirate captain directly into your cartel as a vassal.',
    'show_me_best_benders_desc': 'List the most powerful benders in the world.',
    # Events
    'EVTDESCHYW.58': 'Omashu remains free. While the Fire Nation burns its way across the Earth Kingdom, its old king holds his city as if the war were a game he has already won.',
    'EVTDESC_AIRBALL_1010': 'Your fellow members of the Airball Association have asked you to work on your balance. Training on the poles is the only way to improve.',
    'EVT_AIRBALL_1013_PLACEHOLDER': '',
    'EVTOPT_AIRBALL_1013': 'My balance has never been better.',
    'EVTDESC_SANDR.620': '[Root.GetFirstName],\\n\\nThe Grand Master has heard your request and agrees that you have earned a higher place among the Sand Sailers.',
    'EVTOPTA_SANDR.621': 'I am honoured.',
    'EVTOPTB_SANDR.1068': 'Let them try again!',
    'EVTOPTA_PRT_20084': 'How dare they!',
    'EVTOPTAhA.145': 'May you find your own path.',
    'EVTOPTB_MNSAK_5100': 'Shout for help!',
    'EVTOPTD_MNSAK_5156': '[From.GetFirstName] will pledge allegiance to the Fire Nation.',
    'EVTOPTbending.97': 'My parents have decided I will not get a bending teacher. I will have to make do on my own.',
    'EVTOPTspecial.46': 'I can fly!',
    'TOOLTIPAspecial.26': 'You will begin practising on small animals.',
    'TOOLTIPBspecial.26': 'You put the idea out of your mind.',
    'TOOLTIPAspecial.27': 'You continue practising on small rodents.',
    'NOMADEVTDESC500': 'My [GetFromRelation] [From.GetFullName] has chosen me as [From.GetHerHis] successor.',
    'mandate.6': 'So be it.', 'mandate11b': 'Royal Authority will decrease slightly.',
    'mandatepuppet': 'The Grand Secretariat will rule in my name.', 'mandatepuppetcons': 'The Grand Secretariat will rule in my name.',
    'can_reform_barbarism': 'The Barbarian faith can now be reformed.',
    'CB_AVATAR_CRISIS_WAR': 'Avatar Crisis War', 'WAR_AVATAR_CRISIS_WAR': "The Avatar's Crisis War against [Base.GetTitledFirstName]",
    'NAE.105.TT': 'All your bending traits are combined into Fully Realised Avatar, which gives all of their bonuses.',
    'NAE.112.OPTA': 'Dammit!',
    'NAE.213.TT': 'The Avatar will join your court and help your people.',
    'NAE.313.D': 'My family member has come home from travelling with the Avatar, and has become an expert with weapons along the way.',
    'NAE.315.OPTB': 'And most of it they give away to those in need!',
    'NAE.500.D': 'The Avatar has arrived at the court of [From.GetTitledFirstName].',
    'NAE.551.OPTA': 'Glad to help.', 'NAE.552.OPTA': 'Their loss.',
    'NAE.623.OPTC': "I'm just in touch with my past lives. It's fine.",
    'NAE.624.OPTD': 'There is only one option left to me...',
    'NAE.702.OPTD': "This isn't your fight.",
    'NAE.THANK': 'Thank you, Avatar.',
    # Modifiers
    'ek_unrest': 'Earth Kingdom Unrest', 'ek_law_low_mandate_change': 'Recent Mandate Reform', 'duel_refused_freely': 'Declined a Duel',
    'superhero_cooldown': 'Recently Saved the Day',
    'supporting_the_earth_kingdom_desc': 'As a figurehead Earth King, most of the crown\'s revenue goes to the upkeep of Ba Sing Se, its walls and its bureaucracy.',
    # Traits
    'bisexual': 'Bisexual', 'bisexual_desc': 'This character is attracted to both men and women.',
    'secretly_fire_nation_imperialism': 'Secretly Fire Imperialist', 'secretly_fire_nation_imperialism_desc': 'This character secretly follows Fire Imperialism.',
}
del NEW['EVT_AIRBALL_1013_PLACEHOLDER']
for i, (p, n) in enumerate([('Favour of the Spirits', 'Loss of Favour')] * 1):
    pass
MAND = ['Faint', 'Modest', 'Firm', 'Strong', 'Great', 'Heavenly']
for i in range(6):
    NEW['mandateposituvemodifier%d' % (i + 1)] = 'Mandate of the Spirits: %s' % MAND[i]
    NEW['mandatenegativemodifier%d' % (i + 1)] = 'Mandate Questioned: %s' % ['Murmurs', 'Doubts', 'Discontent', 'Defiance', 'Unrest', 'Revolt'][i]
OVERRIDE = {
    # Earth Monarchy description still described China (GitHub #609)
    'chinese_imperial_government_desc': 'The Earth Monarchy, much like ordinary Feudal government, revolves around vassals owing fealty to their liege. Its officials, examinations and ancient traditions are modelled on the court of Ba Sing Se, and it favours dialogue over religious differences.',
    # Bleeding of past lives: option texts were shifted by one (abdicating read "There is only one option left")
    'NAE.625.OPTB': "I've mastered my past lives.",
    'NAE.625.OPTC': "I'm not fit to rule anymore.",
}
rows = []
miss = []
for k, src in ALIAS.items():
    if src not in loc: miss.append((k, src)); continue
    if k in loc: continue
    txt = loc[src]
    if src.startswith('"'): txt = txt.replace('""', '"').strip('"')
    rows.append((k, txt))
for k, v in NEW.items():
    if k in loc: miss.append((k, 'ALREADY DEFINED')); continue
    rows.append((k, v))
for k, v in OVERRIDE.items(): rows.append((k, v))
assert not miss, miss
for k, v in rows: assert ';' not in v and '\n' not in v, k
out = '#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x\n# ATLA Fixes: missing or mismatched text in Avatar - Four Nations Restored. Named 0000_ so it loads before the base mod files (first definition wins).\n'
out += ''.join('%s;%s;;;;;;;;;;;;;x\n' % (k, v) for k, v in rows)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'wb').write(out.replace('\n', '\r\n').encode('cp1252'))
print(len(rows), 'rows')
