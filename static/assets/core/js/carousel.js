var total = 9;
var current = 1;
var DURATION = 1000;
var nextClick = 0;
var backClick = 0;

function getRotationDegrees(obj) {
    var matrix = obj.css("transform");
    if (matrix !== 'none') {
        var values = matrix.split('(')[1].split(')')[0].split(',');
        var a = values[0];
        var b = -values[2];
        var angle = Math.round(Math.atan2(b, a) * (180 / Math.PI));
    } else {
        var angle = 0;
    }
    return angle;
};
function getTranslateX(obj) {
    var matrix = obj.css("transform");
    if (matrix !== 'none') {
        var values = matrix.split('(')[1].split(')')[0].split(',');

        var x = parseFloat(values[12]);
    } else {
        var x = 0;
    }
    return x;
};

var clicked = false;

moveNext = function () {

    if (clicked) {
        return;
    }
    clicked = true;
    if (current == total) {
        alert("No more image");
        clicked = false;
        return;
    }
    var obj = $("#carousel > img:nth-child(" + current + ")");
    var x = getTranslateX(obj);
    var angle = getRotationDegrees(obj);

    angle += 45;
    x = -200;
    obj.transition({
        rotateY: angle + 'deg',
        duration: DURATION
    });
    obj.css("transform", "translateZ( 288px ) translateX(" + x + "px) rotateY(   " + angle + "deg )");
    var left = current - 1;
    while (left > 0) {

        var left_obj = $("#carousel > img:nth-child(" + left + ")");
        var left_x = getTranslateX(left_obj);
        var left_angle = getRotationDegrees(left_obj);
        left_x -= 20;
        if (left_x < -260) {
            left_obj.css("visibility", "hidden");
        } else {
            left_obj.css("visibility", "visible");
        }
        left_obj.transition({
            rotateY: left_angle + 'deg',
            duration: DURATION
        });
        left_obj.css("transform", "translateZ( 288px ) translateX(" + left_x + "px) rotateY(   " + left_angle + "deg )");
        left -= 1;
    }

    var right = current + 1;
    var new_obj = $("#carousel > img:nth-child(" + right + ")");
    var new_x = getTranslateX(new_obj);
    var new_angle = getRotationDegrees(new_obj);

    new_angle = 0;
    x = 0;
    new_obj.transition({
        rotateY: new_angle + 'deg',
        duration: DURATION
    });
    new_obj.css("transform", "translateZ( 500px ) translateX(" + x + "px) rotateY(   " + new_angle + "deg )");
    right += 1;

    while (right <= total) {
        var right_obj = $("#carousel > img:nth-child(" + right + ")");
        var right_x = getTranslateX(right_obj);
        var right_angle = getRotationDegrees(right_obj);
        right_x -= 20;
        if (right_x > 260) {
            right_obj.css("visibility", "hidden");
        } else {
            right_obj.css("visibility", "visible");
        }
        right_obj.transition({
            rotateY: right_angle + 'deg',
            duration: DURATION
        });
        right_obj.css("transform", "translateZ( 288px ) translateX(" + right_x + "px) rotateY(   " + right_angle + "deg )");
        right += 1;
    }
    current += 1;
    setTimeout(function () {
        clicked = false;
    }, DURATION);
}
moveBack = function () {
    if (clicked) {
        return;
    }
    clicked = true;
    if (current == 1) {
        alert("No more image");
        clicked = false;
        return;
    }

    var obj = $("#carousel > img:nth-child(" + current + ")");
    var x = getTranslateX(obj);
    var angle = getRotationDegrees(obj);

    angle -= 45;
    x = 200;
    obj.transition({
        rotateY: angle + 'deg',
        duration: DURATION
    });
    obj.css("transform", "translateZ( 288px ) translateX(" + x + "px) rotateY(   " + angle + "deg )");

    var left = current - 1;
    var new_obj = $("#carousel > img:nth-child(" + left + ")");
    var new_x = getTranslateX(new_obj);
    var new_angle = getRotationDegrees(new_obj);
    new_angle = 0;
    x = 0;
    new_obj.transition({
        rotateY: new_angle + 'deg',
        duration: DURATION
    });
    new_obj.css("transform", "translateZ( 500px ) translateX(" + x + "px) rotateY(   " + new_angle + "deg )");
    left -= 1;

    while (left > 0) {
        var left_obj = $("#carousel > img:nth-child(" + left + ")");
        var left_x = getTranslateX(left_obj);
        var left_angle = getRotationDegrees(left_obj);
        left_x += 20;
        if (left_x < -260) {
            left_obj.css("visibility", "hidden");
        } else {
            left_obj.css("visibility", "visible");
        }
        left_obj.transition({
            rotateY: left_angle + 'deg',
            duration: DURATION
        });
        left_obj.css("transform", "translateZ( 288px ) translateX(" + left_x + "px) rotateY(   " + left_angle + "deg )");
        left -= 1;
    }

    var right = current + 1;
    while (right <= total) {
        var right_obj = $("#carousel > img:nth-child(" + right + ")");
        var right_x = getTranslateX(right_obj);
        var right_angle = getRotationDegrees(right_obj);
        right_x += 20;
        if (right_x > 260) {
            right_obj.css("visibility", "hidden");
        } else {
            right_obj.css("visibility", "visible");
        }
        right_obj.transition({
            rotateY: right_angle + 'deg',
            duration: DURATION
        });
        right_obj.css("transform", "translateZ( 288px ) translateX(" + right_x + "px) rotateY(   " + right_angle + "deg )");
        right += 1;
    }
    current -= 1;
    setTimeout(function () {
        clicked = false;
    }, DURATION);
}

$("#nextCarousel").click(function () {
    nextClick++;
    backClick = 0;
    moveNext();
    nextClick_loop(nextClick - 1);
});

function nextClick_loop(total_click) {
    setTimeout(function () {
        if (total_click <= 0) {
            nextClick = 0;
            firstTime = true;
            return;
        } else {
            total_click--;
            moveNext();
        }
        nextClick_loop(total_click);
    }, DURATION);
}


$("#backCarousel").click(function () {
    backClick++;
    nextClick = 0;
    moveBack();
    backClick_loop(backClick - 1);
});

function backClick_loop(total_click) {
    setTimeout(function () {
        if (total_click <= 0) {
            backClick = 0;
            firstTime = true;
            return;
        } else {
            total_click--;
            moveBack();
        }
        backClick_loop(total_click);
    }, DURATION);
}


for (var i = 1; i <= total; i++) {
    $("#carousel > img:nth-child(" + i + ")").click(function () {
        var position = $(this).index() + 1;
        var diff = position - current;
        if (diff > 0) {
            var j = diff;
            moveNext();
            j--;
            function forward_loop() {
                setTimeout(function () {
                    moveNext();
                    j--;
                    if (j > 0) {
                        forward_loop();
                    }
                }, DURATION);
            }

            forward_loop();
        } else if (diff < 0) {
            var k = diff;
            moveBack();
            k++;
            function backward_loop() {
                setTimeout(function () {
                    moveBack();
                    k++;
                    if (k < 0) {
                        backward_loop();
                    }
                }, DURATION);
            }

            backward_loop();
        }
    })
}