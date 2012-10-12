
class ExampleProfile {
	private static void hello(String name) {
		System.out.print("Hello "+name);
	}
	public static void exclaim() {
		System.out.println("!");
	}
	public static void die() throws Exception {
		throw new Exception("This is a test");
	}
	public static void main(String[] args) {
		hello("world");
		exclaim();
		try {die();}
		catch(Exception e) {}
	}
}
