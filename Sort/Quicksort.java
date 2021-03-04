class Solution {
  public int[] sortArray(int[] arr) {
        qsort(arr,0,arr.length-1);
        return arr;
    }

    public void qsort(int[] arr, int low, int high) {
      if (low < high) {
        int index = partition(arr, low, high);
        qsort(arr, low,index-1);
        qsort(arr, index+ 1, high);
      }
    }

    public int partition(int arr[], int low, int high) {
        int pivot = arr[high];
        int index = low - 1;
        for (int i = low; i < high; i++) {
            if (arr[i] < pivot) {
                index++;
                swap(arr, i, index);
            }
        }
    //把arr[high]即pivot放到正确的位置。从[low,i]均为比pivot小
        swap(arr,high,index+1);
        return index + 1;
    }

    public void swap(int[] arr, int a, int b) {
        int temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
    }
//      public void quickSort(int arr[], int low, int high) {
//         if (low < high) {
//             int index = partition(arr, low, high);
//             quickSort(arr, low, index - 1);
//             quickSort(arr, index + 1, high);
//         }
//     }

//     public int partition(int[] arr, int low, int high) {
//         int pivot = arr[high];
//         int i = low - 1;
//         for (int j = low; j < high; j++) {
//             if (arr[j] < pivot) {
//                 i++; // i增加的次数即为比pivot小的次数,所以我们把它放到小的那一堆，即遍历到的和arr[i]交换
//                 int temp = arr[i];
//                 arr[i] = arr[j];
//                 arr[j] = temp;
//             }
//         }

//         int temp = arr[i + 1];
//         arr[i + 1] = arr[high];
//         arr[high] = temp;

//         return i + 1;
//     }
}
