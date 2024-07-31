const arrayContainer = document.getElementById('array-container');
const treeContainer = document.getElementById('tree-container');
const arraySizeValue = document.getElementById('array-size-value');
let currentArray = [];
let arraySize = 50;

function toggleFeature(feature) {
    const barChartSection = document.getElementById('bar-chart-section');
    const treeSection = document.getElementById('tree-section');
    if (feature === 'bar') {
        barChartSection.style.display = 'block';
        treeSection.style.display = 'none';
    } else if (feature === 'tree') {
        barChartSection.style.display = 'none';
        treeSection.style.display = 'block';
    }
}

function updateArraySize(size) {
    arraySize = size;
    arraySizeValue.textContent = size;
    generateArray();
}

function generateArray(numElements = arraySize) {
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
            delay += 25;
            setTimeout(() => sort(pi + 1, high), delay);
        } else {
            setTimeout(() => displayArray(arr), delay);
        }
    }

    sort(0, arr.length - 1);
}

// Tree-related functionality

// TreeNode class representing each node in the tree
class TreeNode {
    constructor(value) {
        this.value = value;
        this.left = null; // Left child
        this.right = null; // Right child
        this.element = null; // DOM element for visualization
    }
}

// BinaryTree class for managing the tree structure
class BinaryTree {
    constructor() {
        this.root = null; // Root of the tree
    }

    // Function to insert a new value into the tree
    insert(value) {
        const newNode = new TreeNode(value);
        if (!this.root) {
            this.root = newNode; // If tree is empty, set root
        } else {
            this.insertNode(this.root, newNode); // Insert node recursively
        }
    }

    // Helper function to insert a node in the correct position
    insertNode(node, newNode) {
        if (newNode.value < node.value) {
            if (!node.left) {
                node.left = newNode; // Insert on the left
            } else {
                this.insertNode(node.left, newNode); // Recursive call
            }
        } else {
            if (!node.right) {
                node.right = newNode; // Insert on the right
            } else {
                this.insertNode(node.right, newNode); // Recursive call
            }
        }
    }

    // In-order traversal: Left -> Node -> Right
    inOrderTraversal(node, visit) {
        if (node) {
            this.inOrderTraversal(node.left, visit); // Visit left subtree
            visit(node); // Visit current node
            this.inOrderTraversal(node.right, visit); // Visit right subtree
        }
    }

    // Pre-order traversal: Node -> Left -> Right
    preOrderTraversal(node, visit) {
        if (node) {
            visit(node); // Visit current node
            this.preOrderTraversal(node.left, visit); // Visit left subtree
            this.preOrderTraversal(node.right, visit); // Visit right subtree
        }
    }

    // Post-order traversal: Left -> Right -> Node
    postOrderTraversal(node, visit) {
        if (node) {
            this.postOrderTraversal(node.left, visit); // Visit left subtree
            this.postOrderTraversal(node.right, visit); // Visit right subtree
            visit(node); // Visit current node
        }
    }
}

// Initialize a new BinaryTree instance
let tree = new BinaryTree();

// Function to generate a new tree with random values
function generateTree() {
    tree = new BinaryTree(); // Reset the tree
    const values = Array.from({ length: 10 }, () => Math.floor(Math.random() * 100) + 1);
    values.forEach(value => tree.insert(value)); // Insert random values
    displayTree(tree.root); // Display the generated tree
}

// Function to display the tree in the container
function displayTree(node, depth = 0, pos = 0) {
    if (!node) return;

    const nodeElement = document.createElement('div'); // Create a node element
    nodeElement.className = 'node';
    nodeElement.textContent = node.value;
    nodeElement.style.left = `${50 + pos * 50}px`; // Position horizontally
    nodeElement.style.top = `${depth * 80}px`; // Position vertically with a larger gap for clarity
    nodeElement.style.position = 'absolute'; // Ensure absolute positioning

    node.element = nodeElement; // Save reference for traversal

    treeContainer.appendChild(nodeElement); // Add the node to the container

    // Recursively display left child
    if (node.left) {
        const edgeElement = document.createElement('div');
        edgeElement.className = 'edge';
        edgeElement.style.width = '2px'; // Width of the line
        edgeElement.style.height = '50px'; // Height of the line
        edgeElement.style.backgroundColor = '#f0f0f0'; // Line color
        edgeElement.style.position = 'absolute';
        edgeElement.style.left = `${parseFloat(nodeElement.style.left) - 25}px`;
        edgeElement.style.top = `${parseFloat(nodeElement.style.top) + 20}px`;
        edgeElement.style.transform = 'rotate(-45deg)'; // Line to left child
        treeContainer.appendChild(edgeElement);

        displayTree(node.left, depth + 1, pos - Math.pow(2, 2 - depth)); // Recursive call
    }

    // Recursively display right child
    if (node.right) {
        const edgeElement = document.createElement('div');
        edgeElement.className = 'edge';
        edgeElement.style.width = '2px'; // Width of the line
        edgeElement.style.height = '50px'; // Height of the line
        edgeElement.style.backgroundColor = '#f0f0f0'; // Line color
        edgeElement.style.position = 'absolute';
        edgeElement.style.left = `${parseFloat(nodeElement.style.left) + 25}px`;
        edgeElement.style.top = `${parseFloat(nodeElement.style.top) + 20}px`;
        edgeElement.style.transform = 'rotate(45deg)'; // Line to right child
        treeContainer.appendChild(edgeElement);

        displayTree(node.right, depth + 1, pos + Math.pow(2, 2 - depth)); // Recursive call
    }
}

// Function to start the selected traversal and visualize it
function startTraversal(type) {
    treeContainer.innerHTML = ''; // Clear the tree container
    displayTree(tree.root); // Display the tree

    // Function to highlight visited nodes
    const highlightNode = (node, delay) => {
        setTimeout(() => {
            node.element.style.backgroundColor = 'orange'; // Highlight visited node
        }, delay);
    };

    let delay = 0;
    const visit = (node) => {
        highlightNode(node, delay);
        delay += 500; // Delay between each node highlight
    };

    // Switch to the selected traversal type
    switch (type) {
        case 'inOrder':
            tree.inOrderTraversal(tree.root, visit); // Perform in-order traversal
            break;
        case 'preOrder':
            tree.preOrderTraversal(tree.root, visit); // Perform pre-order traversal
            break;
        case 'postOrder':
            tree.postOrderTraversal(tree.root, visit); // Perform post-order traversal
            break;
    }
}

// Initialize the visualization with a generated array
window.onload = generateArray;
