```java
package Year3.COMP202Alg;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;

public class weightedInterval {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new FileReader("E:\\intellij\\src\\Year3\\COMP202Alg\\weightdp.txt"));
        int count = 0;
        String s;
        while ((s = bufferedReader.readLine()) != null) {
            count++;
        }
        bufferedReader.close();
        bufferedReader = new BufferedReader(new FileReader("E:\\intellij\\src\\Year3\\COMP202Alg\\weightdp.txt"));
        int ii = 0;
        int[][] arr = new int[count][4];
        while ((s = bufferedReader.readLine()) != null) {
            String[] strings = s.split(" ");
//            System.out.println(Arrays.toString(strings));
            arr[ii][1] = Integer.parseInt(strings[0]);
            arr[ii][2] = Integer.parseInt(strings[1]);
            arr[ii][3] = Integer.parseInt(strings[2]);
            System.out.println(Arrays.toString(arr[ii]));
            ii++;

        }
        System.out.println("______");
        Arrays.sort(arr, Comparator.comparingInt(o -> o[2]));
        for (int i = 0; i < count; i++) {
            arr[i][0] = i + 1;
            System.out.println(Arrays.toString(arr[i]));
        }
        int[] p = new int[count + 1];
        for (int i = 1; i <= count; i++) {
            for (int j = i - 1; j > 0; j--) {
                if (arr[j - 1][2] <= arr[i - 1][1]) {
                    p[i] = j;
                    break;
                }
            }
        }
        int maxVal = Integer.MIN_VALUE;
        int[] opt = new int[count + 1];
        for (int i = 1; i <= count; i++) {
            opt[i] = Math.max(opt[i - 1], arr[i - 1][3] + opt[p[i]]);
            maxVal = Math.max(maxVal, opt[i]);
        }
        System.out.println(maxVal);

    }
}

```
