void doIt() {
    List<Integer> nums = [1, 2, 3, -2, -5, 6]
    Collections.sort(nums, { a, b -> a.abs() <=> b.abs() })
}
