import sys

def write_template(f):
  template_file = open("template.gp")
  for line in template_file:
    f.write(line)

def main(argv):
  file_prefix = argv[0]
  print "Parsing logs for %s" % file_prefix

  # List of tuples, where the first item is the time and the second
  # item is 1 if a task started at that time and -1 if a task
  # finished at that time.
  task_events = []

  results_file = open("%s.log" % file_prefix)
  for line in results_file:
    if line.find("Task run") != -1:
      items = line.split(" ")
      start_time = items[7]
      task_events.append((start_time, 1))
      end_time = items[9][:-1]
      task_events.append((end_time, -1))

  task_events.sort(key = lambda x: x[0])
  running_tasks_filename = "%s.running_tasks" % file_prefix
  running_tasks_file = open(running_tasks_filename, "w")
  running_tasks = 0
  earliest_time = task_events[0][0]
  for (time, event) in task_events:
    # Plot only the time delta -- makes the graph much easier to read.
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))
    running_tasks += event
    running_tasks_file.write("%s\t%s\n" % (time - earliest_time, running_tasks))

  # Warning: this graph ends up looking like a comb -- since the time in between task launches is
  # short relative to task runtime.
  running_tasks_plot_file = open("%s_running_tasks.gp" % file_prefix, "w")
  write_template(running_tasks_plot_file)
  running_tasks_plot_file.write("set xlabel \"Time\"\n")
  running_tasks_plot_file.write("set output \"%s_running_tasks.pdf\"\n\n" % file_prefix)
  running_tasks_plot_file.write("plot \"%s\" using 1:2 w l ls 1 title \"Running tasks\"\n" %
    running_tasks_filename)

if __name__ == "__main__":
  main(sys.argv[1:])
