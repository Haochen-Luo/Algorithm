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
        int pivotIndex = getPivotIndex(low, high);
        swap(arr,pivotIndex,high);
        int pivot = arr[high];
        int index = low - 1;
        for (int i = low; i < high; i++) {
            if (arr[i] < pivot) {
                index++;
                swap(arr, i, index);
            }
        }
        swap(arr,high,index+1);
        return index + 1;
    }

    public void swap(int[] arr, int a, int b) {
        int temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
    }
  //    https://stackoverflow.com/questions/363681/how-do-i-generate-random-integers-within-a-specific-range-in-java
     private int getPivotIndex(int low, int high) {
        // int x = new Random().nextInt(high - low + 1) + low;
       int x = ThreadLocalRandom.current().nextInt(low,high+1);
        return x;

    }

}
