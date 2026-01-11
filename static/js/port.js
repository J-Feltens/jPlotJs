function draw_vector_field(canvas, width, height, scale, vectors) {
    /*
        vectors is an array in format
        [ rows
            [ columns
                {
                    color: float,
                    angle: float, interpreted as radians
                    magnitude: float, absolute magnitude
                    magnitude_norm: float, normalized magnitude
                },
                ...
            ]
        ]
     */
    const ctx = canvas.getContext("2d");

    const vec_count_y = vectors.length;
    const vec_count_x = vectors[0].length;
    const x_delta = width / (vec_count_x - 1);
    const y_delta = height / (vec_count_y - 1);
    for (let y = 0; y < vec_count_y; y++) {
        for (let x = 0; x < vec_count_x; x++) {
            const angle = vectors[y][x].angle;
            const color = vectors[y][x].color;
            const mag_norm = vectors[y][x].magnitude_norm;
            const vector_scale = Math.max(mag_norm * scale, 0.3);

            drawArrow(ctx, x * x_delta, y * y_delta, angle, {
                length: VECTOR_LENGTH * vector_scale,
                color: color,
                lineWidth: VECTOR_LINE_WIDTH * vector_scale,
                headLength: VECTOR_HEAD_LENGTH * vector_scale,
                headWidth: VECTOR_HEAD_WIDTH * vector_scale,
                style: VECTOR_FILL_STYLE,
            });
        }
    }
}

function draw_port(canvas, width, height, vectors = null) {
    const ctx = canvas.getContext("2d");

    // Clear
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const scale = 2;


    if (vectors == null) {
        let vector_field = [];
        let vec_count_x = 40;
        let vec_count_y = 20;

        for (let y = 0; y < vec_count_y; y++) {
            let row = []
            for (let x = 0; x < vec_count_x; x++) {
                row.push({color: "blue", angle: Math.random() * 2 * Math.PI});
            }
            vector_field.push(row);
        }
        vectors = vector_field;
    }

    draw_vector_field(canvas, width, height, scale, vectors);
}
