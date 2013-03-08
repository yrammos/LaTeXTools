# Addendum adding LilyPond-book support to the LaTeXTools package for Sublime Text 2 by msiniscalchi.
# Please report bugs related to this addendum to Yannis Rammos (yannis.rammos [at] me.com)
# or github.com/yrammos.
#
# This module, jump_aux.py, provides constants and auxiliary functions for use with the SyncTeX implementation in LyTeXTools.

import re

# The following delimiters (and one regex) are hard-coded as they cover all cases
# I've encountered so far. If more cases crop up, they may warrant a user setting
# via some preference file.

lytex_opening_markers = ["\\begin{lilypond}"]
lytex_closing_markers = ["\\end{lilypond}" + '\n']
tex_opening_markers = ["{%" + '\n', "\\begin{quote}" + '\n']
tex_closing_markers = ["}" + '\n', "\\end{quote}" + '\n']
lily_packages = ["\\usepackage{graphics}" + '\n']

# Look for the next occurence of at least one among "strings" in file "target" and
# assume that the current index of the file is at line "startpos".
# Return the line number of that next occurence and the index of the matched delimiter (if applicable).
def line_of_next_occurrence(target, startpos, strings):
	# Remove whitespace characters, but not newlines, from string s. Convert s to lowercase.
	# Used to used to normalize .lytex and .tex files prior to scanning for Lilypond scopes.
	def filter_line(s):
		s = s.replace(' ', '')
		s = s.replace('\t', '')
		s = s.replace('\r', '').lower()
		return s

	re_lytex_opening = re.compile(r"\\begin(\[[A-Za-z0-9=., ]*\])?{lilypond}", re.IGNORECASE)
	r = target.readline()
	r = filter_line(r)
	counter = startpos + 1          # print "           scanning line: ", counter, ":  ", repr(r)
	while r:
		if r in strings:
			return counter, strings.index(r)
		if (re_lytex_opening.match(r)):
			return counter, 0
		r = target.readline()
		r = filter_line(r)
		counter = counter + 1       # print "           scanning line: ", counter, ":  ", repr(r)
	return counter, 0