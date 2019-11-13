import java.util.*;

public class Main {

    private static LinkedList<Object> list;

    public static void main (String[] args) {
            list = new LinkedList<>();
            for(int i = 0; i < 0x1000000; i++){
                        list.add(new Object[256]);
                    }
            Scanner input = new Scanner(System.in);
            System.out.println(input.nextInt() + input.nextInt());
        }
}
