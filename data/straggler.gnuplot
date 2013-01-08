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

set ylabel "Time (Seconds)"
set xlabel "Number of Tasks"
set bars small
set datafile separator ","
set output "straggler.pdf"
set style fill noborder pattern 3
f(x) = m*x + b
set xrange [40:10000]
set yrange [0:140]
set key top right
set xtics (10,50, 100, 250, 500, 1000, 2500, 5000, 10000)
#fit f(x) "sorted-log" using 5:6 via m, b
#plot "sorted-log" using 5:6 w points lc -1 lt 1 pt 8  title "Time vs Loss", \
#     f(x) w lines lc 9 lt 1 title "Fit line"
#set log x
# processed_stragglers.csv
set log x
#plot "procstragglers" using 1:2 w linespoints pt 1 lc -1 lt 1 lw 2 title "Time per Task"
plot "procstragglers" using 1:2:3 w yerrorbars lc -1 lt -1 lw 1 title "",\
  "procstragglers" using 1:2 w linespoints pt 12 lc -1 lt 0 lw 2 title "Time per Task"
#plot "procstragglers" using 1:3:2 w yerrorbars lc -1
