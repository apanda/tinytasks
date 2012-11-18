import bisect
import math
import random
import sys

""" from http://code.activestate.com/
         recipes/511478-finding-the-percentile-of-the-values/ """
def get_percentile(N, percent, key=lambda x:x):
    """ Find the percentile of a list of values.

    Args:
        percent: a float value from 0.0 to 1.0.
        key: optional key function to compute value from each element of N.

    Returns:
        The percentile of the values
    """
    if not N:
        return 0
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1

def add_task(current_time, avg_task_completion_time, task_completion_times):
    task_completion_time = random.expovariate(1.0 / avg_task_completion_time)
    #task_completion_time = avg_task_completion_time
    position = bisect.bisect(task_completion_times,
                             current_time + task_completion_time)
    bisect.insort(task_completion_times, current_time + task_completion_time)
    return task_completion_time

def simulate(total_slots, total_tasks, avg_task_completion_time):
    # Sorted list of times when tasks will complete.
    task_completion_times = []
    
    current_time = 0
    total_time = 0
    # Fill task_completion_times with total_slots tasks.
    while len(task_completion_times) < min(total_tasks, total_slots):
        total_time += add_task(current_time, avg_task_completion_time,
                               task_completion_times)

    started_tasks = total_slots
    completed_tasks = 0
    # Store this as a sanity check.
    while completed_tasks < total_tasks:
        current_time = task_completion_times.pop(0)
        if started_tasks < total_tasks:
            total_time += add_task(current_time, avg_task_completion_time,
                                   task_completion_times)
            started_tasks += 1
        completed_tasks += 1

    return total_time, current_time

def write_gnuplot_template(file):
    file.write("set terminal pdfcairo font 'Gill Sans,20' linewidth 4 "
               "dashed rounded dashlength 2\n")
    file.write("set style line 80 lt 1 lc rgb \"#808080\"\n")
    file.write("set style line 81 lt 0 # dashed\n")
    file.write("set style line 81 lt rgb \"#808080\"  # grey\n")
    file.write("set grid back linestyle 81\n")
    file.write("set border 3 back linestyle 80\n")
    file.write("set xtics nomirror\n")
    file.write("set ytics nomirror\n")
    file.write("set key left\n")

    file.write("set style line 1 lt rgb \"#E41A1C\" lw 2 pt 1\n")
    file.write("set style line 3 lt rgb \"#377EB8\" lw 2 pt 6\n")
    file.write("set style line 2 lt rgb \"#4DAF4A\" lw 2 pt 2\n")
    file.write("set style line 4 lt rgb \"#984EA3\" lw 2 pt 9\n")

    file.write("set output 'results.pdf'\n")
    file.write("set xlabel 'Total # Tasks' offset 0,0.5\n")
    file.write("set ylabel 'Job Completion Time' offset 1.5\n")
    file.write("plot ")

def main(argv):
    num_iterations = 100
    # Total work, defined in terms of ms of things that need to be done. This 
    # number has no real meaning (since it's alllll relative).
    total_work = 100000
    total_slots = 100
    slots_values = [1, 2, 5, 10, 100, 1000, 10000]

    #gnuplot_file = open("results.gp", "w")
    #write_gnuplot_template(gnuplot_file)

    for index, total_slots in enumerate(slots_values):
        gnuplot_file = open("results_%s.gp" % total_slots, "w")
        write_gnuplot_template(gnuplot_file)

        results_filename = "results_%s" % total_slots
        results_file = open(results_filename, "w")
        results_file.write("Index\tTotalTasks\tAvgTotalComputeTime\tAvgCompletionTime"
                           "\t50th\t5th(relative)\t50th(relative)\t"
                           "95th(relative)\n")
        total_tasks_values = [total_slots, 2*total_slots, 5*total_slots,
                              10*total_slots, 100*total_slots, 1000*total_slots]
        # Keep track of the completion time with total_slots tasks, in order
        # to normalize everything.
        longest_completion_time = 0

        for tasks_index, total_tasks in enumerate(total_tasks_values):
            avg_completion_time = total_work / (total_tasks * 1.0)
            completion_times = []
            total_completion_time = 0
            total_time = 0
            while len(completion_times) < num_iterations:
                time, completion_time = simulate(total_slots, total_tasks,
                                                 avg_completion_time)
                completion_times.append(completion_time)
                total_completion_time += completion_time
                total_time += time

            completion_times.sort()
            avg_completion_time = total_completion_time * 1.0 / num_iterations
            avg_total_time = total_time * 1.0 / num_iterations
            if total_tasks == total_slots:
                longest_completion_time = (
                        1.0 * get_percentile(completion_times, 0.5))
            relative_5th = (get_percentile(completion_times, 0.05) /
                    longest_completion_time)
            relative_50th = (get_percentile(completion_times, 0.5) /
                    longest_completion_time)
            relative_95th = (get_percentile(completion_times, 0.95) /
                    longest_completion_time)
            results_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %
                               (tasks_index, total_tasks / total_slots, avg_total_time,
                                avg_completion_time,
                                get_percentile(completion_times, 0.5),
                                relative_5th, relative_50th, relative_95th))
        gnuplot_file.write("'%s' using 1:5 with l lt %d title 'Slots=%s',\\\n" %
                           (results_filename, index + 1, total_slots))
        gnuplot_file.write("'%s' using 1:5:4:6 with yerrorbars lt %d notitle" %
                           (results_filename, index + 1))  

if __name__ == "__main__":
    main(sys.argv[1:])
