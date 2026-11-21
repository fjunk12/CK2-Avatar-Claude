# ATLA Fixes round 2 (runs inside build.py, after round 1; rd() returns round-1 text for files already edited)
def subre1(t, pat, repl, what, flags=0):
    n = len(re.findall(pat, t, flags)); assert n == 1, (what, n)
    LOG.append(what); return re.sub(pat, repl, t, count=1, flags=flags)
def in_event(f, eid, fn):
    t = rd(f); s, e = event_span(t, eid); b = fn(t[s:e]); t = t[:s] + b + t[e:]; wr(f, t)

# R2-1 GitHub #632: slave colony CB made the new ruler ROOT's vassal after making them tributary,
# which breaks the tributary bond (breaks_on_realm_change = yes). Make them independent, then tributary.
f = 'common/cb_types/outlaw_religions_cbs.txt'; t = rd(f)
i = t.index('cb_slave_colony = {'); s = t.index('on_success_title = {', i); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\t\t\tpiety = 500\n\t\t\t}\n\t\t\tusurp_title_plus_barony_if_unlanded_and_vassals',
         '\t\t\t\tpiety = 500\n\t\t\t\tsave_event_target_as = atlafix_slave_colony_ruler\n\t\t\t}\n\t\t\tusurp_title_plus_barony_if_unlanded_and_vassals', 'slave colony CB: new ruler saved as event target')
b = sub1(b, '\t\t\tROOT = {\n\t\t\t\tmake_tributary = { who = new_character tributary_type = slave_colony_tributary }\n\t\t\t\tnew_character = { set_defacto_liege = THIS }\n\t\t\t\tnew_character = { set_government_type = pirate_cartel }\n\t\t\t}\n',
         '\t\t\t# ATLA Fixes (GitHub #632): independent first, then tributary. Setting ROOT as liege afterwards broke the tributary bond.\n'
         '\t\t\tevent_target:atlafix_slave_colony_ruler = {\n\t\t\t\tset_defacto_liege = THIS\n\t\t\t\tset_government_type = pirate_cartel\n\t\t\t}\n'
         '\t\t\tROOT = {\n\t\t\t\tmake_tributary = { who = event_target:atlafix_slave_colony_ruler tributary_type = slave_colony_tributary }\n\t\t\t}\n',
         'slave colony CB (#632): ruler independent, then tributary of the attacker')
t = t[:s] + b + t[e:]; wr(f, t)

# R2-2 GitHub #615: Roku's eruption death needed HYW_1, which is usually not set by 818
f = 'events/ATLA_hundred_year_war.txt'
in_event(f, 'ATLAE.10', lambda b: sub1(b, '\ttrigger = {\n\t\thas_global_flag = HYW_1\n\t\ttrait = firelord\n\t}',
    '\ttrigger = {\n\t\ttrait = firelord # ATLA Fixes (GitHub #615): HYW_1 removed, it is usually not set by 818 so Roku never died\n\t}', 'ATLAE.10 (#615): Roku dies in the eruption without HYW_1'))

# R2-3 Purge flags: HYW_4 was never set; HYW_5-8 (temples destroyed) were never set either
in_event(f, 'ATLAE.23', lambda b: sub1(b, '\t\t\tset_global_flag = HYW_9\n', '\t\t\tset_global_flag = HYW_9\n\t\t\tset_global_flag = HYW_4 # ATLA Fixes: "Airbender purge started" was never set\n', 'ATLAE.23: purge launch sets HYW_4'))
TEMPLES = ''.join('\t\t\t%s = { holder_scope = { religion_group = air_religions } }\n' % c for c in ('c_northern_air_temple', 'c_southern_air_temple', 'c_eastern_air_temple', 'c_western_air_temple'))
in_event(f, 'ATLAE.69', lambda b: sub1(b, '\t\tNOT = { has_global_flag = HYW_5 }\n\t\tNOT = { has_global_flag = HYW_6 }\n\t\tNOT = { has_global_flag = HYW_7 }\n\t\tNOT = { has_global_flag = HYW_8 }\n',
    '\t\tOR = { # ATLA Fixes: the "temple destroyed" flags HYW_5-8 are never set, so this fired even after a successful purge\n' + TEMPLES + '\t\t}\n', 'ATLAE.69: "Air Nomads survived" only if they still hold an air temple'))
