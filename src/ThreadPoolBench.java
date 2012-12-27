import java.util.concurrent.*;

class ThreadPoolBench {
  private static volatile int counter = 0;

  public static void main(String args[]) throws Exception {
    if (args.length != 2) {
      System.err.println("Usage: ThreadPoolBench <thread_pool_size> <num_tasks>");
      System.exit(0);
    }
    int threadPoolSize = Integer.valueOf(args[0]);
    int numTasks = Integer.valueOf(args[1]);
    ExecutorService execService = Executors.newFixedThreadPool(threadPoolSize);
    long start = System.nanoTime();

    System.err.println("Start " + start);

    Runnable task = new Runnable() {
      @Override
      public void run() {
        counter++;
      }
    };

    for (int i = 0; i < numTasks; ++i) {
      execService.submit(task);
    }

    execService.shutdown();
    // Wait at most 1ms per task ?
    execService.awaitTermination(numTasks, TimeUnit.MILLISECONDS);
    long end = System.nanoTime();
    System.err.println("End " + end);
    System.err.println("Total Time taken " + (end-start) + " ns");
    System.err.println("Per-task Time taken " + (end-start)/numTasks + " ns");
    System.err.println("Final Counter value is " + counter);
  }
}
