Raphael.fn.pieChart = function (cx, cy, r, values, labels, stroke, total, titletext) {
    var paper = this,
        rad = Math.PI / 180,
        chart = this.set(),
		title = paper.text(cx,10,titletext);
		chart.push(title);
    function sector(cx, cy, r, startAngle, endAngle, params) {
        var x1 = cx + r * Math.cos(-startAngle * rad),
            x2 = cx + r * Math.cos(-endAngle * rad),
            y1 = cy + r * Math.sin(-startAngle * rad),
            y2 = cy + r * Math.sin(-endAngle * rad);
        return paper.path(["M", cx, cy, "L", x1, y1, "A", r, r, 0, +(endAngle - startAngle > 180), 0, x2, y2, "z"]).attr(params);
    }
    var angle = 0,
        start = 0.4,
        process = function (j) {
            var value = values[j],
                angleplus = 360 * value / total,
                popangle = angle + (angleplus / 2),
                color = Raphael.hsb(start, .75, 1),
                ms = 500,
                delta = 30,
                bcolor = Raphael.hsb(start, 1, 0.7),
                p = sector(cx, cy, r, angle, angle + angleplus, {fill: "90-" + bcolor + "-" + color, stroke: stroke, "stroke-width": 3, title: labels[j]});
				//txt = paper.text(cx + (r) * Math.cos(-popangle * rad), cy + (r + delta + 25) * Math.sin(-popangle * rad), labels[j]).attr({fill: Raphael.hsb(0, 0, 0), opacity: 1, "font-size": 12, "text-anchor": "start"});
				//rect = paper.rect(cx + (r + delta + 55) * Math.cos(-popangle * rad), cy + (r + delta + 25) * Math.sin(-popangle * rad), txt.width, txt.height);
				//txt.addClass("infobox");
				//txt.hide();
            p.mouseover(function () {
                p.stop().animate({transform: "s1.1 1.1 " + cx + " " + cy}, ms, "elastic");
				//txt.show();
            }).mouseout(function () {
                p.stop().animate({transform: ""}, ms, "elastic");
                //txt.hide();
            });
            angle += angleplus;
            chart.push(p);
			//chart.push(rect);
            //chart.push(txt);
			
            start += .1;
        };
    for (i = 0; i < values.length; i++) {
        process(i);
    }
    return chart;
};

Raphael.fn.pieChartCircle = function (cx, cy, r, label, stroke, titletext) {
	var paper = this,
	chart = this.set(),
	circle = paper.circle(cx,cy,r,label,stroke),
	color = Raphael.hsb(0.4, .75, 1),
	bcolor = Raphael.hsb(0.4, 1, 0.7),
	title = paper.text(cx,10,titletext);
	chart.push(title);
	circle.attr({fill: "90-" + bcolor + "-" + color, stroke: stroke, "stroke-width": 3, title: label});
	circle.mouseover(function () {
		circle.stop().animate({transform: "s1.1 1.1 " + cx + " " + cy}, 500, "elastic");
	}).mouseout(function () {
		circle.stop().animate({transform: ""}, 500, "elastic");
	});
	
	chart.push(circle);
	return chart;
}

Raphael.fn.pieChartEmpty = function (cx, cy, r, titletext) {
	var paper = this,
	chart = this.set(),
	circle = paper.circle(cx,cy,r, "", "#fff"),
	text = paper.text(cx,cy,"No data"),
	title = paper.text(cx,10,titletext);
	chart.push(title);
	circle.attr({fill: "#CFCFCF", stroke: "#fff"});
	chart.push(circle);
	chart.push(text);
	return chart;
}

	
function createPie(key, pie) {
	var values = [],
		labels = (typeof pie["labels"] != 'undefined' ? pie["labels"] : []),
		total = 0,
		holder = pie["holder"],
		datatable= pie["datatable"],
		title= pie["title"];

	$(datatable + " tbody tr").each(function () {
		val = parseInt($(this).children("td").last().text(), 10);
		if(val > 0) { values.push(val);
		total += val;
		
		label = ""
		$(this).children("td").each(function (index) {
			label += $(datatable + " thead th").eq(index).html() + " " + $(this).html() + "\n";
		});
		labels.push(label);
		}
	});

	if(values.length > 1) {
		
		Raphael(holder, 250, 250).pieChart(125, 125, 100, values, labels, "#fff", total, title);
		
	} else {
		Raphael(holder, 250, 250).pieChartCircle(125, 125, 100, labels[0], "#fff", title);
	}
}
