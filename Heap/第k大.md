https://leetcode-cn.com/problems/kth-largest-element-in-an-array/submissions/

```java

 public  int findKthLargest(int[] nums, int k) {
        buildHeap(nums, nums.length - 1);
        int size = nums.length - 1;
        for (int i = nums.length - 1; i >= nums.length - k ; i--) {

            swap(nums, 0, i);
           
            size--;
            maxHeap(nums, 0, size);
        }
        return nums[nums.length - k];
    }


    public static void buildHeap(int arr[], int size) {
        for (int i = size / 2; i >= 0; i--) {
            maxHeap(arr, i, size);
        }
    }

    public static void maxHeap(int arr[], int i, int size) {
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        int largest = i;
        if (l <= size && arr[l] > arr[largest]) {
            largest = l;
        }
        if (r <= size && arr[r] > arr[largest]) {
            largest = r;
        }
        if (largest != i) {
            swap(arr, i, largest);
            maxHeap(arr, largest, size);
        }
    }

    public static void swap(int arr[], int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
```
