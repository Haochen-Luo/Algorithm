若干时间后自己有些了一个版本，把merge和sort拆开来，不是死记硬背的
```java
class Solution {
    static int tmp[];
    public int[] sortArray(int[] arr) {
        tmp = new int[arr.length];
        mergeSort(arr, 0, arr.length - 1);
        return arr;
    }
   
    public static void mergeSort(int[] arr, int l, int r) {
        if (l >= r) {
            return;
        }
        int i = (l + r) / 2;
        mergeSort(arr, l, i);
        mergeSort(arr, i + 1, r);
        merge(arr, l, i, i + 1, r);
    }

    public static void merge(int[] arr, int l1, int l2, int r1, int r2) {
        int left = l1;
        int right = r1;
        int index = l1;
        while (left <= l2 && right <= r2) {
            if (arr[left] < arr[right]) {
                tmp[index++] = arr[left++];
            } else {
                tmp[index++] = arr[right++];
            }
        }
        while (right <= r2) {
            tmp[index++] = arr[right++];
        }
        while (left <= l2) {
            tmp[index++] = arr[left++];
        }
        for (int i = l1; i <= r2; i++) {
            arr[i] = tmp[i];
        }
    }


}
```
