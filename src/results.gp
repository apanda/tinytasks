set terminal pdfcairo font 'Gill Sans,20' linewidth 4 dashed rounded dashlength 2
set style line 80 lt 1 lc rgb "#808080"
set style line 81 lt 0 # dashed
set style line 81 lt rgb "#808080"  # grey
set grid back linestyle 81
set border 3 back linestyle 80
set xtics nomirror
set ytics nomirror
set key left
set style line 1 lt rgb "#E41A1C" lw 2 pt 1
set style line 3 lt rgb "#377EB8" lw 2 pt 6
set style line 2 lt rgb "#4DAF4A" lw 2 pt 2
set style line 4 lt rgb "#984EA3" lw 2 pt 9
set output 'results.pdf'
set yrange [0:60000]
set xlabel 'Total # Tasks' offset 0,0.5
set ylabel 'Job Completion Time' offset 1.5
plot 'results_1' using 1:5 with l lt 0 title 'Slots=1',\
'results_1' using 1:5:4:6 with yerrorbars lt 0 notitle,\
'results_2' using 1:5 with l lt 1 title 'Slots=2',\
'results_2' using 1:5:4:6 with yerrorbars lt 1 notitle,\
'results_5' using 1:5 with l lt 2 title 'Slots=5',\
'results_5' using 1:5:4:6 with yerrorbars lt 2 notitle,\
'results_10' using 1:5 with l lt 3 title 'Slots=10',\
'results_10' using 1:5:4:6 with yerrorbars lt 3 notitle,\
'results_100' using 1:5 with l lt 4 title 'Slots=100',\
'results_100' using 1:5:4:6 with yerrorbars lt 4 notitle,\
'results_1000' using 1:5 with l lt 5 title 'Slots=1000',\
'results_1000' using 1:5:4:6 with yerrorbars lt 5 notitle,\
'results_10000' using 1:5 with l lt 6 title 'Slots=10000',\
'results_10000' using 1:5:4:6 with yerrorbars lt 6 notitle
