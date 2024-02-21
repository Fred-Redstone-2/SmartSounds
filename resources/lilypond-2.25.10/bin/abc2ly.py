#!/home/lily/lilypond-2.25.10/release/binaries/dependencies/install/Python-3.10.8/bin/python3.10
# -*- coding: utf-8 -*-

#    This file is part of LilyPond, the GNU music typesetter.
#
#    Copyright (C) 1999--2023  Han-Wen Nienhuys <hanwen@xs4all.nl>
#                              Jan Nieuwenhuizen <janneke@gnu.org>
#
#    LilyPond is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    LilyPond is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with LilyPond.  If not, see <http://www.gnu.org/licenses/>.

# Convert ABC music notation to LilyPond code.
#
# This script provides incomplete support for ABC standard v1.6:
#
#   https://abcnotation.com/standard/abc_v1.6.txt
#


# Limitations
#
# Multiple tunes in single file not supported
# Blank T: header lines should write score and open a new score
# Not all header fields supported
# ABC line breaks are ignored
# Block comments generate error and are ignored
# Postscript commands are ignored
# lyrics not resynchronized by line breaks (lyrics must fully match notes)
# %%LY slyrics can't be directly before a w: line.


# TODO:
#
# * updates to latest ABC standard
# * coding style
# * lilylib
# * GNU style messages:  warning:FILE:LINE:
# * l10n
# * support of upbeats for metered music – this needs a huge rewrite of
#   this script
# * better support for incomplete repeats
#
# UNDEF -> None


import gettext
import os
import re
import sys

"""

# relocate-preamble.py.in
#
# This file is part of LilyPond, the GNU music typesetter.
#
# Copyright (C) 2007--2023  Han-Wen Nienhuys <hanwen@xs4all.nl>
#
# LilyPond is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LilyPond is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LilyPond.  If not, see <http://www.gnu.org/licenses/>.
#

This is generic code, used for all python scripts.

The quotes are to ensure that the source .py file can still be
run as a python script, but does not include any sys.path handling.
Otherwise, the lilypond-book calls inside the build
might modify installed .pyc files.

"""

# This is needed for installations with a non-default layout, ie where share/
# is not next to bin/.
sys.path.insert (0, os.path.join ('/home/lily/lilypond-2.25.10/release/binaries/mingw/lilypond/install/share/lilypond/2.25.10', 'python'))

# Dynamic relocation, for installations with a default layout including GUB,
# but also for execution from the build directory.
bindir = os.path.abspath (os.path.dirname (sys.argv[0]))
topdir = os.path.dirname (bindir)
if bindir.endswith (r'/scripts/out'):
    topdir = os.path.join (os.path.dirname (topdir), 'out')
datadir = os.path.abspath (os.path.join (topdir, 'share', 'lilypond'))
for v in [ 'current', '2.25.10' ]:
    sys.path.insert (0, os.path.join (datadir, v, 'python'))

"""
"""

# Load translation and install _() into Python's builtins namespace.
gettext.install('lilypond', '/home/lily/lilypond-2.25.10/release/binaries/mingw/lilypond/install/share/locale')

import lilylib as ly

version = '2.25.10'
if version == '@' + 'TOPLEVEL_VERSION' + '@':
    version = '(unknown version)'                # uGUHGUHGHGUGH

UNDEF = 255
parser_state = UNDEF
voice_idx_dict = {}
header = {}
header['footnotes'] = ''
lyrics = []
slyrics = []
voices = []
state_list = []
implicit_repeat = [False] * 8
current_voice_idx = -1
current_lyric_idx = -1
lyric_idx = -1
default_len = 8
length_specified = False
nobarlines = False
global_key = [0] * 7                        # UGH
names = ["One", "Two", "Three"]
DIGITS = '0123456789'
HSPACE = ' \t'
midi_specs = ''
need_unmetered_bar = False


def error(msg):
    sys.stderr.write(msg)
    if global_options.strict:
        sys.exit(1)


def alphabet(i):
    return chr(i + ord('A'))


def check_clef(s, state):
    # the number gives the base_octave
    clefs = [("treble", "treble", 0),
             ("treble1", "french", 0),
             ("bass3", "varbaritone", 0),
             ("bass", "bass", 0),
             ("alto4", "tenor", 0),
             ("alto2", "mezzosoprano", 0),
             ("alto1", "soprano", 0),
             ("alto", "alto", 0),
             ("perc", "percussion", 0)]
    modifier = [("-8va", "_8", -1),
                ("-8", "_8", -1),
                (r"\+8", "^8", +1),
                ("8", "_8", -1)]

    if not s:
        return ''
    clef = None
    octave = 0
    for c in clefs:
        m = re.match('^' + c[0], s)
        if m:
            (clef, octave) = (c[1], c[2])
            s = s[m.end():]
            break
    if not clef:
        return s

    mod = ""
    for md in modifier:
        m = re.match('^' + md[0], s)
        if m:
            mod = md[1]
            octave += md[2]
            s = s[m.end():]
            break

    state.base_octave = octave
    voices_append("\\clef \"" + clef + mod + "\"\n")
    return s


def select_voice(name, rol):
    global current_voice_idx
    global parser_state

    if name not in voice_idx_dict:
        state_list.append(Parser_state())
        voices.append('')
        slyrics.append([])
        voice_idx_dict[name] = len(voices) - 1

    current_voice_idx = voice_idx_dict[name]
    parser_state = state_list[current_voice_idx]

    # TODO: Add more keywords.
    while rol != '':
        m = re.match('^([^ \t=]*)=(.*)$', rol)  # find keyword
        if m:
            keyword = m.group(1)
            rol = m.group(2)
            a = re.match('^("[^"]*"|[^ \t]*) *(.*)$', rol)
            if a:
                value = a.group(1)
                rol = a.group(2)
                if keyword == 'clef':
                    check_clef(value, parser_state)
                elif keyword == "name":
                    value = re.sub('\\\\', '\\\\\\\\', value)
                    # < 2.2
                    voices_append(
                        "\\set Staff.instrumentName = %s\n" % value)
                elif keyword in ("sname", "snm"):
                    voices_append(
                        "\\set Staff.shortInstrumentName = %s\n" % value)
        else:
            break


