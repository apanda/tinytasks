set terminal pdfcairo font 'Gill Sans,20' linewidth 6 dashed rounded dashlength 1
set style line 80 lt 1 lc rgb "#808080"
set style line 81 lt 0 # dashed
set style line 81 lt rgb "#808080"  # grey
set grid back linestyle 81
set border 3 back linestyle 80
set xtics nomirror
set ytics nomirror
set key bottom
set style line 1 lt rgb "#E41A1C" lw 2 pt 1
set style line 3 lt rgb "#377EB8" lw 2 pt 6
set style line 2 lt rgb "#4DAF4A" lw 2 pt 2
set style line 4 lt rgb "#984EA3" lw 2 pt 9
set output 'skew_results.pdf'
set xlabel 'Machine Load (Relative to Average)' offset 0,0.5
set ylabel 'Cumulative Probability' offset 1.5
plot 'skew_results_100000' using 2:1 with l lt 1 title 'Multiplier=1',\
'skew_results_200000' using 2:1 with l lt 2 title 'Multiplier=2',\
'skew_results_500000' using 2:1 with l lt 3 title 'Multiplier=5',\
'skew_results_1000000' using 2:1 with l lt 4 title 'Multiplier=10'