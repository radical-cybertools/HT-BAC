set border 2 front linetype -1 linewidth 1.000
set boxwidth 0.5 absolute
set style fill solid 0.25 border 
unset key

set pointsize 0.25
set style data boxplot

set ytics nomirror
set xtics border (16, 32, 64, 128, 256, 512, 1024) nomirror autojustify 

set xtics

set title "HT-BAC 'MMPBSA' (fecalc) Benchmarks: Avg. CU Runtimes (stampede)"
set xlabel "Pilot Size (cores)"
set ylabel "Avg. CU Runtime (minutes)"

set timefmt "%S"
set ydata time

plot 'results-per-cu.dat' using 2:($2 == 16   && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 32   && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 64   && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 128  && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 256  && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 512  && $1 == 1 ? $3:1/0) linecolor 5, \
                       '' using 2:($2 == 1024 && $1 == 1 ? $3:1/0) linecolor 5, \
                       \
                       '' using 2:($2 == 16   && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 32   && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 64   && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 128  && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 256  && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 512  && $1 == 2 ? $3:1/0) linecolor 4, \
                       '' using 2:($2 == 1024 && $1 == 2 ? $3:1/0) linecolor 4, \
                       \
                       '' using 2:($2 == 16   && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 32   && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 64   && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 128  && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 256  && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 512  && $1 == 4 ? $3:1/0) linecolor 3, \
                       '' using 2:($2 == 1024 && $1 == 4 ? $3:1/0) linecolor 3, \
                       \
                       '' using 2:($2 == 16   && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 32   && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 64   && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 128  && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 256  && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 512  && $1 == 8 ? $3:1/0) linecolor 2, \
                       '' using 2:($2 == 1024 && $1 == 8 ? $3:1/0) linecolor 2, \
                       \
                       '' using 2:($2 == 16   && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 32   && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 64   && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 128  && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 256  && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 512  && $1 == 16 ? $3:1/0) linecolor 1, \
                       '' using 2:($2 == 1024 && $1 == 16 ? $3:1/0) linecolor 1