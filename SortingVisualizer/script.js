const arrayContainer = document.getElementById('array-container');

function generateArray(numElements = 50) {
    const arr = [];
    for (let i = 0; i < numElements; i++) {
        arr.push(Math.floor(Math.random() * 100) + 1);
    }
    displayArray(arr);
    return arr;
}

function displayArray(arr, highlightedIndexes = [], className = '') {
    arrayContainer.innerHTML = '';
    arr.forEach((value, idx) => {
        const bar = document.createElement('div');
        bar.style.height = `${value * 3}px`; // Scale factor to visualize
        bar.classList.add('array-bar');
        if (highlightedIndexes.includes(idx)) {
            bar.classList.add(className);
        }
        arrayContainer.appendChild(bar);
    });
}

function startSorting() {
    const sortedArray = generateArray(); // Store the array to sort
    bubbleSort(sortedArray);
}

function bubbleSort(arr) {
    const len = arr.length;
    let delay = 0; // Initialize delay for visualization

    function sortStep(i,j) {
        if (i < len) {
            if (j < len - i - 1) {
                displayArray(arr, [j, j + 1], 'testing');
                if (arr[j] > arr[j + 1]) {
                    let tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                    displayArray(arr, [j, j + 1], 'swapped');
                }
                setTimeout(() => sortStep(i, j + 1), delay);
                delay += .01;
            } else {
                setTimeout(() => sortStep(i + 1, 0), delay);
            }
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
            }

            sortStep(0, 0);

        }
window.onload = generateArray;
