public class Mergesort {

    void merge_sort(int arr[], int low, int high) {
        if (low >= high) return;

        int mid = (low + high) / 2;
        merge_sort(arr, low, mid);
        merge_sort(arr, mid + 1, high);
        merge(arr, low, mid, high);
    }

    void merge(int[] arr, int low, int mid, int high) {
        int[] tmp = new int[high - low + 1];
        int k = 0, i = low, j = mid + 1;
        while (i <= mid && j <= high)
            if (arr[i] <= arr[j]) tmp[k++] = arr[i++];
            else tmp[k++] = arr[j++];

        while (i <= mid) tmp[k++] = arr[i++];
        while (j <= high) tmp[k++] = arr[j++];

        for (i = low, j = 0; i <= high; i++, j++) arr[i] = tmp[j];

    }
    
}
