import sys

def write_template(f):
  template_file = open("template.gp")
  for line in template_file:
    f.write(line)

def write_output_data(filename, data, earliest_time):
  f = open(filename, "w")
  for (time, x) in data:
    f.write("%s\t%s\n" % (time - earliest_time, x))
  f.close()

def write_running_tasks_plot(file_prefix, y2label, output_filename, running_tasks_plot_file,
    running_tasks_filename):
  # Warning: this graph ends up looking like a comb -- since the time in between task launches is
  # short relative to task runtime.
  running_tasks_plot_file.write(
    "# Must be plotted from the parent directory for links to work correctly\n")
  write_template(running_tasks_plot_file)
  running_tasks_plot_file.write("set xlabel \"Time (ms)\"\n")
  running_tasks_plot_file.write("set xrange [0:100000]\n")
  running_tasks_plot_file.write("set y2tics\n")
  running_tasks_plot_file.write("set y2label \"%s\"\n" % y2label)
  running_tasks_plot_file.write("set output \"%s/%s.pdf\"\n\n" % (file_prefix, output_filename))
  running_tasks_plot_file.write(
    ("plot \"%s\" using 1:2 w l ls 1 title \"Running tasks\" axes x1y1,\\\n" %
      running_tasks_filename))

def main(argv):
  file_prefix = argv[0].strip("/")
  print "Parsing logs in directory %s" % file_prefix

  # List of tuples, where the first item is the time and the second
  # item is 1 if a task started at that time and -1 if a task
  # finished at that time.
  task_events = []

  # Time, CPU usage tuples.
  user_cpu_usage = []
  sys_cpu_usage = []
  total_cpu_usage = []

  # Time, IO rate tuples
  rchar = []
  rbytes = []
  wchar = []
  wbytes = []

  # Time, network traffic tuples.
  trans_bytes = []
  trans_packets = []
  recv_bytes = []
  recv_packets = []
  
  BYTES_PER_MB = 1048576

  task_durations = []

  results_file = open("%s/%s.log" % (file_prefix, file_prefix))
  for line in results_file:
    if line.find("Task run") != -1:
      items = line.split(" ")
      start_time = int(items[7])
      task_events.append((start_time, 1))
      end_time = int(items[9][:-1])
      task_events.append((end_time, -1))
      task_durations.append(end_time - start_time)
    elif line.find("CPU utilization") != -1:
      items = line.split(" ")
      time = int(items[4])
      user_cpu_usage.append((time, float(items[8])))
      sys_cpu_usage.append((time, float(items[10])))
      total_cpu_usage.append((time, float(items[12][:-1])))
    elif line.find("rchar") != -1:
      items = line.split(" ")
      time = int(items[4])
      rchar.append((time, float(items[7]) / BYTES_PER_MB))
      rbytes.append((time, float(items[13]) / BYTES_PER_MB))
      wchar.append((time, float(items[10]) / BYTES_PER_MB))
      wbytes.append((time, float(items[16][:-1]) / BYTES_PER_MB))
    elif line.find("trans rates") != -1:
      items = line.strip("\n").split(" ")
      time = int(items[4])
      trans_bytes.append((time, float(items[7]) / BYTES_PER_MB))
      trans_packets.append((time, float(items[9])))
      recv_bytes.append((time, float(items[13]) / BYTES_PER_MB))
      recv_packets.append((time, float(items[15])))

  # Output file with number of running tasks.
  task_events.sort(key = lambda x: x[0])
  running_tasks_filename = "%s/running_tasks" % file_prefix
  running_tasks_file = open(running_tasks_filename, "w")
  running_tasks = 0
  earliest_time = int(task_events[0][0])
  latest_time = int(task_events[-1][0])
  for (time, event) in task_events:
    # Plot only the time delta -- makes the graph much easier to read.
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))
    running_tasks += event
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))

  # Output CPU usage data.
  user_cpu_filename = "%s/user_cpu" % file_prefix
  write_output_data(user_cpu_filename, user_cpu_usage, earliest_time)
  sys_cpu_filename = "%s/sys_cpu" % file_prefix
  write_output_data(sys_cpu_filename, sys_cpu_usage, earliest_time)
  total_cpu_filename = "%s/total_cpu" % file_prefix
  write_output_data(total_cpu_filename, total_cpu_usage, earliest_time)
  
  # Print average CPU usage during time when tasks were running. This assumes that
  # all the measurement intervals were the same.
  filtered_user_cpu_usage = filter(
    lambda x: x[0] >= earliest_time and x[0] <= latest_time, user_cpu_usage)
  print "Average user CPU use:"
  print sum([pair[1] for pair in filtered_user_cpu_usage]) * 1.0 / len(filtered_user_cpu_usage)

  filtered_total_cpu_usage = filter(
    lambda x: x[0] >= earliest_time and x[0] <= latest_time, total_cpu_usage)
  print "Average total CPU use:"
  print sum([pair[1] for pair in filtered_total_cpu_usage]) * 1.0 / len(filtered_total_cpu_usage)

  # Output job duration ESTIMATE (just last task end - first task start; this is just one worker
  # so not totally accurate) and average task duration.
  print "Job duration ESTIMATE (ms): ", latest_time - earliest_time
  print "Average task duration (ms): ", sum(task_durations) * 1.0 / len(task_durations)

  # Output IO usage data.
  rchar_filename = "%s/rchar" % file_prefix
  write_output_data(rchar_filename, rchar, earliest_time)
  rbytes_filename = "%s/rbytes" % file_prefix
  write_output_data(rbytes_filename, rbytes, earliest_time)
  wchar_filename = "%s/wchar" % file_prefix
  write_output_data(wchar_filename, wchar, earliest_time)
  wbytes_filename = "%s/wbytes" % file_prefix
  write_output_data(wbytes_filename, wbytes, earliest_time)

  # Output network data.
  trans_bytes_filename = "%s/trans_bytes" % file_prefix
  write_output_data(trans_bytes_filename, trans_bytes, earliest_time)
  trans_packets_filename = "%s/trans_packets" % file_prefix
  write_output_data(trans_packets_filename, trans_packets, earliest_time)
  recv_bytes_filename = "%s/recv_bytes" % file_prefix
  write_output_data(recv_bytes_filename, recv_bytes, earliest_time)
  recv_packets_filename = "%s/recv_packets" % file_prefix
  write_output_data(recv_packets_filename, recv_packets, earliest_time)

  # Output one file with running tasks, CPU, and IO usage.
  running_tasks_plot_file = open("%s/running_tasks_cpu.gp" % file_prefix, "w")
  write_running_tasks_plot(file_prefix, "MB", "running_tasks_cpu", running_tasks_plot_file,
    running_tasks_filename)
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 2 title \"User CPU\" axes x1y1,\\\n" %
      user_cpu_filename))
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 3 title \"System CPU\" axes x1y1,\\\n" %
      sys_cpu_filename))
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 4 title \"Total CPU\" axes x1y1,\\\n" %
      total_cpu_filename))
  running_tasks_plot_file.write(
    "\"%s\" using 1:2 w l ls 5 title \"rchar\" axes x1y2,\\\n" % rchar_filename)
  running_tasks_plot_file.write(
    "\"%s\" using 1:2 w l ls 6 title \"wchar\" axes x1y2\n" % wchar_filename)
  # Comment these out 'till I figure out what rbytes/wbytes actually are.
  #running_tasks_plot_file.write(
  #  "\"%s\" using 1:2 w l ls 7 title \"rbytes\" axes x1y2,\\\n" % rbytes_filename)
  #running_tasks_plot_file.write(
  #  "\"%s\" using 1:2 w l ls 8 title \"wbytes\" axes x1y2\n" % wbytes_filename)

  # Output two network files: one with bytes and another with packets.
  network_plot_file = open("%s/running_tasks_network_bytes.gp" % file_prefix, "w")
  write_running_tasks_plot(file_prefix, "MB", "running_tasks_network_bytes",
    network_plot_file, running_tasks_filename)
  network_plot_file.write(
    ("\"%s\" using 1:2 w l ls 2 title \"Transmitted bytes\" axes x1y2,\\\n" %
      trans_bytes_filename))
  network_plot_file.write(
    "\"%s\" using 1:2 w l ls 3 title \"Received bytes\" axes x1y2\n" % recv_bytes_filename)

  network_plot_file = open("%s/running_tasks_network_packets.gp" % file_prefix, "w")
  write_running_tasks_plot(file_prefix, "packets", "running_tasks_network_packets",
    network_plot_file, running_tasks_filename)
  network_plot_file.write(
    ("\"%s\" using 1:2 w l ls 2 title \"Transmitted packets\" axes x1y2,\\\n" %
      trans_packets_filename))
  network_plot_file.write(
    "\"%s\" using 1:2 w l ls 3 title \"Received packets\" axes x1y2\n" % recv_packets_filename)


if __name__ == "__main__":
  main(sys.argv[1:])
