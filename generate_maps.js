const fs = require('fs');

const R = 19;
const C = 25;

const F=0, W=1, FIRE=2, SMK=3, EXIT=4, BCC=5, TWL=6, MSK=7, KEY=8, DLCK=9, TOX=10;
const PS=11, FUR=12, ELEC=13, BRKR=14, GASL=15, GASV=16, PHONE=17, HDOOR=18, SDOOR=19;
const NPC=20, BLCK=21, EXITL=22;

function generate_maze() {
    let maze = Array.from({length: R}, () => Array(C).fill(W));
    for(let i=1; i<R-1; i+=2) {
        for(let j=1; j<C-1; j+=2) {
            maze[i][j] = F;
        }
    }
    
    let stack = [[1, 1]];
    let visited = new Set(['1,1']);
    
    while(stack.length > 0) {
        let [cr, cc] = stack[stack.length - 1];
        let neighbors = [];
        const dirs = [[-2, 0], [2, 0], [0, -2], [0, 2]];
        for(let [dr, dc] of dirs) {
            let nr = cr + dr, nc = cc + dc;
            if(nr > 0 && nr < R-1 && nc > 0 && nc < C-1 && !visited.has(`${nr},${nc}`)) {
                neighbors.push([nr, nc]);
            }
        }
        
        if(neighbors.length > 0) {
            let index = Math.floor(Math.random() * neighbors.length);
            let [nr, nc] = neighbors[index];
            maze[cr + (nr - cr)/2][cc + (nc - cc)/2] = F;
            visited.add(`${nr},${nc}`);
            stack.push([nr, nc]);
        } else {
            stack.pop();
        }
    }
    
    // Random loops
    for(let i=0; i<15; i++) {
        let r = Math.floor(Math.random() * (R-2)) + 1;
        let c = Math.floor(Math.random() * (C-2)) + 1;
        if(maze[r][c] === W) maze[r][c] = F;
    }
    return maze;
}

let levels = [];
for(let i=0; i<15; i++) {
    let maze = generate_maze();
    
    maze[1][1] = PS;
    maze[R-2][C-2] = EXIT;
    
    let empty_spots = [];
    for(let r=1; r<R-1; r++) {
        for(let c=1; c<C-1; c++) {
            if(maze[r][c] === F && !(r===1 && c===1) && !(r===R-2 && c===C-2)) {
                empty_spots.push([r, c]);
            }
        }
    }
    empty_spots.sort(() => Math.random() - 0.5);
    
    let num_fires = i + 1;
    let num_bccs = Math.max(1, Math.min(4, Math.floor(i/3) + 1));
    
    for(let j=0; j<num_fires; j++) {
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = FIRE; }
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = SMK; }
    }
    
    for(let j=0; j<num_bccs; j++) {
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = BCC; }
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = TWL; }
    }
    
    if(i >= 3) {
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = KEY; }
        maze[R-2][C-3] = DLCK;
    }
    if(i >= 5) {
        maze[R-3][C-2] = ELEC;
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = BRKR; }
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = MSK; }
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = TOX; }
    }
    if(i >= 7) {
        maze[R-4][C-2] = GASL;
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = GASV; }
    }
    if(i >= 10) {
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = PHONE; }
        maze[R-2][C-2] = EXITL;
    }
    if(i >= 12) {
        if(empty_spots.length) { let [r,c]=empty_spots.pop(); maze[r][c] = NPC; }
    }
    
    levels.push({
        nameVi: `Thử thách màn ${i+1}`,
        time: 120 + i*15,
        fireSpread: 180,
        map: maze,
        tip: `Cẩn thận với khói lửa và tìm các vật phẩm hỗ trợ. Khám phá đường đi! (Màn ${i+1})`
    });
}

fs.writeFileSync('frontend/js/game-levels.js', 'window.GAME_LEVELS = ' + JSON.stringify(levels, null, 2) + ';\n');
console.log('Successfully generated frontend/js/game-levels.js');
