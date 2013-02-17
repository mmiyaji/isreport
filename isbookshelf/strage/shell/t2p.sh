#!/bin/sh                                                                                                               
TEMPLATE=template
INTERMED=temp

sed -e 's/PATTERN/'''$1'''/g' $TEMPLATE.tex > $INTERMED.tex

platex $INTERMED.tex
dvips -E -Ppdf -x 5000 $INTERMED.dvi -o $INTERMED.eps
convert $INTERMED.eps $2.png
rm -rf $INTERMED{.aux,.dvi,.eps,.log,.tex}