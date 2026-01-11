/**
 * Draw an arrow on an HTML canvas.
 *
 * @param {CanvasRenderingContext2D} ctx
 * @param {number} x        Arrow center x (pixels)
 * @param {number} y        Arrow center y (pixels)
 * @param {number} length   Shaft length (pixels)
 * @param {number} rotation Rotation in radians (0 = pointing right)
 * @param {object} opt
 * @param {string} opt.color        Stroke/fill color (e.g. "#ff0000" or "rgba(...)")
 * @param {string} opt.style        "line" | "filled" | "hollow"
 * @param {number} opt.lineWidth    Shaft/outline width
 * @param {number} opt.headLength   Head length (pixels)
 * @param {number} opt.headWidth    Head width (pixels) (tip-to-tip)
 * @param {boolean} opt.dashed      Dashed shaft
 * @param {number[]} opt.dash       Dash pattern, e.g. [6, 4]
 */
function drawArrow(ctx, x, y, rotation, opt = {}) {
    const {
        color = "#111",
        length = VECTOR_LENGTH,
        style = "line",     // "line" | "filled" | "hollow"
        lineWidth = 2,
        // length = 20,
        headLength = Math.max(10, length * 0.25),
        headWidth = Math.max(10, length * 0.18),
        dashed = false,
        dash = [6, 4],
    } = opt;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    // Optional dashed shaft
    ctx.setLineDash(dashed ? dash : []);

    // We draw pointing to +X direction in local space
    const shaftLen = Math.max(0, length - headLength);
    const halfHeadW = headWidth / 2;

    // Shaft: from -length/2 to tip area
    const startX = -length / 2;
    const shaftEndX = startX + shaftLen;

    // Draw shaft (skip for filled/hollow if you only want head, but usually keep it)
    ctx.beginPath();
    ctx.moveTo(startX, 0);
    ctx.lineTo(shaftEndX, 0);
    ctx.stroke();

    // Arrow head triangle points
    const tipX = startX + length;
    const baseX = tipX - headLength;

    // Reset dash for head so it’s clean
    ctx.setLineDash([]);

    ctx.beginPath();
    ctx.moveTo(tipX, 0);
    ctx.lineTo(baseX, -halfHeadW);
    ctx.lineTo(baseX, +halfHeadW);
    ctx.closePath();

    if (style === "filled") {
        ctx.fill();
    } else if (style === "hollow") {
        ctx.stroke();
    } else {
        // "line": classic open V head
        ctx.beginPath();
        ctx.moveTo(tipX, 0);
        ctx.lineTo(baseX, -halfHeadW);
        ctx.moveTo(tipX, 0);
        ctx.lineTo(baseX, +halfHeadW);
        ctx.stroke();
    }

    ctx.restore();
}
