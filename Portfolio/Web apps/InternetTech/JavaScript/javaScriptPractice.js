function sumArrays(numbers) {
    let total = 0;
    numbers.forEach(addToTotal);

    function addToTotal(value) {
        total += value;
    }
    document.write("Sum of array: "+total);
}