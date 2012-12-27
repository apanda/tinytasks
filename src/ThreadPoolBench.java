import java.util.concurrent.*;

class ThreadPoolBench {

  public static final int THREAD_POOL_SIZE = 1;
  public static final int NUM_TASKS = 1000000;

  public static void main(String args[]) throws Exception {
    ExecutorService execService = Executors.newFixedThreadPool(1);
    long start = System.nanoTime();
    System.err.println("Start " + start);

    Runnable task = new Runnable() {
      @Override
      public void run() {
        System.out.println(System.nanoTime());
      }
    };

    for (int i = 0; i < NUM_TASKS; ++i) {
      execService.submit(task);
    }

    execService.shutdown();
    // Wait at most 1ms per task ?
    execService.awaitTermination(NUM_TASKS, TimeUnit.MILLISECONDS);
    long end = System.nanoTime();
    System.err.println("End " + end);
    System.err.println("Total Time taken " + (end-start) + " ns");
    System.err.println("Per-task Time taken " + (end-start)/NUM_TASKS + " ns");
  }
}
