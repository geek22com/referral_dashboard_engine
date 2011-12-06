function drawCtrCharts(values, elemClicks, elemCtr) {
	var dt = new google.visualization.DataTable();
	dt.addColumn('string', 'Время');
	dt.addColumn('number', 'Показы');
	dt.addColumn('number', 'Клики');
	dt.addRows(values.length);
	
	var dtc = new google.visualization.DataTable();
	dtc.addColumn('string', 'Время');
	dtc.addColumn('number', 'CTR');
	dtc.addRows(values.length);

	var ind = 0;
	$.each(values, function(i, val) {
		dt.setValue(ind, 0, val.time);
		dt.setValue(ind, 1, val.shows);
		dt.setValue(ind, 2, val.clicks);
		
		dtc.setValue(ind, 0, val.time);
		dtc.setValue(ind, 1, val.shows > 0 ? val.clicks/val.shows : 0);
		
		ind++;
	});
	
	var w = Math.max(values.length * 50, 900);
	var h = 300;
	var options = { 
		width: w, height: h, fontSize: 14, legend: 'none',
		hAxis: { slantedText: true, slantedTextAngle: 90 },
		chartArea: { left: 40, top: 30, width: w-40 }
	};
	
	var chClicks = new google.visualization.ColumnChart(elemClicks);
	chClicks.draw(dt, options);
	
	var chCtr = new google.visualization.LineChart(elemCtr);
	chCtr.draw(dtc, options);
}