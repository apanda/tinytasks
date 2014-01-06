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

def main(argv):
  file_prefix = argv[0]
  print "Parsing logs for %s" % file_prefix

  # List of tuples, where the first item is the time and the second
  # item is 1 if a task started at that time and -1 if a task
  # finished at that time.
  task_events = []

  # Time, CPU usage tuples.
  user_cpu_usage = []
  sys_cpu_usage = []
  total_cpu_usage = []

  results_file = open("%s.log" % file_prefix)
  for line in results_file:
    if line.find("Task run") != -1:
      items = line.split(" ")
      start_time = int(items[7])
      task_events.append((start_time, 1))
      end_time = int(items[9][:-1])
      task_events.append((end_time, -1))
    elif line.find("CPU utilization") != -1:
      items=  line.split(" ")
      time = int(items[4])
      user_cpu_usage.append((time, items[8]))
      sys_cpu_usage.append((time, items[10]))
      total_cpu_usage.append((time, items[12]))

  # Output file with number of running tasks.
  task_events.sort(key = lambda x: x[0])
  running_tasks_filename = "%s.running_tasks" % file_prefix
  running_tasks_file = open(running_tasks_filename, "w")
  running_tasks = 0
  earliest_time = int(task_events[0][0])
  for (time, event) in task_events:
    # Plot only the time delta -- makes the graph much easier to read.
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))
    running_tasks += event
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))

  # Output CPU usage files.
  user_cpu_filename = "%s.user_cpu" % file_prefix
  write_output_data(user_cpu_filename, user_cpu_usage, earliest_time)
  sys_cpu_filename = "%s.sys_cpu" % file_prefix
  write_output_data(sys_cpu_filename, sys_cpu_usage, earliest_time)
  total_cpu_filename = "%s.total_cpu" % file_prefix
  write_output_data(total_cpu_filename, total_cpu_usage, earliest_time)


  # Warning: this graph ends up looking like a comb -- since the time in between task launches is
  # short relative to task runtime.
  running_tasks_plot_file = open("%s_running_tasks_cpu.gp" % file_prefix, "w")
  write_template(running_tasks_plot_file)
  running_tasks_plot_file.write("set xlabel \"Time\"\n")
  running_tasks_plot_file.write("set output \"%s_running_tasks_cpu.pdf\"\n\n" % file_prefix)
  running_tasks_plot_file.write(
    ("plot \"%s\" using 1:2 w l ls 1 title \"Running tasks\" axes x1y1,\\\n" %
      running_tasks_filename))
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 2 title \"User CPU\" axes x1y2,\\\n" %
      user_cpu_filename))
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 3 title \"System CPU\" axes x1y2,\\\n" %
      sys_cpu_filename))
  running_tasks_plot_file.write(
    ("\"%s\" using 1:2 w l ls 4 title \"Total CPU\" axes x1y2\n" %
      total_cpu_filename))

if __name__ == "__main__":
  main(sys.argv[1:])