
import java.util.Random;

public class Quicksort{
    public static void main(String[] args) {
//        int arr[] = {14, 4, 4, 4, 1};
        Quicksort q= new Quicksort();
//        quicksort_demo.quickSort(arr, 0, arr.length - 1);
//        for (int i : arr) {
//            System.out.print(i + ",");
//        }
        for (int i = 0; i < 1000000; i++) {
            int a = quicksort_demo.getPivotIndex(10, 20);
            if (a < 10 || a > 20) {
                System.out.println("error");
            }
        }
    }

    public void quickSort(int arr[], int low, int high) {
        if (low < high) {
            int index = partition(arr, low, high);
            quickSort(arr, low, index - 1);
            quickSort(arr, index + 1, high);
        }
    }

    public int partition(int[] arr, int low, int high) {
        int pivotIndex = getPivotIndex(low, high);
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++; // i增加的次数即为比pivot小的次数,所以我们把它放到小的那一堆，即遍历到的和arr[i]交换
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
//       //把arr[high]即pivot放到正确的位置。从[low,i]均为比pivot小
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;
    }

    //    https://stackoverflow.com/questions/363681/how-do-i-generate-random-integers-within-a-specific-range-in-java
    private int getPivotIndex(int low, int high) {
        int x = new Random().nextInt(high - low + 1) + low;
//        int x = ThreadLocalRandom.current().nextInt(low,high+1);
//        System.out.println(x);
        return x;

    }
}
