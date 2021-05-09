package Year3.COMP202Alg;

import java.util.ArrayList;
import java.util.Arrays;

public class RSAdemo {
    public static void main(String[] args) {
        gcd(338, 12);
        System.out.println(Arrays.toString(extendedGCD(338, 12)));
        imitateExtendedGCD(412, 260);
    }

    public static void gcd(int a, int b) {
        int small = Math.min(a, b);
        int large = Math.max(a, b);
//        System.out.println(large + " " + small);
        while (small != 0) {
            int temp = large;
            large = small;
            small = temp % small;
//            System.out.println(large + " " + small);
        }
        System.out.println("final result is " + large);
    }

    public static int[] extendedGCD(int a, int b) {
        int small = Math.min(a, b);
        int large = Math.max(a, b);
        if (small == 0) {
            return new int[]{large, 1, 0};
        }
        int r = large % small;
        int q = large / small;
        int[] temp = extendedGCD(small, r);
        return new int[]{temp[0], temp[2], temp[1] - temp[2] * q};
    }

    public static void imitateExtendedGCD(int a, int b) {
        int _a = Math.max(a, b);
        int _b = Math.min(a, b);
        _imitateExtendedGCD(_a, _b);
    }

    public static void _imitateExtendedGCD(int a, int b) {
        ArrayList<Integer> as = new ArrayList<>();
        ArrayList<Integer> bs = new ArrayList<>();
        ArrayList<Integer> qs = new ArrayList<>();
        ArrayList<Integer> rs = new ArrayList<>();
        as.add(a);
        bs.add(b);
        while (b != 0) {
            int temp = a;
            a = b;
            int q = temp / b;
            int r = temp % b;
            b = r;
            as.add(a);
            bs.add(b);
            qs.add(q);
            rs.add(r);
        }
        ArrayList<Integer> js = new ArrayList<>();
        ArrayList<Integer> ks = new ArrayList<>();
        js.add(1);
        ks.add(0);
        for (int i = 0; i < as.size() - 1; i++) {
            int tempJ = js.get(0);
            int tempK = ks.get(0);
            js.add(0, tempK);
            ks.add(0, tempJ - qs.get(as.size() - i - 2) * tempK);
        }
        ArrayList<ArrayList<Integer>> all = new ArrayList<ArrayList<Integer>>(Arrays.asList(as, bs, qs, rs, js, ks));
        for (ArrayList<Integer> i : all) {
            for (int j : i) {
                System.out.printf("|%-4s", j);
//                System.out.printf("|%-4s", j);
            }
            System.out.println();
        }

    }

}
