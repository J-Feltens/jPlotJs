function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function onload() {
    const WINDOW_WIDTH = window.innerWidth * 0.8;
    const WINDOW_HEIGHT = window.innerHeight * 0.8;

    const canvas = document.createElement("canvas");
    canvas.setAttribute("id", "canvas");
    canvas.width = WINDOW_WIDTH;
    canvas.height = WINDOW_HEIGHT;
    canvas.classList.add("vectorfield-canvas");
    document.body.appendChild(canvas);

    const delta_i = 0.000001
    let i = 0
    while (true) {
        calc_port(i).then(port => {
            const vectors = port.vectors;
            console.log(vectors);

            draw_port(canvas, WINDOW_WIDTH, WINDOW_HEIGHT, vectors);
        });

        i += delta_i;
        await sleep(INTERVAL);
    }
}

