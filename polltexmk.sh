#! /bin/bash
pidlist=`pidof perl xetex xelatex latexmk latex biber lilypond lilypond-book python`
echo -e "\n\npidlist = $pidlist\n\n"
while [ -n "$pidlist" ]; do
  for pid in `echo $pidlist`; do
    echo -e "invoking kill on $pid..."
    while kill -0 "$pid"; do
      sleep 1.5 
    done 
  done
pidlist=`pidof perl xetex xelatex latexmk latex biber lilypond lilypond-book python`
echo -e "\n\npidlist = $pidlist\n\n"
done
