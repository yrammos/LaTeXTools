# ST2/ST3 compat
# Addendum for LilyPond-book support in the LaTeXTools package for Sublime Text 2 by msiniscalchi.
# Please report bugs related to this addendum to Yannis Rammos (yannis.rammos [at] me.com)
# or github.com/yrammos.
#
# This module, jump_aux.py, provides constants and auxiliary functions for use with the SyncTeX implementation in LyTeXTools.

import re

lytex_scope_open = ["%\\openlytex\n"]
lytex_scope_close = ["%\\closelytex\n"]
lytex_scope_open_regex = ["%.*\\.*openlytex.*$"]
lytex_scope_close_regex = ["%.*\\.*closelytex.*$"]
lily_packages = ["\\usepackage{graphics}\n"]

# Look for the next occurence of at least one among "strings" in file "target" and
# assume that the current index of the file is at line "startpos".
# Return the line number of that next occurence and the index of the matched delimiter (if applicable).
# If "regex" is false (default), then each line has all whitespace characters filtered out before matching is attempted.
# If "regex" is true, then "strings" contains regex patterns rather than string literals, and no filtering out is
# performed prior to matching.
def line_of_next_occurrence(target, startpos, strings, regex=False):
	# Remove whitespace characters, but not newlines, from string s. Convert s to lowercase.
	# Used to used to normalize .lytex and .tex files prior to scanning for Lilypond scopes.
	def filter_line(s):
		s = s.replace(' ', '')
		s = s.replace('\t', '')
		s = s.replace('\r', '').lower()
		return s

	# print ("Seeking: ", strings)
	# re_lytex_opening = re.compile(r"\\begin(\[[A-Za-z0-9=., ]*\])?{lilypond}", re.IGNORECASE)
	r = target.readline()
	if not regex:
		r = filter_line(r)
		counter = startpos + 1
		# print ("           scanning line: ", counter, ":  ", repr(r))
		while r:
			if r in strings:
				return counter, strings.index(r)
			r = target.readline()
			r = filter_line(r)
			counter = counter + 1
			# print ("           scanning line: ", counter, ":  ", repr(r))
		return counter, 0
	else:
		counter = startpos + 1
		# print ("           scanning line: ", counter, ":  ", repr(r))
		while r:
			for pat in strings:
				if re.search(pat, r):
					return counter, strings.index(pat)
			r = target.readline()
			counter = counter + 1
			# print ("           scanning line: ", counter, ":  ", repr(r))
		return counter, 0
