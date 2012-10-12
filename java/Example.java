
class Example {

  private static void hello() {
    try {Thread.sleep( 300);} catch (Exception e) {}
    Context.start("saying hello");
    System.out.print("hello ");
    try {Thread.sleep(800);} catch (Exception e) {}
    Context.endok("finished hello");
  }

  private static void world(int i) {
    for (int j=0 ; j<i ; j++) {
      Context.start("saying world", j);
      System.out.print("world");
      try {Thread.sleep(500);} catch (Exception e) {}
      Context.endok("");
    }
    System.out.println();
  }

  public static void main(String[] args) throws java.net.MalformedURLException {
    Context.setLog("file://output.java.ctxt");
    Context.start("running program with args:", args);

    (new Thread(new Runnable() {public void run() {
      hello();
    }})).start();

    world(3);

    Context.endok("running program finished");
    Context.closeLog();
  }

}
