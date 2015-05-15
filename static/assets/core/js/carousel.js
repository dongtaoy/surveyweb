var total = 13;
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
var alerted = false;

moveNext = function () {

    if (clicked) {
        return;
    }
    clicked = true;

    if (current == total) {
        clicked = false;

        if (alerted) {
            return;
        } else {
            alerted = true;
            alert("No more image");
            return;
        }
    }

    alerted = false;

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
        if (left_x < -240) {
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
        if (right_x > 240) {
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
};

moveBack = function () {
    if (clicked) {
        return;
    }
    clicked = true;

    if (current == 1) {
        clicked = false;
        if (alerted) {
            return;
        } else {
            alerted = true;
            alert("No more image");
            return;
        }
    }

    alerted = false;

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
        if (left_x < -240) {
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
};

function nextClick_loop(total_click) {
    setTimeout(function () {
        if (total_click <= 0) {
            nextClick = 0;
            return;
        } else {
            total_click--;
            moveNext();
        }
        nextClick_loop(total_click);
    }, DURATION);
}

function backClick_loop(total_click) {
    setTimeout(function () {
        if (total_click <= 0) {
            backClick = 0;
            return;
        } else {
            total_click--;
            moveBack();
        }
        backClick_loop(total_click);
    }, DURATION);
}

$("#nextCarousel").click(function () {
    nextClick++;
    backClick = 0;
    moveNext();
    nextClick_loop(nextClick - 1);
});


$("#backCarousel").click(function () {
    backClick++;
    nextClick = 0;
    moveBack();
    backClick_loop(backClick - 1);
});

for (var i = 1; i <= total; i++) {
    $("#carousel > img:nth-child(" + i + ")").click(function () {
        var position = $(this).index() + 1;
        var diff = position - current;
        if (diff == 0) {
            var url = $(this).attr("src");
            window.open(url, '_blank');
        }
        if (diff > 0) {
            moveNext();
            nextClick_loop(diff - 1);
        } else if (diff < 0) {
            moveBack();
            backClick_loop(Math.abs(diff) - 1);
        }
    })
}
;

$("body").keydown(function (e) {
    if (e.keyCode == 39) { // left
        nextClick++;
        backClick = 0;
        moveNext();
        nextClick_loop(nextClick - 1);
    }
    if (e.keyCode == 37) {
        backClick++;
        nextClick = 0;
        moveBack();
        backClick_loop(backClick - 1);
    }
})