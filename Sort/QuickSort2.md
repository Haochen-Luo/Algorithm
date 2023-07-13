## 和之前的区别是index是取l

这里的index可以理解为和pivot相比，即将要填充的位置
```java
class Solution {
     public int[] sortArray(int[] arr) {
        quickSort(arr,0,arr.length-1);
        return arr;
    }
    public static void quickSort(int[] arr, int l, int r) {
        if (l >= r) {
            return;
        }
        int i = partition(arr, l, r);
        quickSort(arr, l, i - 1);
        quickSort(arr, i + 1, r);
    }

    public static int partition(int[] arr, int l, int r) {
        int pivot = arr[r];
        int index = l;
        for (int i = l; i < r; i++) {
            //循环l-r次，index最多为l-r-1

            if (arr[i] < pivot) {

                swap(arr, i, index);
                index++;
            }
        }
        swap(arr, index, r);
        return index;

    }

    public static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }


}
```