def dump_global(outf):
    if need_unmetered_bar:
        outf.write(r'''
cadenzaMeasure = {
  \cadenzaOff
  \partial 1024 s1024
  \cadenzaOn
}
''')


def dump_header(outf, hdr):
    outf.write('\n\\header {\n')
    ks = sorted(hdr.keys())
    for k in ks:
        hdr[k] = re.sub('"', '\\"', hdr[k])
        outf.write('  %s = "%s"\n' % (k, hdr[k]))
    outf.write('}\n')


def dump_lyrics(outf):
    if lyrics:
        outf.write("\n\\markup \\column {\n")
        for i in range(len(lyrics)):
            outf.write(lyrics[i])
            outf.write("\n")
        outf.write("}\n")


def dump_slyrics(outf):
    ks = sorted(voice_idx_dict.keys())
    for k in ks:
        for i in range(len(slyrics[voice_idx_dict[k]])):
            outf.write("\n\"words%sV%s\" = \\lyricmode {" % (k, i + 1))
            outf.write("\n" + slyrics[voice_idx_dict[k]][i])
            outf.write("\n}\n")


def dump_voices(outf):
    ks = sorted(voice_idx_dict.keys())
    for k in ks:
        idx = voice_idx_dict[k]

        if re.match('[1-9]', k):
            m = alphabet(int(k))
        else:
            m = k
        outf.write("\n\"voice%s\" = {" % m)
        if implicit_repeat[idx]:
            outf.write("\n\\repeat volta 2 {")
        outf.write("\n" + voices[idx])
        if repeat_state[idx]:
            if repeat_state[idx] in (ALTERNATIVE1, ALTERNATIVE2):
                outf.write("} } }")
            else:
                outf.write("}")
        outf.write("\n}\n")


def try_parse_q(a):
    # Assume that Q takes the form "Q:'opt. description' 1/4=120".
    # There are other possibilities, but they are deprecated.
    r = re.compile(r' *^(.*?) *([0-9]+) */ *([0-9]+) *=* *([0-9]+)\s*')
    m = r.match(a)
    if m:
        descr = m.group(1)  # possibly empty
        numerator = int(m.group(2))
        denominator = int(m.group(3))
        tempo = m.group(4)
        dur = duration_to_lilypond_duration((numerator, denominator), 0)
        if descr:
            descr += ' '
        voices_append("\\tempo " + descr + dur + " = " + tempo + "\n")
    else:
        # Parsing of numeric tempi, as these are fairly
        # common.  The spec says the number is a "beat" so using
        # a quarter note as the standard time.
        numericQ = re.compile('[0-9]+')
        m = numericQ.match(a)
        if m:
            voices_append("\\tempo 4=" + m.group(0))
        else:
            sys.stderr.write(
                "abc2ly: Warning, unable to parse Q specification: %s\n" % a)


def dump_score(outf):
    outf.write(r"""

\score {
  <<
""")

    ks = sorted(voice_idx_dict.keys())
    for k in ks:
        if k == 'default' and len(voice_idx_dict) > 1:
            break
        outf.write("    \\context Staff = \"%s\" {\n" % k)
        if k != 'default':
            outf.write("      \\voicedefault\n")
        outf.write("      \\\"voice%s\"" % k)
        outf.write("\n    }")

        for i in range(len(slyrics[voice_idx_dict[k]])):
            outf.write("\n    \\addlyrics {\n")
            outf.write("      \\\"words%sV%s\"" % (k, i + 1))
            outf.write("\n    }")

    outf.write("\n  >>\n")
    if global_options.beams:
        outf.write(r'''
  \layout {
    \context {
      \Voice
      \autoBeamOff
      melismaBusyProperties = #'()
    }
  }''')
    else:
        outf.write(r'''
  \layout {}''')
    outf.write("\n  \\midi {%s}\n}\n" % midi_specs)


def set_default_length(s):
    global default_len
    global length_specified

    m = re.search('1/([0-9]+)', s)
    if m:
        default_len = int(m.group(1))
        length_specified = True


def set_default_len_from_time_sig(s):
    global default_len

    m = re.search('([0-9]+)/([0-9]+)', s)
    if m:
        n = int(m.group(1))
        d = int(m.group(2))
        if n / d < 0.75:
            default_len = 16
        else:
            default_len = 8


