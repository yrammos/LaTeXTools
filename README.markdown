#LyTeXTools: LilyPond-aware LaTeXTools for Sublime Text 2 & 3
by [Yannis Rammos](www.twitter.com/yannisrammos)

[**UPDATE: If you have not yet upgraded to OS X El Capitan (10.11.x), and LyTeXTools has stopped working, please read [Path Considerations].**]

This package adds `lilypond-book` support to [Marciano Siniscalchi’s](http://tekonomist.wordpress.com/) [LaTeXTools](http://github.com/SublimeText/LaTeXTools) for [Sublime Text 2](http://www.sublimetext.com/2) and [Sublime Text 3](http://www.sublimetext.com/3).

A component of [GNU LilyPond](http://lilypond.org), the formidable music typesetter, `lilypond-book` enables LaTeX writers to include LilyPond code snippets within LaTeX documents, thereby freely mixing text with musical notation. It is a command-line preprocessor that “extracts snippets of music from your document, runs LilyPond on them, and outputs the document with pictures substituted for the music.”

Overall, LyTeXTools extends LaTeXTools in the following ways:

* It accepts `.lytex` (LaTeX with inline LilyPond) in addition to `.tex` (plain LaTeX) source files.
* It instructs `lilypond-book` to preprocess the current document, if needed, and to produce a `.tex` file prior to invoking `latexmk`.
* It extends the SyncTeX functionality of LaTeXTools, with seamless “forward” and “inverse” search capabilities regardless of the source file extension (`.tex` or `.lytex`). Unfortunately, as `lilypond-book` provides no native support for SyncTeX, this functionality would be best described as a hack and relies on a bash script for OS X (see below). Users are warmly invited to contribute a port of this short and straightforward script to Windows.

LaTeXTools and LyTeXTools behave identically when invoked with plain `.tex` files.

## Installing LyTeXTools (OSX-only)

To avoid confusion, and given its lack of support for Windows at present, LyTeXTools has not been submitted to [Will Bond’s](http://wbond.net) [Package Control](http://wbond.net/sublime_packages/package_control). You may install the package manually by cloning (or copying the unzipped contents of) this repository into your `./Packages` folder:

	git clone https://github.com/yrammos/LyTeXTools.git

* Please note that the stable version of LyTeXTools is in the `lytextools` branch, not the `master` branch! Run `git checkout lilypond2latexmk` after cloning to ensure that you are on that branch.

New users unfamiliar with Marciano Siniscalchi’s LaTeXTools are advised to read his detailed and lucid [documentation](http://github.com/SublimeText/LaTeXTools#requirements-and-setup) first. The following notes only address areas where the two packages diverge.

It is best to uninstall the original LaTeXTools package before installing LyTeXTools, or you may confront build engine conflicts.

## Setting up LyTeXTools

The following settings override those of the original LaTeXTools. All other LaTeXTools settings still apply to LyTeXTools.

### Jumping from/to PDF (SyncTeX)

“Forward” and “inverse” search with `.lytex` files are non-trivial because SyncTeX only provides a mapping between the PDF and the LilyPond-generated `.tex`, whereas the original source file is the `.lytex`. LyTeXTools undertakes the missing link, namely a bidirectional mapping between `.tex` and `.lytex` line numbers.

Inverse search from the PDF (Skim.app) to the `.lytex` or `.tex` source is provided by the `sublsync` script, a central component of this package. Its purpose is to store the SyncTeX-generated coordinates (source file name, line number) into a file whence LyTeXTools can then retrieve them.

By default, LyTeXTools expects this file to be `~/.sublatex.txt`. This location may be overriden via a `synctex_output` key-value pair in a `LyTeXTools.sublime-settings` JSON file, for example:

	{
    	"synctex_output":   "~/path/file.extension"
	}

Please ensure you have adequate write privileges in that path.

But enough with theory and preliminaries. To actually set up your SyncTeX-enabled PDF viewer (which I presume is Skim.app):

1. Go to Skim > Preferences > Sync.
2. Under "Preset" select "Custom."
3. Deselect the "Check for file changes" box.
4. In the Command field enter `<full_path_to_LyTeXTools_Package>/sublsync`.
5. In the Arguments field enter `~/.sublatex.txt "%file" %line "/usr/local/bin/"`. <br>Replace:<br>
	a. Optionally, the `~/.sublatex.txt` default with whatever setting you have overriden it with (per instructions above).<br>
	b. `"/usr/local/bin/"` with the full path to the directory containing [subl](http://www.sublimetext.com/docs/2/osx_command_line.html) binary, which launches Sublime Text 2 from the command line. Remember to enclose the path in quotation marks if it includes spaces!

### Path considerations

The process will likely fail unless a valid path to the `lilypond-book` binary is declared within the `LaTeX.sublime-build` file, for example:

	"osx":  {
    	        ...
        	    "path" : "$PATH:/usr/texbin:/usr/local/bin:/Applications/LilyPond.app/Contents/Resources/bin/"
            	...
	        }

The LyTeXTools build engine assumes that you are running OS X El Capitan (10.11.x) or later. **If you are running an earlier version (<10.11) **, please replace `/Library/TeX/texbin` with `/usr/texbin` in the `LaTeX.sublime-build` file. This is a kludge, but I currently have no time to provide a more elegant solution (and besides, I plan to update LyTeXTools to bring it up to date with the mother project (LaTeXTools), which provides a superior and customizable build engine mechanism).

## Using LyTeXTools

### Compiling LilyPond within your LaTeX project

LyTeXTools decides whether to invoke `lilypond-book` **solely on the basis of the filename extension**: `.tex` files are assumed to contain no LilyPond-content and are passed directly to `latexmk`, whereas `.lytex` files are preprocessed by `lilypond-book` prior to compilation by `latexmk`. Invoking `lilypond-book` on files with no LilyPond code has no side-effects, so you may want to use the `.lytex` extension on all your project files regardless of content and no longer worry about the issue.

### LyTeXTools and multi-file typesetting projects

It is strongly recommended that you **use the `.lytex` extension** with the root file of your project, even if it does not contain any LilyPond code in itself: Doing so will instruct LyTeXTools to trigger `lilypond-book` on the entire project (as a `lilypond-book` “make” session of sorts), and therefore to preprocess any other `.lytex` files that you may have included in your project with `\input` statements, rendering a manual run of `lilypond-book` on each individual `.lytex` project file unnecessary.

Of course you will need to explicitly include this extension in the `% !TEX root` flags at the top of all your `.tex.` and `.lytex` project files:

    % !TEX root = my_root_file_name.lytex

Likewise, `\input` statements should explicitly specify the `.lytex` extension, unless you really intend to include a LilyPond-free `.tex` file, in which case the extension is optional:

    \input{Chapter1.lytex}

### Inserting LilyPond code in your LaTeX project

LyTeXTools is transparent and works just like its original counterpart, LaTeXTools. Simply ensure that your LilyPond code blocks are wrapped with the LyTeXTools-specific `% \openlytex` and `% \closelytex` delimiters, as in the following example:

	\documentclass[a4paper]{article}

	\begin{document}

	Documents for \verb+lilypond-book+ may freely mix music and text!
	For example,

	% \openlytex
	\begin{lilypond}
	\relative c' {
	  c2 g'2 \times 2/3 { f8 e d } c'2
	}
	\end{lilypond}
	% \closelytex

	Larger examples can be put into a separate file, and introduced with
	\verb+\lilypondfile+, as follows:

	% \openlytex
	\lilypondfile{example.ly}
	% \closelytex

	\end{document}

Failure to use these delimiters **will break the Jump to/from PDF (SyncTeX) functionality!** Please use the templates described in the following section to have the delimiters automatically inserted as you type.

#### Technical note: Why the delimiters are necessary

In order to accurately map `.tex` line numbers to `.lytex` line numbers and vice-versa, LyTeXTools must be able to unambiguously identify LilyPond scopes, both within the source (`.lytex`) file and within the LilyPond-generated `.tex` file.

LilyPond scopes in the `.lytex` file are trivial to identify:

	\begin{lilypond}[...]
		...
	\end{lilypond}

The situation appears less straightforward on the `.tex` side. So far, I have been able to identify only two pairs of delimiters that may wrap the generated LilyPond code:

	\begin{quote}
		...
	\end{quote}

and a rather bland pair of curly brackets:

	{
		...
	}

It is obvious that neither pair can be unambiguously attributed to LilyPond. For this reason, I am replacing the error-prone heuristics of earlier LyTeXTools versions with the unambiguous delimiters `% \openlytex` and `% \closelytex`.

### Code highlighting

LyTeXTools includes a "LilyPond Book" syntax definition. Any LilyPond code embedded within your `.lytex` source will be correctly identified and, provided that the [SubLilyPond](https://www.github.com/yrammos/SubLilyPond) package is also installed, highlighted. To prevent duplicate installations of SubLilyPond, I decided against repackaging it within LyTeXTools. The most straightforward way to install SubLilyPond is via Package Control.

### Snippets and autocompletions

LyTeXTools provides a number of templates (or, in Sublime Text 2 parlance, snippets and autcompletions) to facilitate the inclusion of LilyPond content within your `.lytex` document.

#### `Wrap in LyTeXTools delimiters`

Accessible via the command palette `⌘-⇧-P`. Wraps the selected text within `% \openlytex` and `% \closelytex` delimiters. I have not assigned a tab trigger to this snippet but you may do so yourself by tweaking the file `Wrap in LyTeXTools delimiters.sublime-snippet`.

#### `beginlilypond⇥`

Available as tab trigger and via the command pallette `⌘-⇧-P`. Expands to:

	% \openlytex
	\begin{lilypond}[...]
		...
	\end{lilypond}
	% \closelytex

Press ⇥ to quickly move between the two fillable fields.

#### `lilypondfile⇥`

Available as tab trigger and via the command pallette `⌘-⇧-P`. Expands to:

	% \openlytex
	\lilypondfile[...]{...}
	% \closelytex

Press ⇥ to quickly move between the two fillable fields.

#### `lilypond⇥`

Tab trigger expanding to:

	% \openlytex
	\lilypond[...]{...}
	% \closelytex

Press ⇥ to quickly move between the two fillable fields.

#### `openlytex⇥`

Tab trigger expanding to `% \openlytex`.

#### `closelytex⇥`

Tab trigger expanding to `% \closelytex`.

### Error reporting

All output of the `lilypond-book` (pre-processing) stage is flushed to `./lilypond-book.log` within the directory that LyTeXTools were invoked from. Building is aborted if any errors are encountered during this stage. Otherwise, all pre-processed content is passed on to LaTeX, with errors thereby handled by the log parser provided with the original LaTeXTools.

## Version history

**3 October 2015**
- UPDATED: The build engine now assumes that the system is running OS X El Capitan (10.11.x). If you are still using an older version of OS X, and LyTeXTools has stopped working, please read [Path Considerations].

**18 June 2014**
- FIXED: A bug that prevented LyTeXTools from detecting that compilation has been completed.

**12 Jan 2014**
- NEW: Sublime Text 3 is now supported.
- NEW: All the latest [LaTeXTools](http://github.com/SublimeText/LaTeXTools) features.
- FIXED: Minor bugs.

**1 Sep 2013**
- FIXED: A regression that prevented polltexmk.sh (a core LyTeXTools script) from running, possibly resulting in spurious build errors and a premature termination of the build engine.

**29 May 2013**
- IMPROVED: Scope names are now rationalized, facilitating future development.
- FIXED: A regression that caused L**a**TeXTools snippets and autocompletions to be unavailable in LyTeX documents.
- FIXED: Other small issues.

**8 April 2013**

- NEW: Added syntax definition for `.lytex` documents. Embedded LilyPond code will now be highlighted (depends on the [SubLilyPond](https://www.github.com/yrammos/SubLilyPond) package).
- FIXED: Snippet typo.

**14 March 2013**

- NEW: Added snippets and autocompletions for LilyPond content within `.lytex` documents.
- FIXED: Rare SyncTeX-related bug.

**10 March 2013**

- NEW: LilyPond scopes are now expected to be manually wrapped within the `% \openlytex` and `% \closelytex` delimiters.
- NEW: LilyPond-book output is now logged for reference in case of errors.
- NEW: Merged the latest commit of LaTeXTools (#07335).
- IMPROVED: Cleaned up SyncTeX-related code.
- FIXED: SyncTeX functionality is now more robust (please contact me in case you encounter issues).

**31 August 2012**

- FIXED: "Open PDF" command (by default bound to `Shift-Command-B`) now works with `.lytex` files.

**30 July 2012**

- NEW: First release.

Copyright © 2012-3 by [Yannis Rammos](twitter.com/yannisrammos). This work is made available under the terms of the Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) license, <http://creativecommons.org/licenses/by-sa/3.0/>.
