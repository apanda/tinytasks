# Note you need gnuplot 4.4 for the pdfcairo terminal.

set terminal pdfcairo dashed font "Gill Sans, 28" linewidth 6 rounded enhanced

# Line style for axes
set style line 80 lt 1 lc rgb "#808080"

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80 # Remove border on top and right.  These
# borders are useless and make it harder to see plotted lines near the border.
# Also, put it in grey; no need for so much emphasis on a border.

set xtics nomirror
set ytics nomirror

set ylabel "Cumulative Fraction"
set xlabel "Improvement in Job Completion Time"
set bars small
set datafile separator ","
set output "binpacked1-sep-avg.pdf"
set style fill noborder pattern 3
f(x) = m*x + b
set xrange [1:10]
set key bottom right
#fit f(x) "sorted-log" using 5:6 via m, b
#plot "sorted-log" using 5:6 w points lc -1 lt 1 pt 8  title "Time vs Loss", \
#     f(x) w lines lc 9 lt 1 title "Fit line"
#set log x
plot "binpacking-separated-inv-multi-avg1"  using 1:(1./43733.) s cumul lc 3 lt 0 lw 2 title "1 - 9 Tasks",\
     "binpacking-separated-inv-multi-avg10"  using 1:(1./8072.) s cumul lc -1 lt 1 lw 2 title "10 - 99 Tasks",\
     "binpacking-separated-inv-multi-avg100"  using 1:(1./3171.) s cumul lc 1 lt 2 lw 2 title "100+ Tasks"
