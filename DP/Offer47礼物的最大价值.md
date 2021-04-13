```java
public int maxValue(int[][] grid) {
int[][] f = new int[grid.length + 1][grid[0].length + 1];
        for (int i = 1;i<=grid.length;i++){
            for (int j = 1;j<=grid[0].length ;j++ ) {
                f[i][j] = Math.max(f[i-1][j],f[i][j-1])+grid[i-1][j-1];
            }
        }
        return f[grid.length][grid[0].length];
    }
```
