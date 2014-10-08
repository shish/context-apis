
class BailOut extends Exception {}

class ExampleProfile {
	private static final int BOARD_SIZE = 8;

	private static void validate(int[] queens) throws BailOut {
		int left, right, col;
		left = right = col = queens[queens.length-1];
	    for(int n = queens.length-2; n>=0; n--) {
			int r = queens[n];
	        left--;
			right++;
	        if(r == left || r == col || r == right) {
	            throw new BailOut();
			}
		}
	}

	private static int[] add_queen(int[] queens) throws BailOut {
		try {Thread.sleep(10);}
		catch(Exception e) {}

		for(int i=0; i<BOARD_SIZE; i++) {
			int[] test_queens = new int[queens.length + 1];
			for(int n=0; n<queens.length; n++) {
				test_queens[n] = queens[n];
			}
			test_queens[queens.length] = i;

			try {
				validate(test_queens);
				if(test_queens.length == BOARD_SIZE) {
					return test_queens;
				}
				else {
					return add_queen(test_queens);
				}
			}
			catch(BailOut e) {}
		}
		throw new BailOut();
	}

	public static void main(String[] args) {
		int[] queens = new int[0];
		try {
			queens = add_queen(queens);
			for(int n=0; n<queens.length; n++) {
				System.out.print(queens[n]);
			}
			System.out.println("");
		}
		catch(BailOut e) {
			System.out.println("Top-level bail");
		}
//		for(int n=0; n<BOARD_SIZE; n++) {
//			int q = queens[n];
//			System.out.println(". "*q + "Q " + ". "*(BOARD_SIZE - q - 1));
//		}
	}
}
