const NUM_OF_CELLS = 50;

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

// computational grid
let c_grid = readGrid();
// console.log(c_grid);

let genBtn = document.getElementById("generation");
genBtn.addEventListener(
	"click",
	function () {
		// let updated_grid = c_grid;
		// hacky deep copy
		let updated_grid = JSON.parse(JSON.stringify(c_grid));

		console.log("start generation...");
		// [ x-1 ][ y-1 ] [  x  ][ y-1 ] [ x+1 ][ y-1 ]
		// [ x-1 ][  y  ] [  x  ][  y  ] [ x+1 ][  y  ]
		// [ x-1 ][ y+1 ] [  x  ][ y+1 ] [ x+1 ][ y+1 ]

		for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
			for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
				// compute number of neighbors
				let neighbors = 0;

				// check if neighbors are alive
				neighbors += c_grid[x - 1][y - 1];
				neighbors += c_grid[x - 1][y + 1];
				neighbors += c_grid[x + 1][y - 1];
				neighbors += c_grid[x + 1][y + 1];
				neighbors += c_grid[x - 1][y];
				neighbors += c_grid[x + 1][y];
				neighbors += c_grid[x][y - 1];
				neighbors += c_grid[x][y + 1];

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
		console.log("end generation...");

		c_grid = JSON.parse(JSON.stringify(updated_grid));
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

let debugBtn = document.getElementById("debug");
debugBtn.addEventListener(
	"click",
	function () {
		let x = 1;
		let y = 1;
		let neighbors = 0;
		// iterating through offsets to each border cell
		for (let xOffset = -1; xOffset < 2; xOffset++) {
			for (let yOffset = -1; yOffset < 2; yOffset++) {
				console.log(`${yOffset} ${xOffset}`);
				// check if neighbor is alive if offset is not (0, 0)
				if (!(xOffset === 0 && yOffset === 0)) {
					console.log("checked");
					try {
						let neighbor = document.getElementById(
							`_cell${x + xOffset}_${y + yOffset}`
						);
						if (neighbor.classList.contains("full")) {
							neighbors++;
						}
					} catch (error) {
						console.error(
							`cell: (${x}, ${y}) neighbor: (${x + xOffset}, ${y + yOffset})`
						);
					}
				}
			}
		}

		console.log(neighbors);
	},
	false
);

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