f2 = 'decisions/ATLA_imperialism_decisions.txt'; t = rd(f2)
s = t.index('imperial_ambitions_22 = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\t\thas_global_flag = HYW_8\n', '\t\t\thas_global_flag = HYW_4 # ATLA Fixes: HYW_8 (Northern Air Temple destroyed) was never set, so this was never available\n\t\t\tc_northern_air_temple = { holder_scope = { NOT = { religion_group = air_religions } } }\n', 'Recruit the Barbarians: available once the Northern Air Temple has fallen')
t = t[:s] + b + t[e:]; wr(f2, t)

# R2-4 "Prince's Ambition" (ATLAE.118/132): the fallback random_child always ran and overwrote Ozai
FALL = '\t\trandom_child = {\n\t\t\tlimit = {\n\t\t\t\tis_adult = yes\n\t\t\t\tNOT = { has_character_flag = chosen_son }\n\t\t\t}\n\t\t\tsave_event_target_as = usurper_son\n\t\t\tset_character_flag = usurper_son\n\t\t}\n'
FALLNEW = ('\t\tif = { # ATLA Fixes: fallback only when there is no adult Ozai (it used to overwrite him)\n'
           '\t\t\tlimit = { NOT = { any_child = { is_adult = yes has_character_flag = is_ozai } } }\n'
           '\t\t\trandom_child = {\n\t\t\t\tlimit = {\n\t\t\t\t\tis_adult = yes\n\t\t\t\t\tNOT = { has_character_flag = chosen_son }\n\t\t\t\t}\n'
           '\t\t\t\tsave_event_target_as = usurper_son\n\t\t\t\tset_character_flag = usurper_son\n\t\t\t}\n\t\t}\n')
for eid in ('ATLAE.118', 'ATLAE.132'):
    in_event(f, eid, lambda b, eid=eid: sub1(b, FALL, FALLNEW, '%s: usurper son fallback only without Ozai' % eid))

