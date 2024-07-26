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

let currentArray = [];

function startSorting(algorithm) {
    currentArray = generateArray(); // Store the array to sort
    switch (algorithm) {
        case 'bubble':
            bubbleSort(currentArray);
            break;
        case 'selection':
            selectionSort(currentArray);
            break;
        case 'insertion':
            insertionSort(currentArray);
            break;
        case 'quick':
            quickSort(currentArray);
            break;
    }
}

function bubbleSort(arr) {
    const len = arr.length;
    let delay = 0;

    function sortStep(i, j) {
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
                delay += 0.1;
            } else {
                setTimeout(() => sortStep(i + 1, 0), delay);
            }
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
    }

    sortStep(0, 0);
}

function selectionSort(arr) {
    const len = arr.length;
    let delay = 0;

    function sortStep(i, j, minIndex) {
        if (i < len) {
            if (j < len) {
                displayArray(arr, [j, minIndex], 'testing');
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
                setTimeout(() => sortStep(i, j + 1, minIndex), delay);
                delay += 0.1;
            } else {
                if (minIndex !== i) {
                    let tmp = arr[i];
                    arr[i] = arr[minIndex];
                    arr[minIndex] = tmp;
                    displayArray(arr, [i, minIndex], 'swapped');
                }
                setTimeout(() => sortStep(i + 1, i + 2, i + 1), delay);
            }
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
    }

    sortStep(0, 1, 0);
}

function insertionSort(arr) {
    const len = arr.length;
    let delay = 0;

    function sortStep(i, j) {
        if (i < len) {
            if (j > 0 && arr[j - 1] > arr[j]) {
                displayArray(arr, [j, j - 1], 'testing');
                let tmp = arr[j];
                arr[j] = arr[j - 1];
                arr[j - 1] = tmp;
                displayArray(arr, [j, j - 1], 'swapped');
                setTimeout(() => sortStep(i, j - 1), delay);
                delay += 1;
            } else {
                setTimeout(() => sortStep(i + 1, i + 1), delay);
            }
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
    }

    sortStep(1, 1);
}

function quickSort(arr) {
    let delay = 0;

    function partition(low, high) {
        let pivot = arr[high];
        let i = low - 1;

        for (let j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                [arr[i], arr[j]] = [arr[j], arr[i]];
                displayArray(arr, [i, j], 'swapped');
            }
        }
        [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
        displayArray(arr, [i + 1, high], 'swapped');
        return i + 1;
    }

    function sort(low, high) {
        if (low < high) {
            let pi = partition(low, high);
            setTimeout(() => sort(low, pi - 1), delay);
            delay += 0.1;
            setTimeout(() => sort(pi + 1, high), delay);
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
    }

    sort(0, arr.length - 1);
}

window.onload = generateArray;
