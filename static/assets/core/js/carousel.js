$(document).ready(function(){
	var total = 9;
	var current = 1;
	var DURATION = 1000;
	function getRotationDegrees(obj) {
		var matrix = obj.css("transform");
		if(matrix !== 'none') {
		    var values = matrix.split('(')[1].split(')')[0].split(',');
		    var a = values[0];
		    var b = -values[2];
		    var angle = Math.round(Math.atan2(b, a) * (180/Math.PI));
	  } else { var angle = 0; }
	  return angle;
	};
	function getTranslateX(obj){
		var matrix = obj.css("transform");
		if (matrix !== 'none') {
			var values = matrix.split('(')[1].split(')')[0].split(',');

			var x = parseFloat(values[12]);
		}else{
			var x = 0;
		}
		return x;
	};

	var clicked = false;
	$("#nextCarousel").click(function(e){
		if (clicked){
			return ;
		}
		clicked = true;
		if (current == total){
			alert("No more image");
			clicked=false;
			return;
		}
		var obj = $("#carousel > a:nth-child("+current+") img");
		var x = getTranslateX(obj);
		var angle = getRotationDegrees(obj); 

		angle += 45;x = -200;
		obj.transition({
		  rotateY: angle+'deg',
		  duration: DURATION
		});
		obj.css("transform", "translateZ( 288px ) translateX("+x+"px) rotateY(   "+angle+"deg )");

		var left = current - 1;
		while (left > 0){
			
			var left_obj = $("#carousel > a:nth-child("+left+") img");
			var left_x = getTranslateX(left_obj);
			var left_angle = getRotationDegrees(left_obj);
			left_x -= 20;
			if (left_x < -260){
				left_obj.css("visibility","hidden");
			}else{
				left_obj.css("visibility","visible");
			}
			left_obj.transition({
			  rotateY: left_angle+'deg',
			  duration: DURATION
			});
			left_obj.css("transform", "translateZ( 288px ) translateX("+left_x+"px) rotateY(   "+left_angle+"deg )");
			left -= 1;
		}

		var right = current + 1;
		var new_obj = $("#carousel > a:nth-child("+right+") img");
		var new_x = getTranslateX(new_obj);
		var new_angle = getRotationDegrees(new_obj); 

		new_angle = 0;x = 0;
		new_obj.transition({
		  rotateY: new_angle+'deg',
		  duration: DURATION
		});
		new_obj.css("transform", "translateZ( 500px ) translateX("+x+"px) rotateY(   "+new_angle+"deg )");
		right += 1;
		
		while (right <= total){
			var right_obj = $("#carousel > a:nth-child("+right+") img");
			var right_x = getTranslateX(right_obj);
			var right_angle = getRotationDegrees(right_obj);
			right_x -= 20;
			if (right_x > 260){
				right_obj.css("visibility","hidden");
			}else{
				right_obj.css("visibility","visible");
			}
			right_obj.transition({
			  rotateY: right_angle+'deg',
			  duration: DURATION
			});
			right_obj.css("transform", "translateZ( 288px ) translateX("+right_x+"px) rotateY(   "+right_angle+"deg )");
			right += 1;
		}
		current += 1;
		setTimeout(function(){ clicked=false; }, DURATION);
	});

	$("#backCarousel").click(function(){
		if (clicked){
			return ;
		}
		clicked = true;
		if (current == 1){
			alert("No more image");
			clicked=false;
			return;
		}

		var obj = $("#carousel > a:nth-child("+current+") img");
		var x = getTranslateX(obj);
		var angle = getRotationDegrees(obj); 

		angle -= 45;x = 200;
		obj.transition({
		  rotateY: angle+'deg',
		  duration: DURATION
		});
		obj.css("transform", "translateZ( 288px ) translateX("+x+"px) rotateY(   "+angle+"deg )");

		var left = current - 1;
		var new_obj = $("#carousel > a:nth-child("+left+") img");
		var new_x = getTranslateX(new_obj);
		var new_angle = getRotationDegrees(new_obj); 
		new_angle = 0;x = 0;
		new_obj.transition({
		  rotateY: new_angle+'deg',
		  duration: DURATION
		});
		new_obj.css("transform", "translateZ( 500px ) translateX("+x+"px) rotateY(   "+new_angle+"deg )");
		left -= 1;

		while (left > 0){
			var left_obj = $("#carousel > a:nth-child("+left+") img");
			var left_x = getTranslateX(left_obj);
			var left_angle = getRotationDegrees(left_obj);
			left_x += 20;
			if (left_x < -260){
				left_obj.css("visibility","hidden");
			}else{
				left_obj.css("visibility","visible");
			}
			left_obj.transition({
			  rotateY: left_angle+'deg',
			  duration: DURATION
			});
			left_obj.css("transform", "translateZ( 288px ) translateX("+left_x+"px) rotateY(   "+left_angle+"deg )");
			left -= 1;
		}

		var right = current + 1;
		while (right <= total){
			var right_obj = $("#carousel > a:nth-child("+right+") img");
			var right_x = getTranslateX(right_obj);
			var right_angle = getRotationDegrees(right_obj);
			right_x += 20;
			if (right_x > 260){
				right_obj.css("visibility","hidden");
			}else{
				right_obj.css("visibility","visible");
			}
			right_obj.transition({
			  rotateY: right_angle+'deg',
			  duration: DURATION
			});
			right_obj.css("transform", "translateZ( 288px ) translateX("+right_x+"px) rotateY(   "+right_angle+"deg )");
			right += 1;
		}
		current -= 1;
		setTimeout(function(){ clicked=false; }, DURATION);
	});
});