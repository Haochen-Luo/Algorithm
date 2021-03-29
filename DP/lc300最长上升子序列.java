   public  int lengthOfLIS(int[] nums) {
        int max = 1;

        int f[] = new int[nums.length];
        f[0] = 1;
        for (int i = 1; i < nums.length; i++) {
            int tempMax = 1;
            for (int k = 0; k < i; k++) {
                if (nums[i] > nums[k]) {
                    tempMax = Math.max(tempMax, f[k] + 1);
                }
            }

            f[i] = tempMax;
            max = Math.max(max, tempMax);
        }
        return max;
    }
