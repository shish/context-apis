import java.net.InetAddress;
import java.lang.management.ManagementFactory;
import java.text.DecimalFormat;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import java.net.URL;
import java.net.MalformedURLException;

class Context {

  //----------------------------------------------------------------
  // Private Variables
  //----------------------------------------------------------------

  private static DecimalFormat  time_formater = new DecimalFormat("0.000000");
  private static double         nano_offset   = System.currentTimeMillis()/1000D - System.nanoTime()/1000000000D;
  private static BufferedWriter log_file      = null;

  //----------------------------------------------------------------
  // Private Methods
  //----------------------------------------------------------------

  private static String getTime() {
    return time_formater.format(nano_offset + (System.nanoTime()/1000000000D));
  }

  private static String getMethodName(final int stack_depth_up) {
    return Thread.currentThread().getStackTrace()[stack_depth_up].getMethodName();
  }

  private static String genMsg(String text, String type) {
    String   time       = getTime();
    String[] pid_string = java.lang.management.ManagementFactory.getRuntimeMXBean().getName().split("@");
    StringBuffer msg    = new StringBuffer();
    msg.append(time);          // time
    msg.append(" ");
    msg.append(pid_string[1]); // host
    msg.append(" ");
    msg.append(pid_string[0]); // pid
    msg.append(" ");
    msg.append(Thread.currentThread().getName().replace(" ","-")); // thread
    msg.append(" ");
    msg.append(type);          // type (START, ENDOK, BMARK, etc)
    msg.append(" ");
    msg.append(getMethodName(4)); // function name
    msg.append(" ");
    msg.append(text);          // text
    msg.append("\n");
    return msg.toString();
  }

  private static void compactStringBuffer(StringBuffer text, Object o) {
      if (o.getClass().isArray()) {
        for (Object oo : (Object[])o) {
          compactStringBuffer(text, oo);
        }
      }
      else {
        text.append(o.toString());
        text.append(" ");
      }
  }
  private static String compactStrings(Object[] objs) {
    StringBuffer text = new StringBuffer();
    compactStringBuffer(text, objs);
    return text.toString();
  }
  
  private static synchronized void logMsg(String msg) {
    try {
      if (log_file != null) {log_file.write(msg);}
      else                  {System.out.print(msg);}
    }
    catch (IOException e) {
      System.err.println("Unable to write to log file " + e.getMessage());
      closeLog();
    }
  }

  //----------------------------------------------------------------
  // Public Methods
  //----------------------------------------------------------------

  public static void setLog(String filename) throws MalformedURLException {
  	setLog(new URL(filename));
  }

  public static void setLog(URL url) {
    try {
		if(url.getProtocol().equals("file")) {
	      log_file = new BufferedWriter(new FileWriter(url.getHost() + url.getPath(), false));
		}
		else {
		}
    }
    catch (IOException e){
      System.err.println("Unable to open log file: " + e.getMessage());
    }
  }
  public static void closeLog() {
      try {log_file.close();} catch (Exception e) {}
      log_file = null;
  }

  public static void start(Object... text) {logMsg(genMsg(compactStrings(text), "START"));}
  public static void endok(Object... text) {logMsg(genMsg(compactStrings(text), "ENDOK"));}
  public static void ender(Object... text) {logMsg(genMsg(compactStrings(text), "ENDER"));}
  public static void bmark(Object... text) {logMsg(genMsg(compactStrings(text), "BMARK"));}
  public static void clear(Object... text) {logMsg(genMsg(compactStrings(text), "CLEAR"));}

}
