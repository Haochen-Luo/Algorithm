class Solution {
    int count = 0;
    public int reversePairs(int[] nums) {
        sort(nums, 0, nums.length - 1);
        return count;
    }

    public void sort(int[] arr, int low, int high) {
        if (low >= high) {
            return;
        }

        //长度为8,low为0,high为7,mid为3,即第四个元素，偏左
        //长度为7,low为0,high为6,mid为3,即第四个元素，正中
        int mid = (high + low) / 2;

        //sort part
        sort(arr, low, mid);
        sort(arr, mid + 1, high);

        //merge part
        int[] tmp = new int[high - low + 1];
        int index = 0;//临时数组的索引
        int i = low;//左半部分数组的起点
        int j = mid + 1;//右半部分数组的起点

        while (i <= mid && j <= high) {
            if (arr[i] <= arr[j]) {
                tmp[index++] = arr[i++];

            } else {
                tmp[index++] = arr[j++];
                //较小的都更大，那后面的肯定也大于了，这里是以右半边数组的角度考虑和左边逆序对的数量，另外一个解法是从左边数组考虑
                count += mid + 1 - i;
            }
        }

        while (i <= mid) {
            tmp[index++] = arr[i++];
        }
        while (j <= high) {
            tmp[index++] = arr[j++];

        }
        for (index = 0, i = low; i <= high; i++, index++) {
            arr[i] = tmp[index];
        }
    }
}
