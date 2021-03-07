const NUM_OF_CELLS = 50;

// constructs array based on dimensions that are passed in
// number of params determines number of dimensions
function createArray(length) {
	let arr = new Array(length || 0);
	let i = length;

	if (arguments.length > 1) {
		let args = Array.prototype.slice.call(arguments, 1);
		while (i--) arr[length - 1 - i] = createArray.apply(this, args);
	}

	return arr;
}

// retrieve "visual grid" contents and transfer to c_grid
function readGrid() {
	let grid = createArray(NUM_OF_CELLS + 2, NUM_OF_CELLS + 2);

	for (let y = 0; y < NUM_OF_CELLS + 2; y++) {
		for (let x = 0; x < NUM_OF_CELLS + 2; x++) {
			// record cell status in computational grid
			let cell = document.getElementById(`_cell${x}_${y}`);
			if (cell.classList.contains("full")) {
				grid[x][y] = 1;
			} else {
				// this may not be necessary if grid is already full of zeroes
				grid[x][y] = 0;
			}
		}
	}

	return grid;
}

// performs one iteration of game of life
function generation(grid) {
	// let updated_grid = c_grid;
	// hacky deep copy
	let updated_grid = JSON.parse(JSON.stringify(grid));

	// iterate through interactable cells on grid
	for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
		for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
			// compute number of neighbors
			let neighbors = 0;

			// check if neighbors are alive
			neighbors += grid[x - 1][y - 1];
			neighbors += grid[x - 1][y + 1];
			neighbors += grid[x + 1][y - 1];
			neighbors += grid[x + 1][y + 1];
			neighbors += grid[x - 1][y];
			neighbors += grid[x + 1][y];
			neighbors += grid[x][y - 1];
			neighbors += grid[x][y + 1];

			// console.log(neighbors);

			// LIVING CELL
			if (c_grid[x][y] === 1) {
				if (neighbors < 2) {
					// Death by exposure ( <2 neighbors )
					updated_grid[x][y] = 0;
				} else if (neighbors > 3) {
					// Death by overcrowding ( >3 neighbors )
					updated_grid[x][y] = 0;
				}
			}
			// EMPTY CELL
			else {
				if (neighbors === 3) {
					// New Life
					updated_grid[x][y] = 1;
				}
			}
		}
	}

	return updated_grid;
}

// computational grid
let c_grid = readGrid();
// console.log(c_grid);

let genBtn = document.getElementById("generation");
genBtn.addEventListener(
	"click",
	function () {
		c_grid = generation(c_grid);
		printGrid(c_grid);
	},
	false
);

let flipBtn = document.getElementById("flippe");
flipBtn.addEventListener(
	"click",
	function () {
		for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
			for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
				let cell = document.getElementById(`_cell${x}_${y}`);
				cell.classList.toggle("full");
				cell.classList.toggle("empty");
			}
		}
	},
	false
);

let startBtn = document.getElementById("start");
startBtn.addEventListener(
	"click",
	function () {
		console.log("start button does nothing...");
		// stateful main loop for game
		// state functions allow for event driven pausing via start and stop functions
		// must have controllable timing, asychronous
	},
	false
);

// let debugBtn = document.getElementById("debug");
// debugBtn.addEventListener(
// 	"click",
// 	function () {
// 		() => {}
// 	},
// 	false
// );

function printGrid(c_grid) {
	for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
		for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
			let cell = document.getElementById(`_cell${x}_${y}`);
			if (c_grid[x][y] === 0) {
				cell.classList.remove("full");
				cell.classList.add("empty");
			} else {
				cell.classList.remove("empty");
				cell.classList.add("full");
			}
		}
	}
}
