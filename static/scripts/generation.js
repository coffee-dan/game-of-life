// def generation( c_grid ) :
//   updated_grid = deepcopy( c_grid )
//   for y in range( 1, NUM_OF_CELLS+1 ) :
//     for x in range( 1, NUM_OF_CELLS+1 ) :
//       neighbors = 0
//       neighbors += c_grid[ x-1 ][ y-1 ]
//       neighbors += c_grid[  x  ][ y-1 ]
//       neighbors += c_grid[ x+1 ][ y-1 ]
//       neighbors += c_grid[ x-1 ][  y  ]
//       neighbors += c_grid[ x+1 ][  y  ]
//       neighbors += c_grid[ x-1 ][ y+1 ]
//       neighbors += c_grid[  x  ][ y+1 ]
//       neighbors += c_grid[ x+1 ][ y+1 ]
//       # Live cell
//       if c_grid[ x ][ y ] == 1 :
//         if neighbors < 2 :
//           # Death by exposure ( <2 neighbors )
//           updated_grid[ x ][ y ] = 0
//         elif neighbors > 3 :
//           # Death by overcrowding ( >3 neighbors )
//           updated_grid[ x ][ y ] = 0
//       # Dead cell
//       else :
//         if neighbors == 3 :
//           # New life
//           updated_grid[ x ][ y ] = 1
//   return updated_grid

// gotta get the grid from html
// need a way to not hard code this

console.log("dab");

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

let c_grid = createArray(NUM_OF_CELLS + 2, NUM_OF_CELLS + 2);

let flipBtn = document.getElementById("flippe");
flipBtn.addEventListener(
	"click",
	function () {
		for (let y = 1; y < NUM_OF_CELLS + 1; y++) {
			for (let x = 1; x < NUM_OF_CELLS + 1; x++) {
				let cell = document.getElementById(`_cell${x}${y}`);
				// console.log(`_cell${x}${y}`);
				cell.classList.toggle("full");
				cell.classList.toggle("empty");
			}
		}
	},
	false
);