# Pitch manipulation. Tuples are (name, alteration).
# 0 is (central) C. Alteration -1 is a flat, alteration +1 is a sharp.
# Pitch in semitones.
def semitone_pitch(tup):
    p = 0

    t = tup[0]
    p += 12 * (t // 7)
    t = t % 7

    if t > 2:
        p -= 1

    p += t * 2 + tup[1]
    return p


def fifth_above_pitch(tup):
    (n, a) = (tup[0] + 4, tup[1])

    difference = 7 - (semitone_pitch((n, a)) - semitone_pitch(tup))
    a += difference

    return (n, a)


def sharp_keys():
    p = (0, 0)
    l = []
    while True:
        l.append(p)
        (t, a) = fifth_above_pitch(p)
        if semitone_pitch((t, a)) % 12 == 0:
            break

        p = (t % 7, a)
    return l


def flat_keys():
    p = (0, 0)
    l = []
    while True:
        l.append(p)
        (t, a) = quart_above_pitch(p)
        if semitone_pitch((t, a)) % 12 == 0:
            break

        p = (t % 7, a)
    return l


def quart_above_pitch(tup):
    (n, a) = (tup[0] + 3, tup[1])

    difference = 5 - (semitone_pitch((n, a)) - semitone_pitch(tup))
    a += difference

    return (n, a)


key_lookup = {         # abc to LilyPond key mode names
    'm': 'minor',
    'min': 'minor',
    'maj': 'major',
    'major': 'major',
    'phr': 'phrygian',
    'ion': 'ionian',
    'loc': 'locrian',
    'aeo': 'aeolian',
    'mix': 'mixolydian',
    'mixolydian': 'mixolydian',
    'lyd': 'lydian',
    'dor': 'dorian',
    'dorian': 'dorian'
}


def lily_key(k):
    if k == 'none':
        return ''
    orig = "" + k
    # UGR
    k = k.lower()
    key = k[0]
    # UGH
    k = k[1:]
    if k and k[0] == '#':
        key += 'is'
        k = k[1:]
    elif k and k[0] == 'b':
        key += 'es'
        k = k[1:]
    if not k:
        return '%s \\major' % key

    typ = k[0:3]
    if typ not in key_lookup:
        # ugh, use lilylib, say WARNING:FILE:LINE:
        sys.stderr.write("abc2ly:warning:")
        sys.stderr.write("ignoring unknown key: `%s'" % orig)
        sys.stderr.write('\n')
        return 0
    return "%s \\%s" % (key, key_lookup[typ])


def shift_key(note, acc, shift):
    s = semitone_pitch((note, acc))
    s = (s + shift + 12) % 12
    if s <= 4:
        n = s // 2
        a = s % 2
    else:
        n = (s + 1) // 2
        a = (s + 1) % 2
    if a:
        n += 1
        a = -1
    return (n, a)


key_shift = {  # semitone shifts for key mode names
    'm': 3,
    'min': 3,
    'minor': 3,
    'maj': 0,
    'major': 0,
    'phr': -4,
    'phrygian': -4,
    'ion': 0,
    'ionian': 0,
    'loc': 1,
    'locrian': 1,
    'aeo': 3,
    'aeolian': 3,
    'mix': 5,
    'mixolydian': 5,
    'lyd': -5,
    'lydian': -5,
    'dor': -2,
    'dorian': -2
}


def compute_key(k):
    k = k.lower()
    intkey = (ord(k[0]) - ord('a') + 5) % 7
    intkeyacc = 0
    k = k[1:]

    if k and k[0] == 'b':
        intkeyacc = -1
        k = k[1:]
    elif k and k[0] == '#':
        intkeyacc = 1
        k = k[1:]
    k = k[0:3]
    if k and k in key_shift:
        (intkey, intkeyacc) = shift_key(intkey, intkeyacc, key_shift[k])
    keytup = (intkey, intkeyacc)

    sharp_key_seq = sharp_keys()
    flat_key_seq = flat_keys()

    accseq = None
    accsign = 0
    if keytup in sharp_key_seq:
        accsign = 1
        key_count = sharp_key_seq.index(keytup)
        accseq = [(4 * x - 1) % 7 for x in range(1, key_count + 1)]
    elif keytup in flat_key_seq:
        accsign = -1
        key_count = flat_key_seq.index(keytup)
        accseq = [(3 * x + 3) % 7 for x in range(1, key_count + 1)]
    else:
        error("Huh?")
        raise Exception("Huh")

    key_table = [0] * 7
    for a in accseq:
        key_table[a] += accsign

    return key_table


tup_lookup = {
    '2': '3/2',
    '3': '2/3',
    '4': '4/3',
    '5': '4/5',
    '6': '4/6',
    '7': '6/7',
    '9': '8/9',
}


def try_parse_tuplet_begin(s, state):
    if re.match(r'\([2-9]', s):
        dig = s[1]
        s = s[2:]
        prev_tuplet_state = state.parsing_tuplet
        state.parsing_tuplet = int(dig[0])
        if prev_tuplet_state:
            close_beam_state(state)
            voices_append("}")
        voices_append("\\times %s {" % tup_lookup[dig])
    return s


def try_parse_group_end(s, state):
    if s and s[0] in HSPACE:
        s = s[1:]
        close_beam_state(state)
    return s


def header_append(key, a):
    s = ''
    if key in header:
        s = header[key] + "\n"
        header[key] = s + a


def wordwrap(a, v):
    linelen = len(v) - v.rfind('\n')
    if linelen + len(a) > 80:
        v += '\n'
    return v + a + ' '


def stuff_append(stuff, idx, a):
    if not stuff:
        stuff.append(a)
    else:
        stuff[idx] = wordwrap(a, stuff[idx])


# Ignore wordwrap since we are adding to the previous word.

def stuff_append_back(stuff, idx, a):
    if not stuff:
        stuff.append(a)
    else:
        point = len(stuff[idx]) - 1
        while stuff[idx][point] == ' ':
            point -= 1
        point += 1
        stuff[idx] = stuff[idx][:point] + a + stuff[idx][point:]


def voices_append(a):
    if current_voice_idx < 0:
        select_voice('default', '')
    stuff_append(voices, current_voice_idx, a)


# Wordwrap really makes it hard to bind beams to the end of notes since it
# pushes out whitespace on every call. The _back functions do an append
# prior to the last space, effectively tagging whatever they are given
# onto the last note.

def voices_append_back(a):
    if current_voice_idx < 0:
        select_voice('default', '')
    stuff_append_back(voices, current_voice_idx, a)


def lyrics_append(a):
    a = re.sub('#', '\\#', a)        # latex does not like naked #'s
    a = re.sub('"', '\\"', a)        # latex does not like naked "'s
    a = '  \\line { "' + a + '" }\n'
    stuff_append(lyrics, current_lyric_idx, a)


# Break lyrics to words and put "'s around words containing numbers and '"'s.

def fix_lyric(s):
    ret = ''
    while s != '':
        m = re.match('[ \t]*([^ \t]*)[ \t]*(.*$)', s)
        if m:
            word = m.group(1)
            s = m.group(2)
            word = re.sub('"', '\\"', word)    # escape "
            if re.match(r'.*[0-9"\(]', word):
                word = re.sub('_', ' ', word)  # _ causes probs inside ""
                ret += '\"' + word + '\" '
            else:
                ret += word + ' '
        else:
            return ret
    return ret


TEXT = 1
SPACE = 2
SPANNER = 3

def slyrics_append(a):
    global lyric_idx

    s = ''
    status = TEXT
    prev_status = TEXT
    escaped = False

    for c in a:
        # Escaped characters are inserted as-is.
        if escaped:
            if status != TEXT:
                s += ' '
            s += c
            status = TEXT
            escaped = False
            continue

        if c == '\\':
            escaped = True
        elif c == ' ':
            s += ' '
            status = SPACE
            continue       # Don't update `prev_status'.
        elif c == '-':
            # ' -' is the same as '-_'.
            if status == SPACE:
                if prev_status == TEXT:
                    s += '-- '
                s += '_'
                status = SPANNER
            elif status == TEXT:
                s += ' --'
                status = SPANNER
            elif status == SPANNER:
                s += ' _'
        elif c == '_':
            if status == SPACE:
                if prev_status == TEXT:
                    s += '__ '
                s += '_'
                status = SPANNER
            if status == TEXT:
                s += ' __ _'
                status = SPANNER
            elif status == SPANNER:
                s += ' _'
        elif c == '*':
            if status == SPACE:
                s += '_'
            else:
                s += ' _'
        elif c == '~':
            s += '_'
            status = TEXT
        else:
            if status == SPANNER:
                s += ' '
            s += c
            status = TEXT

        prev_status = status

    # ensure that we have a space between this and a potential follow-up 'w:' line
    s += ' '

    s = re.sub('#', '\\#', s)         # latex does not like naked #'s
    # put numbers and " and ( into quoted string
    if re.match(r'.*[0-9"\(]', s):
        s = fix_lyric(s)

    lyric_idx += 1

    if len(slyrics[current_voice_idx]) <= lyric_idx:
        slyrics[current_voice_idx].append(s)
    else:
        slyrics[current_voice_idx][lyric_idx] = wordwrap(
            s, slyrics[current_voice_idx][lyric_idx])


def try_parse_header_line(ln, state):
    m = re.match('^([A-Za-z]): *(.*)$', ln)

    if m:
        g = m.group(1)
        a = m.group(2)
        if g == 'T':  # title
            a = re.sub('[ \t]*$', '', a)  # strip trailing blanks
            if 'title' in header:
                if a:
                    if len(header['title']):
                        # the non-ascii character
                        # in the string below is a
                        # punctuation dash. (TeX ---)
                        header['title'] += ' — ' + a
                    else:
                        header['subtitle'] = a
            else:
                header['title'] = a
        elif g == 'M':        # Meter
            global length_specified

            if a == 'C':
                if not state.common_time:
                    state.common_time = True
                    voices_append("\\defaultTimeSignature")
                a = '4/4'
            elif a == 'C|':
                if not state.common_time:
                    state.common_time = True
                    voices_append("\\defaultTimeSignature")
                a = '2/2'
            elif a in ('4/4', '2/2'):
                if state.common_time:
                    state.common_time = False
                    voices_append("\\numericTimeSignature")

            if not length_specified:
                set_default_len_from_time_sig(a)
            else:
                length_specified = False

            if a == 'none':
                state.has_meter = False
            else:
                if state.in_music and not state.has_meter:
                    voices_append('\\cadenzaOff\n')
                voices_append('\\time %s' % a)
                state.has_meter = True
            state.next_bar = ''
        elif g == 'K':  # KEY
            a = check_clef(a, state)
            if a and a != 'none':
                global global_key

                # separate clef info
                m = re.match('^([^ \t]*) *([^ ]*)( *)(.*)$', a)
                if m:
                    # There may or may not be a space
                    # between the key letter and the mode.
                    # Convert the mode to lower-case before comparing.
                    mode = m.group(2)[0:3].lower()
                    if mode and mode in key_lookup:
                        # use the full mode, not only the first three letters
                        key_info = m.group(1) + m.group(2).lower()
                        clef_info = a[m.start(4):]
                    else:
                        key_info = m.group(1)
                        clef_info = a[m.start(2):]
                    global_key = compute_key(key_info)
                    k = lily_key(key_info)
                    if k:
                        voices_append('\\key %s' % k)
                    check_clef(clef_info, state)
                else:
                    global_key = compute_key(a)
                    k = lily_key(a)
                    if k:
                        voices_append('\\key %s \\major' % k)
        elif g == 'N':  # Notes
            header['footnotes'] += '\\\\\\\\' + a
        elif g == 'O':  # Origin
            header['origin'] = a
        elif g == 'X':  # Reference Number
            header['crossRefNumber'] = a
        elif g == 'A':  # Area
            header['area'] = a
        elif g == 'H':  # History
            header_append('history', a)
        elif g == 'B':  # Book
            header['book'] = a
        elif g == 'C':  # Composer
            if 'composer' in header:
                if a:
                    header['composer'] += '\\\\\\\\' + a
            else:
                header['composer'] = a
        elif g == 'S':
            header['subtitle'] = a
        elif g == 'L':  # Default note length
            set_default_length(ln)
        elif g == 'V':  # Voice
            voice = re.sub(' .*$', '', a)
            rest = re.sub('^[^ \t]*  *', '', a)
            if state.next_bar:
                voices_append(state.next_bar)
                state.next_bar = ''
            select_voice(voice, rest)
        elif g == 'W':  # Words
            lyrics_append(a)
        elif g == 'w':  # vocals
            slyrics_append(a)
        elif g == 'Q':  # tempo
            try_parse_q(a)
        elif g == 'R':  # Rhythm (e.g. jig, reel, hornpipe)
            header['meter'] = a
        elif g == 'Z':  # Transcription (e.g. Steve Mansfield 1/2/2000)
            header['transcription'] = a
        return ''
    return ln


# We use in this order specified accidental, active accidental for bar,
# active accidental for key.

def pitch_to_lilypond_name(name, acc, bar_acc, key):
    s = ''
    if acc == UNDEF:
        if not nobarlines:
            acc = bar_acc
    if acc == UNDEF:
        acc = key
    if acc == -1:
        s = 'es'
    elif acc == 1:
        s = 'is'

    if name > 4:
        name -= 7
    return chr(name + ord('c')) + s


def octave_to_lilypond_quotes(o):
    o += 2
    s = ''
    if o < 0:
        o = -o
        s = ','
    else:
        s = '\''

    return s * o


def parse_num(s):
    durstr = ''
    while s and s[0] in DIGITS:
        durstr += s[0]
        s = s[1:]

    n = None
    if durstr:
        n = int(durstr)
    return (s, n)


def duration_to_lilypond_duration(multiply_tup, dots):
    base = 1
    while base * multiply_tup[0] < multiply_tup[1]:
        base *= 2
    if base == 1:
        if (multiply_tup[0] / multiply_tup[1]) == 2:
            base = '\\breve'
        elif (multiply_tup[0] / multiply_tup[1]) == 3:
            base = '\\breve'
            dots = 1
        elif (multiply_tup[0] / multiply_tup[1]) == 4:
            base = '\\longa'
    return '%s%s' % (base, '.' * dots)


class Parser_state:
    def __init__(self):
        self.in_music = False
        self.has_meter = False
        self.in_acc = {}
        self.next_articulation = ''
        self.next_bar = ''
        self.next_dots = 0
        self.next_den = 1
        self.parsing_tuplet = 0
        self.in_chord = False
        self.is_first_chord_note = False
        self.chord_num = -1
        self.chord_den = -1
        self.chord_current_dots = -1
        self.plus_chord = False
        self.base_octave = 0
        self.common_time = True
        self.parsing_beam = False


# return (str, num, den, dots, tie)
def parse_duration_and_tie(s, state):
    num = 0
    den = state.next_den
    state.next_den = 1
    tie = ''

    (s, num) = parse_num(s)
    if not num:
        num = 1
    if len(s):
        if s[0] == '/':
            if len(s[0]):
                while s[:1] == '/':
                    s = s[1:]
                    d = 2
                    if s[0] in DIGITS:
                        (s, d) = parse_num(s)

                    den *= d

    den *= default_len

    if s[0] == '-':
        tie = '~'
        s = s[1:]

    current_dots = state.next_dots
    state.next_dots = 0

    current_dots_delta = 0
    den_factor = 1
    next_dots_delta = 0
    next_den_factor = 1

    have_lt = False
    have_gt = False

    if re.match('[ \t]*[<>]', s):
        while s[0] in HSPACE:
            s = s[1:]
        while s[0] == '>':
            have_gt = True
            s = s[1:]
            current_dots_delta += 1
            next_den_factor *= 2
        while s[0] == '<':
            have_lt = True
            s = s[1:]
            den_factor *= 2
            next_dots_delta += 1

    if state.in_chord:
        if have_gt:
            sys.stderr.write("Warning: ignoring '>' in chord\n")
        if have_lt:
            sys.stderr.write("Warning: ignoring '<' in chord\n")
    else:
        current_dots += current_dots_delta
        den *= den_factor
        state.next_dots += next_dots_delta
        state.next_den *= next_den_factor

    try_dots = [3, 2, 1]
    for d in try_dots:
        f = 1 << d
        multiplier = (2 * f - 1)
        if num % multiplier == 0 and den % f == 0:
            num /= multiplier
            den /= f
            current_dots += d

    return (s, num, den, current_dots, tie)


def try_parse_rest(s, state):
    global lyric_idx

    if not s or s[0] != 'z' and s[0] != 'x':
        return s

    lyric_idx = -1

    if state.next_bar:
        voices_append(state.next_bar)
        state.next_bar = ''

    if s[0] == 'z':
        rest = 'r'
    else:
        rest = 's'
    s = s[1:]

    (s, num, den, d, tie) = parse_duration_and_tie(s, state)
    voices_append(
        '%s%s' % (rest, duration_to_lilypond_duration((num, den), d)))
    if tie:
        sys.stderr.write("Warning: ignoring tie after rest\n")
    if state.next_articulation:
        voices_append(state.next_articulation)
        state.next_articulation = ''

    return s


artic_tbl = {
    '.': '-.',
    'T': '^\\trill',
    'H': '^\\fermata',
    'u': '^\\upbow',
    'K': '^\\ltoe',
    'k': '^\\accent',
    'M': '^\\tenuto',
    '~': '^"~" ',
    'J': '',                # ignore slide
    'R': '',                # ignore roll
    'S': '^\\segno',
    'O': '^\\coda',
    'v': '^\\downbow'
}


def try_parse_articulation(s, state):
    while s and s[:1] in artic_tbl:
        state.next_articulation += artic_tbl[s[:1]]
        if not artic_tbl[s[:1]]:
            sys.stderr.write("Warning: ignoring `%s'\n" % s[:1])

        s = s[1:]

    # s7m2 input doesn't care about spaces
    if re.match(r'[ \t]*\(', s):
        s = s.lstrip()

    while s[:1] == '(' and s[1] not in DIGITS:
        state.next_articulation += '('
        s = s[1:]

    return s


# Remember accidental for rest of bar.

def set_bar_acc(note, octave, acc, state):
    if acc == UNDEF:
        return
    n_oct = note + octave * 7
    state.in_acc[n_oct] = acc


# Get accidental set in this bar or UNDEF if not set.

def get_bar_acc(note, octave, state):
    n_oct = note + octave * 7
    if n_oct in state.in_acc:
        return state.in_acc[n_oct]
    return UNDEF


def clear_bar_acc(state):
    state.in_acc = {}


# if we are parsing a beam, close it off
def close_beam_state(state):
    if state.parsing_beam and global_options.beams:
        state.parsing_beam = False
        voices_append_back(']')


# WAT IS ABC EEN ONTZETTENDE PROGRAMMEERPOEP  !
def try_parse_note(s, state):
    global lyric_idx

    if not s:
        return s

    articulation = ''
    acc = UNDEF
    if s[0] in '^=_':
        c = s[0]
        s = s[1:]
        if c == '^':
            acc = 1
        if c == '=':
            acc = 0
        if c == '_':
            acc = -1

    octave = state.base_octave
    if s[0] in "ABCDEFG":
        s = s[0].lower() + s[1:]
        octave -= 1

    notename = 0
    if s[0] in "abcdefg":
        notename = (ord(s[0]) - ord('a') + 5) % 7
        s = s[1:]
    else:
        return s                # failed; not a note!

    lyric_idx = -1

    if state.next_bar:
        voices_append(state.next_bar)
        state.next_bar = ''

    while s[0] == ',':
        octave -= 1
        s = s[1:]
    while s[0] == '\'':
        octave += 1
        s = s[1:]

    (s, num, den, current_dots, tie) = parse_duration_and_tie(s, state)
    if state.in_chord and not state.is_first_chord_note:
        state.chord_num = num
        state.chord_den = den
        state.chord_current_dots = current_dots
        state.is_first_chord_note = True

    if (global_options.beams
            and state.parsing_beam
            and num / den > 1 / 8):
        close_beam_state(state)

    if re.match(r'[ \t]*\)', s):
        s = s.lstrip()
    slur_end = 0
    while s[:1] == ')':
        slur_end += 1
        s = s[1:]

    bar_acc = get_bar_acc(notename, octave, state)
    pit = pitch_to_lilypond_name(notename, acc, bar_acc, global_key[notename])
    octv = octave_to_lilypond_quotes(octave)
    if acc != UNDEF and acc in (global_key[notename], bar_acc):
        mod = '!'
    else:
        mod = ''

    if state.in_chord:
        voices_append("%s%s%s%s" % (pit, octv, mod, tie))
    else:
        voices_append(
            "%s%s%s%s%s" %
            (pit, octv, mod, duration_to_lilypond_duration(
                (num, den), current_dots), tie))

    set_bar_acc(notename, octave, acc, state)
    if not state.in_chord:
        if state.next_articulation:
            articulation += state.next_articulation
            state.next_articulation = ''
        if articulation:
            voices_append(articulation)

    if slur_end:
        voices_append(')' * slur_end)

    if not state.in_chord and state.parsing_tuplet:
        state.parsing_tuplet -= 1
        if not state.parsing_tuplet:
            close_beam_state(state)
            voices_append("}")

    if (global_options.beams
            and not state.parsing_beam
            and not state.in_chord
            and (s[0] in '^=_ABCDEFGabcdefg'
                 or (s[0] == '[' and s[2] != ':'))
            and num / den <= 1 / 8):
        state.parsing_beam = True
        voices_append_back('[')

    return s


def junk_space(s, state):
    while s and s[0] in '\t\n\r ':
        s = s[1:]
        close_beam_state(state)

    return s


def try_parse_guitar_chord(s, state):
    if s[:1] == '"':
        s = s[1:]
        gc = ''
        if s[0] == '_' or (s[0] == '^'):
            position = s[0]
            s = s[1:]
        else:
            position = '^'
        while s and s[0] != '"':
            gc += s[0]
            s = s[1:]

        if s:
            s = s[1:]
        gc = re.sub('#', '\\#', gc)        # escape '#'s
        state.next_articulation = ("%c\"%s\"" % (position, gc)) \
            + state.next_articulation
    return s


def try_parse_escape(s):
    if not s or s[0] != '\\':
        return s

    s = s[1:]
    if s[:1] == 'K':
        key_table = compute_key()
    return s


# |] thin-thick double bar line
# || thin-thin double bar line
# [| thick-thin double bar line
# :| left repeat
# |: right repeat
# :: left-right repeat
# |1 volta 1
# |2 volta 2

# TODO:
#
# * In '|[1' or ':|[2', allow space after '|'.
# * Support '... :| ... :|'.

bar_dict = {
    '|]': '\\bar "|."',
    '||': '\\bar "||"',
    '[|': '\\bar ".|"',
    ':|': '}',
    '|:': '\n\\repeat volta 2 {',
    '::': '}\n\\repeat volta 2 {',
    '[1': '\n  \\alternative {\n    \\volta 1 {',
    '|1': '\n  \\alternative {\n    \\volta 1 {',
    '|[1': '\n  \\alternative {\n    \\volta 1 {',
    '[2': '}\n    \\volta 2 {',
    '|2': '}\n    \\volta 2 {',
    ':|2': '}\n    \\volta 2 {',
    ':|[2': '}\n    \\volta 2 {',
    '|': '\\bar "|"'
}

alternative1_opener = ['[1', '|1', '|[1']
alternative2_opener = ['[2', '|2', ':|2', ':|[2']
repeat_ender = [':|']
repeat_opener = ['|:']       # implicitly closes alternatives
repeat_ender_opener = ['::'] # implicitly closes alternatives

REPEAT = 0
ALTERNATIVE1 = 1
ALTERNATIVE2 = 2

repeat_state = [None] * 8


def try_parse_bar(string, state):
    bs = ''
    braces = ''
    if current_voice_idx < 0:
        select_voice('default', '')

    # Try the longer one first.
    for trylen in [4, 3, 2, 1]:
        if string[:trylen] and string[:trylen] in bar_dict:
            s = string[:trylen]
            string = string[trylen:]
            rep = repeat_state[current_voice_idx]

            if s in alternative1_opener:
                if rep == ALTERNATIVE1:
                    sys.stderr.write(
                        ("Warning: already in first alternative,"
                         " ignoring `%s'\n") % s)
                    break
                if rep == ALTERNATIVE2:
                    sys.stderr.write(
                        ("Warning: already in second alternative,"
                         " ignoring `%s'\n") % s)
                    break
                if rep == REPEAT:
                    rep = ALTERNATIVE1
                else:
                    if implicit_repeat[current_voice_idx]:
                        sys.stderr.write(
                            "Warning: not in a repeat, ignoring `%s'\n" % s)
                        break
                    # Assume an implicit repeat sign at the beginning of
                    # the piece.
                    implicit_repeat[current_voice_idx] = True
                    rep = ALTERNATIVE1

            elif s in alternative2_opener:
                if rep == ALTERNATIVE2:
                    sys.stderr.write(
                        ("Warning: already in second alternative,"
                         " ignoring `%s'\n") % s)
                    break
                if rep == REPEAT:
                    sys.stderr.write(
                        ("Warning: no first alternative,"
                         " ignoring `%s'\n") % s)
                    break
                if rep == ALTERNATIVE1:
                    rep = ALTERNATIVE2
                else:
                    sys.stderr.write(
                        "Warning: not in a repeat, ignoring `%s'\n" % s)
                    break

            else:
                if s in repeat_ender:
                    if rep is None:
                        if implicit_repeat[current_voice_idx]:
                            sys.stderr.write(
                                ("Warning: not in a repeat,"
                                 " ignoring `%s'\n") % s)
                            break
                        # Assume an implicit repeat sign at the
                        # beginning of the piece.
                        implicit_repeat[current_voice_idx] = True
                    rep = None

                elif s in repeat_opener:
                    if rep in (ALTERNATIVE1, ALTERNATIVE2):
                        braces = '} } }'
                    elif rep == REPEAT:
                        braces = '}'
                    rep = REPEAT

                elif s in repeat_ender_opener:
                    if rep is None:
                        if implicit_repeat[current_voice_idx]:
                            sys.stderr.write(
                                ("Warning: not in a repeat,"
                                 " ignoring `%s'\n") % s)
                            break
                        # Assume an implicit repeat sign at the
                        # beginning of the piece.
                        implicit_repeat[current_voice_idx] = True
                    elif rep in (ALTERNATIVE1, ALTERNATIVE2):
                        braces = '} }'
                    rep = REPEAT

            repeat_state[current_voice_idx] = rep
            bs = braces + bar_dict[s]
            break

    if string[:1] == '|':
        state.next_bar = '|\n'
        string = string[1:]
        clear_bar_acc(state)
        close_beam_state(state)

    if string[:1] == '}':
        close_beam_state(state)

    if bs or state.next_bar:
        if state.parsing_tuplet:
            state.parsing_tuplet = 0
            voices_append('}')

    if bs:
        global need_unmetered_bar

        clear_bar_acc(state)
        close_beam_state(state)
        if not state.has_meter:
            need_unmetered_bar = True
            voices_append('\\cadenzaMeasure')
        voices_append(bs)
    return string


def bracket_escape(s, state):
    m = re.match(r'^([^\]]*)] *(.*)$', s)
    if m:
        cmd = m.group(1)
        s = m.group(2)
        try_parse_header_line(cmd, state)
    return s


def try_parse_chord_delims(s, state):
    out = ''
    tie = ''
    if s[:1] == '[':
        if re.match('\\[[0-9]', s):      # repeat, not chord
            return s
        s = s[1:]
        if re.match('[A-Z]:', s):        # bracket escape, not chord
            return bracket_escape(s, state)
        if state.next_bar:
            voices_append(state.next_bar)
            state.next_bar = ''
        out = '<'
    elif s[:1] == '+':                   # deprecated since ABC 1.6
        s = s[1:]
        if state.plus_chord:
            out = '>'
            state.plus_chord = False
        else:
            if state.next_bar:
                voices_append(state.next_bar)
                state.next_bar = ''
            out = '<'
            state.plus_chord = True
    elif s[:1] == ']':
        global default_len

        state.in_chord = False

        s = s[1:]
        out = '>'

        def_len = default_len
        next_den = state.next_den
        next_dots = state.next_dots

        default_len = 1
        state.next_den = 1
        state.next_dots = 0

        (s, num, den, current_dots, tie) = parse_duration_and_tie(s, state)
        state.chord_num *= num
        state.chord_den *= den
        state.chord_current_dots += current_dots

        default_len = def_len
        state.next_den *= next_den
        state.next_dots += next_dots

    if not out:
        return s

    if re.match(r'[ \t]*\)', s):
        s = s.lstrip()
    slur_end = 0
    while s[:1] == ')':
        slur_end += 1
        s = s[1:]

    if out == '>':
        out += duration_to_lilypond_duration(
            (state.chord_num, state.chord_den), state.chord_current_dots)
        out += tie

        if state.next_articulation:
            out += state.next_articulation
            state.next_articulation = ''

        voices_append(out + ")" * slur_end)

        if state.parsing_tuplet:
            state.parsing_tuplet -= 1
            if not state.parsing_tuplet:
                close_beam_state(state)
                voices_append("}")

        if (global_options.beams
                and not state.parsing_beam
                and (s[0] in '^=_ABCDEFGabcdefg'
                     or (s[0] == '[' and s[2] != ':'))
                and state.chord_num / state.chord_den <= 1 / 8):
            state.parsing_beam = True
            voices_append('[')

    else:
        if slur_end:
            sys.stderr.write("Warning: ignoring `)' in chord\n")
        state.in_chord = True
        state.is_first_chord_note = False
        voices_append(out)

    return s


def try_parse_grace_delims(s, state):
    if s[:1] == '{':
        if state.next_bar:
            voices_append(state.next_bar)
            state.next_bar = ''
        s = s[1:]
        voices_append('\\grace {')
    elif s[:1] == '}':
        s = s[1:]
        close_beam_state(state)
        voices_append('}')

    return s


def try_parse_comment(s):
    if s[0] == '%':
        if s[0:5] == '%MIDI':
            # The nobarlines option is necessary for an abc to LilyPond
            # translator for exactly the same reason abc2midi needs it: abc
            # requires the user to enter the note that will be printed, and
            # MIDI and LilyPond expect entry of the pitch that will be
            # played.
            #
            # In standard 19th century musical notation, the algorithm for
            # translating between printed note and pitch involves using the
            # barlines to determine the scope of the accidentals.
            #
            # Since ABC is frequently used for music in styles that do not
            # use this convention, such as most music written before 1700,
            # or ethnic music in non-western scales, it is necessary to be
            # able to tell a translator that the barlines should not affect
            # its interpretation of the pitch.
            if 'nobarlines' in s:
                global nobarlines
                nobarlines = True
        elif s[0:3] == '%LY':
            p = s.find('voices')
            if p > -1:
                voices_append(s[p + 7:])
                voices_append("\n")
            p = s.find('slyrics')
            if p > -1:
                slyrics_append(s[p + 8:])

    # Write other kinds of appending if we ever need them.
    return s


lineno = 0
happy_count = 100


def parse_file(fn):
    global parser_state
    global lineno

    f = open(fn, encoding='utf-8')
    ls = f.readlines()
    ls = [re.sub("\r$", '', x) for x in ls]

    select_voice('default', '')
    lineno = 0
    if not global_options.quiet:
        sys.stderr.write("Line ... ")
        sys.stderr.flush()
    parser_state = state_list[current_voice_idx]

    for ln in ls:
        lineno += 1

        if not lineno % happy_count:
            sys.stderr.write('[%d]' % lineno)
            sys.stderr.flush()
        m = re.match('^([^%]*)%(.*)$', ln)  # add comments to current voice
        if m:
            if m.group(2):
                try_parse_comment(m.group(2))
                voices_append('%% %s\n' % m.group(2))
            ln = m.group(1)

        orig_ln = ln

        ln = junk_space(ln, parser_state)
        ln = try_parse_header_line(ln, parser_state)

        # If `ln' is not empty at this point, the parsing of header lines is
        # finished, and the music block starts.
        if ln:
            parser_state.in_music = True
            if not parser_state.has_meter:
                voices_append("\\once \\omit Staff.TimeSignature\n")
                voices_append("\\cadenzaOn\n")

        # Try nibbling characters off until the line doesn't change.
        prev_ln = ''
        while ln != prev_ln:
            prev_ln = ln
            ln = try_parse_chord_delims(ln, parser_state)
            ln = try_parse_rest(ln, parser_state)
            ln = try_parse_articulation(ln, parser_state)
            ln = try_parse_note(ln, parser_state)
            ln = try_parse_bar(ln, parser_state)
            ln = try_parse_escape(ln)
            ln = try_parse_guitar_chord(ln, parser_state)
            ln = try_parse_tuplet_begin(ln, parser_state)
            ln = try_parse_group_end(ln, parser_state)
            ln = try_parse_grace_delims(ln, parser_state)
            ln = junk_space(ln, parser_state)

        if ln:
            error("%s: %d: Huh?  Don't understand\n" % (fn, lineno))
            left = orig_ln[0:-len(ln)]
            sys.stderr.write(left + '\n')
            sys.stderr.write(' ' * len(left) + ln + '\n')


def identify():
    if not global_options.quiet:
        sys.stderr.write("%s from LilyPond %s\n" % (ly.program_name, version))


authors = """
Written by Han-Wen Nienhuys <hanwen@xs4all.nl>, Laura Conrad
<lconrad@laymusic.org>, Roy Rankin <Roy.Rankin@@alcatel.com.au>.
"""


def print_version():
    print(r"""abc2ly (GNU LilyPond) %s""" % version)


def get_option_parser():
    p = ly.get_option_parser(
        usage=_("%s [OPTION]... FILE") %
        'abc2ly',
        description=_('''abc2ly converts ABC music files (see
%s) to LilyPond input.
''') %
        'https://abcnotation.com/standard/abc_v1.6.txt',
        add_help_option=False)

    p.version = "abc2ly (LilyPond) 2.25.10"
    p.add_option("--version",
                 action="version",
                 help=_("show version number and exit"))
    p.add_option("-h", "--help",
                 action="help",
                 help=_("show this help and exit"))
    p.add_option("-o", "--output", metavar='FILE',
                 action="store",
                 help=_("write output to FILE"))
    p.add_option("-s", "--strict",
                 action="store_true",
                 help=_("be strict about success"))
    p.add_option('-b', '--beams',
                 action="store_true",
                 help=_("preserve ABC's notion of beams"))
    p.add_option('-q', '--quiet',
                 action="store_true",
                 help=_("suppress progress messages"))
    p.add_option_group('',
                       description=(
                           _('Report bugs via %s')
                           % 'bug-lilypond@gnu.org') + '\n')
    return p


option_parser = get_option_parser()
(global_options, files) = option_parser.parse_args()


identify()

header['tagline'] = (
    'LilyPond %s was here -- automatically converted from ABC' % version)

for file in files:
    if file == '-':
        file = ''

    if not global_options.quiet:
        sys.stderr.write('Parsing `%s\'...\n' % file)
    parse_file(file)

    if not global_options.output:
        global_options.output = os.path.basename(
            os.path.splitext(file)[0]) + ".ly"
    if not global_options.quiet:
        sys.stderr.write('LilyPond output to: `%s\'...' %
                         global_options.output)
    out_file = open(global_options.output, 'w', encoding='utf-8')

    # Don't substitute @VERSION@.  We want this to reflect
    # the last version that was verified to work.
    out_file.write('\\version "2.24.0"\n')

    dump_header(out_file, header)
    dump_global(out_file)
    dump_slyrics(out_file)
    dump_voices(out_file)
    dump_score(out_file)
    dump_lyrics(out_file)
    if not global_options.quiet:
        sys.stderr.write('\n')
