const NUM_OF_CELLS = 50;

// function createArray(length) {
// 	let arr = new Array(length || 0);
// 	let i = length;

// 	if (arguments.length > 1) {
// 		let args = Array.prototype.slice.call(arguments, 1);
// 		while (i--) arr[length - 1 - i] = createArray.apply(this, args);
// 	}

// 	return arr;
// }

// let c_grid = createArray(NUM_OF_CELLS + 2, NUM_OF_CELLS + 2);

let genBtn = document.getElementById("generation");
genBtn.addEventListener(
	"click",
	function () {
		console.log("start generation...");
		// [ x-1 ][ y-1 ] [  x  ][ y-1 ] [ x+1 ][ y-1 ]
		// [ x-1 ][  y  ] [  x  ][  y  ] [ x+1 ][  y  ]
		// [ x-1 ][ y+1 ] [  x  ][ y+1 ] [ x+1 ][ y+1 ]

		for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
			for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
				let cell = document.getElementById(`_cell${x}_${y}`);
				let neighborCount = 0;
				for (let xOffset = -1; xOffset < 2; xOffset++) {
					for (let yOffset = -1; yOffset < 2; yOffset++) {
						if (!(xOffset === 0 && yOffset === 0)) {
							let neighbor = document.getElementById(
								`_cell${x + xOffset}_${y + yOffset}`
							);
							if (neighbor.classList.contains("full")) {
								neighborCount++;
							}

							// console.error(
							// 	`cell: (${x}, ${y}) neighbor: (${x + xOffset}, ${y + yOffset})`
							// );
						}
					}
				}
				// console.log(neighborCount);

				// LIVING CELL
				if (cell.classList.contains("full")) {
					if (neighborCount < 2) {
						// Death by exposure ( <2 neighbors )
						cell.classList.remove("full");
						cell.classList.add("empty");
					} else if (neighborCount > 3) {
						// Death by overcrowding ( >3 neighbors )
						cell.classList.remove("full");
						cell.classList.add("empty");
					}
				}
				// EMPTY CELL
				else {
					if (neighborCount === 3) {
						// New Life
						cell.classList.remove("empty");
						cell.classList.add("full");
					}
				}
			}
		}
		console.log("end generation...");
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
		let neighborCount = 0;
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
							neighborCount++;
						}
					} catch (error) {
						console.error(
							`cell: (${x}, ${y}) neighbor: (${x + xOffset}, ${y + yOffset})`
						);
					}
				}
			}
		}

		console.log(neighborCount);
	},
	false
);

function printGrid(c_grid) {
	for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
		for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
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