# R2-5 GitHub #608: pacifist Air Nomads could take the aggressive "Expand your Realm" ambition
f = 'common/objectives/00_ambitions.txt'; t = rd(f)
s = t.index('obj_see_the_realm_grow = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
b = sub1(b, '\t\tNOT = { has_character_flag = tookFiveYearFocus }\n\t}\n\t\n\tallow = {',
         '\t\tNOT = { has_character_flag = tookFiveYearFocus }\n\t\tNOR = { # ATLA Fixes (GitHub #608): pacifist air faiths\n\t\t\treligion = air_spirituality\n\t\t\treligion = air_acolytism\n\t\t\treligion = air_acolytism_reformed\n\t\t}\n\t}\n\t\n\tallow = {', 'Expand your Realm (#608): not for pacifist Air Nomads')
t = t[:s] + b + t[e:]; wr(f, t)

# R2-6 earthking.66: a non-Earth-Kingdom-culture holder of the Earth Kingdom had no option at all
in_event('events/ATLA_earthking.txt', 'earthking.66', lambda b: subre1(b, r'(name = EVTOPTC_EK_66b\n\t\ttrigger = \{\n)\t\t\tculture_group = earth_kingdom_cultures\n',
    r'\1\t\t\t# ATLA Fixes: culture check removed, a foreign conqueror holding the Earth Kingdom had no option\n', 'earthking.66: option for foreign holders of the Earth Kingdom'))

# R2-7 Pets: the rare-pet search kept rolling after giving up and could open a success event with no options
in_event('events/ATLA_pets_events.txt', 'PETS.5', lambda b: subre1(b, r'(\n\tis_triggered_only = yes\n)',
    r'\1\ttrigger = { # ATLA Fixes: stop searching after giving up\n\t\tOR = {\n\t\t\thas_character_flag = searching_for_bear\n\t\t\thas_character_flag = searching_for_catdeer\n\t\t\thas_character_flag = searching_for_dragon\n\t\t}\n\t}\n', 'PETS.5: search stops after giving up'))

# R2-8 Breaking the Avatar cycle (the manual promises it, nothing set the flag)
f = 'events/ATLA_Duel_events.txt'; t = rd(f)
t = sub1(t, '\t\t\t\tsubtract_variable = { which = mySTA value = 2 }\n\t\t\t\tcharacter_event = { id = ADUEL.99 }',
         '\t\t\t\tsubtract_variable = { which = mySTA value = 2 }\n\t\t\t\tset_character_flag = atlafix_in_avatar_state # ATLA Fixes: dying within 10 days of this ends the Avatar cycle\n\t\t\t\tcharacter_event = { id = ADUEL.99 }', 'duel: Avatar State marks the Avatar')
wr(f, t)
f = 'events/ATLA_avatar_system.txt'
def nae001(b):
    b = sub1(b, '\timmediate = {\n\t\tset_global_flag = avatar_interregnum\n',
             '\timmediate = {\n\t\t# ATLA Fixes: killed in a duel while in the Avatar State (flag set within the last 10 days) -> the cycle ends\n'
             '\t\tif = {\n\t\t\tlimit = {\n\t\t\t\thas_character_flag = atlafix_in_avatar_state\n\t\t\t\tNOT = { had_character_flag = { flag = atlafix_in_avatar_state days = 10 } }\n\t\t\t}\n'
             '\t\t\tset_global_flag = avatar_cycle_broken\n\t\t\tany_player = { narrative_event = { id = atlafix.10 days = 7 } }\n\t\t}\n'
             '\t\tset_global_flag = avatar_interregnum\n', 'NAE.001: cycle breaks if the Avatar dies in the Avatar State')
    s = b.index('\t\ttrigger_switch = {\n\t\t\ton_trigger = has_global_flag')
    k = '#Ping event to set up reincarnation events\n'; e = b.index(k) + len(k)
    LOG.append('NAE.001: no reincarnation once the cycle is broken')
    return b[:s] + '\t\tif = { # ATLA Fixes: no reincarnation once the cycle is broken\n\t\t\tlimit = { NOT = { has_global_flag = avatar_cycle_broken } }\n' + b[s:e] + '\t\t}\n' + b[e:]
in_event(f, 'NAE.001', nae001)
in_event(f, 'NAE.002', lambda b: subre1(b, r'(\n\t\tNOT = \{ persistent_event_target:the_avatar = \{ is_alive = yes \} \}[^\n]*\n)',
    r'\1\t\tNOT = { has_global_flag = avatar_cycle_broken } # ATLA Fixes\n', 'NAE.002: never after the cycle is broken'))
in_event(f, 'NAE.004', lambda b: sub1(b, 'trigger = { NOT = { persistent_event_target:the_avatar = { is_alive = yes } } } # ATLA Fixes',
    'trigger = { NOT = { persistent_event_target:the_avatar = { is_alive = yes } } NOT = { has_global_flag = avatar_cycle_broken } } # ATLA Fixes', 'NAE.004: never after the cycle is broken'))

# R3-1 Crisis War (cb_shatter_realm): on success it iterated any_realm_title, which does not exist in CK2
# (error.log: "Unknown effect-type" at line 1120), so the defeated realm's kingdom and empire titles were never destroyed.
f = 'common/cb_types/03_cb_types_ATLA.txt'; t = rd(f)
s = t.index('cb_shatter_realm = {'); e = block_end(t, t.index('{', s)); b = t[s:e]
old = '''					any_realm_title = { #Targets vassals AND ruler!
						limit = {
							higher_tier_than = DUKE
							controls_religion = no
						}
						unsafe_destroy_landed_title = THIS
					}
'''
new = '''					# ATLA Fixes: any_realm_title does not exist in CK2, so nothing was destroyed. Ruler, then every vassal.
					any_demesne_title = {
						limit = {
							higher_tier_than = DUKE
							controls_religion = no
						}
						unsafe_destroy_landed_title = THIS
					}
					any_realm_character = {
						any_demesne_title = {
							limit = {
								higher_tier_than = DUKE
								controls_religion = no
							}
							unsafe_destroy_landed_title = THIS
						}
					}
'''
b = sub1(b, old, new, 'Crisis War: destroys the kingdom and empire titles of the defeated realm (any_realm_title does not exist)')
t = t[:s] + b + t[e:]; wr(f, t)
