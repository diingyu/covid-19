<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>COVID-19</title>
	<script type="text/javascript" src="js/echarts.min.js"></script>
	<script type="text/javascript" src="js/jquery-3.5.0.min.js"></script>
    <script type="text/javascript" src="data/map.js"></script>
	<script type="text/javascript" src="data/data.js"></script>
	<script type="text/javascript" src="data/country.js"></script>
    <script type="text/javascript" src="data/top10.js"></script>
	<style type="text/css">
		* {
			margin:0 auto;
            padding:0;
            width: 1230px;
            border-color:white;
		}
        .head {
            height: 50px;
            background: darkblue;
            color:white;
            font-size:30px;
            text-align:center;
            line-height: 50px;

        }
        .total {
            background: black;
            border:1px solid rgba(255,255,255,0.8);
            height: 100px;
            line-height: 50px;
            text-align:center;
            font-size:20px;
        }
        .top10 {
            float:left;
            width:408px;
            height:300px;
            background: black;
            border:1px solid rgba(255,255,255,0.8);
        }
        .trend {
            height:300px;
            width:816px;
            background: black;
            color:white;
            border:1px solid rgba(255,255,255,0.8);
            float:left;
        }
        .map {
            height:500px;
            background: black;
            color:white;
            border:1px solid rgba(255,255,255,0.8);
            float:right;
        }
        .predict {
            float:left;
            height:50px; 
            background:darkblue; 
            color: white;
            font-size:30px;
            text-align:center;
            line-height: 50px;
        }
        .figure {
            float: left;
            width: 300px;
            height:230px;
            border:1px solid rgba(255,255,255,0.8);
        }
        .foot {
            background: grey;
            height:50px;
            color:white;
            text-align: center;
            border:1px solid rgba(255,255,255,0.8);
        }
    </style>
</head>
<body>
	<div class="head">
		COVID-19 in the world
	</div>
    
    <div class="total">
        <div id="update_day" style="float:left;color:white;text-align: center;width:310px;"></div>

        <div style="float:left;color:white;text-align:right;width:120px;">Confirmed:&nbsp;&nbsp;</div>
        <div id="TotalConfirmed" style="float:left;color:red;text-align:left;width:180px;"></div>

        <div style="float:left;color:white;text-align:right;width:120px;">Recovered:&nbsp;&nbsp;</div>
        <div id="TotalCured" style="float:left;color:red;text-align:left;width:180px;"></div>

        <div style="float:left;color:white;text-align:right;width:80px;">Death:&nbsp;&nbsp;</div>
        <div id="TotalDead" style="float:left;color:red;text-align:left;width:220px;"></div>

        <div style="float:left;color:white;text-align:right;width:420px;">World&nbsp;Recovered&nbsp;Rate:&nbsp;&nbsp;</div>
        <div id="health_index" style="float:left;color:red;text-align:left;width:180px;"></div>

        <div style="float:left;color:white;text-align:right;width:380px;">World&nbsp;Hope&nbsp;Index:&nbsp;&nbsp;</div>
        <div id="hope_index" style="float:left;color:red;text-align:left;width:220px;"></div>
    </div>

    <div id="world-trend" class="trend"></div>

    <div id="top10-confirmed" class="top10"></div>
    <div id="top10-deaths" class="top10"></div>
    <div id="top10-new-confirmed" class="top10"></div>
    <div id="top10-health" class="top10"></div>
    <div id="top10-hope-day" class="top10"></div>
    <div id="top10-death-rate" class="top10"></div>
    <div id="top10-infection-rate" class="top10"></div>

    <div id="map" class="map"></div>
    
    <div class="predict">
        cases of all countries sorted by descent
    </div>

   	<div style="overflow-y: auto;height: 250px;">
   		<script type="text/javascript">
	        var data = window.data;   
	        // console.log(data);
            //config the date 
            document.getElementById("update_day").innerHTML =  window.top10["Date"];

	        document.getElementById("TotalConfirmed").innerHTML = (window.top10["TotalConfirmed"]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
	        // console.log(TotalConfirmed);
	        // TotalConfirmed.innerHTML = "TotalConfirmed: "+data["TotalConfirmed"];
	        document.getElementById("TotalCured").innerHTML = (window.top10["TotalCured"]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
	        // TotalConfirmed.innerHTML = "TotalCured: "+data["TotalCured"];
	        document.getElementById("TotalDead").innerHTML = (window.top10["TotalDead"]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
	        // TotalConfirmed.innerHTML = "TotalDead: "+data["TotalDead"];
	        document.getElementById("health_index").innerHTML = window.top10["health_index"];
            document.getElementById("hope_index").innerHTML = window.top10["hope_index"];

	        for (var i = 0; i < window.country.length; i++) {
	            html = "<div id=\""+window.country[i]+"\" class=\"figure\"></div>";
	            document.writeln(html);
	        }
	        html = "<div style=\"clear:both;\"></div>";
	        document.writeln(html)
	        for (var i = 0; i < window.country.length; i++) {
	            var myChart = echarts.init(document.getElementById(window.country[i]), 'dark');
	            var option = {
	                title: {
	                    text: window.country[i]
	                },
	                tooltip: {
                        position:"top",
                        extraCssText:'width:160px;height:60px;background:red'
                    },
	                toolbox: {
	                	feature: {
	                		saveAsImage: {}
	                	}
	                },
	                legend: {
	                    data:['pre-confirmed','confirmed','recovered','death']
	                },
	                xAxis: {
	                    data: data["Period"]
	                },
                    grid: {
                        x: 100, //默认是80px
                        y: 60, //默认是60px
                        x2: 40, //默认80px
                        y2: 45 //默认60px
                    },
	                yAxis:  [
                        {
                            type : 'value',
                            axisLabel : {
                                margin:'0',
                                textStyle:{
                                  align:'right'
                                }
                            },
                        }
                    ],
	                series: [{
	                    name: 'pre-confirmed',
	                    type: 'line',
	                    data: data["data"][window.country[i]]["PreConfirmed"]
	                },
	                {
	                    name: 'confirmed',
	                    type: 'line',
	                    data: data["data"][window.country[i]]["Confirmed"]
	                },
                    {
                        name: 'recovered',
                        type: 'line',
                        data: data["data"][window.country[i]]["Cured"]
                    },
                    {
                        name: 'death',
                        type: 'line',
                        data: data["data"][window.country[i]]["Dead"]
                    }
	                ]
	            };
	            myChart.setOption(option);
	        }
    	</script>
   	</div>
	
    <div class="foot">
    	E-mail:&nbsp;30833663@qq.com&nbsp;;&nbsp;&nbsp;&nbsp;&nbsp;WeChat:&nbsp;dingyuLL
    	<br>
    	<a href="https://github.com/diingyu/COVID-19">code source here</a>
    </div>
</body>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-confirmed"), 'white');
    option = {
        title: {
            text: "CASES TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            }
        },
        backgroundColor: 'black',
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["confirmed"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["confirmed"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "darkred",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-deaths"), 'white');
    option = {
        title: {
            text: "DEATHS TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            }
        },
        backgroundColor: 'black',
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["deaths"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["deaths"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "darkgrey",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-new-confirmed"), 'white');
    option = {
        title: {
            text: "NEW CASES TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            }
        },
        backgroundColor: 'black',
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["increase"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["increase"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "darkorange",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-health"), 'white');
    option = {
        title: {
            text: "RECOVERED RATE TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            },
            itemGap:2,
            subtext:"(recovered/cases,  0-1)"
        },
        backgroundColor: 'black',
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["hope"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["hope"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "darkgreen",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-hope-day"), 'white');
    option = {
        title: {
            text: "HOPE INDEX TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            },
            itemGap:2,
            subtext:"(new recovered/new cases)"
        },
        backgroundColor: 'black',
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["hope_day"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["hope_day"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "purple",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-death-rate"), 'white');
    option = {
        title: {
            text: "FATALITY RATE TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            },
            itemGap:2,
            subtext:"(death/cases,  0-1)"
        },
        backgroundColor: 'black',
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["death_rate"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["death_rate"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "grey",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    // draw top10 confirmed figure
    var top10 = window.top10;
    var myChart = echarts.init(document.getElementById("top10-infection-rate"), 'white');
    option = {
        title: {
            text: "infection RATE TOP 10",
            left:"center",
            textStyle: {
                color:"white",
                fontSize:15
            },
            itemGap:2,
            subtext:"(confirmed/population,  0-1000)"
        },
        backgroundColor: 'black',
        tooltip: {
            trigger: 'item',
            position:"bottom",
            showDelay: 0,
            transitionDuration: 0.2,
            extraCssText:'width:160px;height:20px;',
            formatter: function (params) {
                return "click to see details";
            }
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '11%',
            bottom: '2.5%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [{
            type: 'category',
            data: top10["infection_rate"]["country"],
            inverse: true,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                margin: 10,
                textStyle: {
                    fontSize: 10,
                    color: 'white'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#2548ac'
                }
            },
        }],
        xAxis: [{
            type: 'value',
            axisLabel: {
                margin: 10,
                interval: 1, //横轴信息全部显示  
                rotate: -30, //-15度角倾斜显示  
                textStyle: {
                    fontSize: 10,
                    color: 'white',
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#192469'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#17367c'
                }
            }
        }],
        series: [{
            name: 'Top 10',
            type: 'bar',
            barWidth: 12,
            data: top10["infection_rate"]["data"],
            label: {
                normal: {
                    show: true,
                    position: 'insideright',
                    textStyle: {
                        color: 'white', //color of value
                        fontSize: 12,
                    }
                }
            },
            itemStyle: {
                normal: {
                    color: "darkblue",
                    shadowColor: 'rgba(0,0,0,0.1)',
                    shadowBlur: 3,
                    shadowOffsetY: 3
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.on("click", function(params) {
        document.getElementById(params.name).scrollIntoView();
    });
</script>

<script type="text/javascript">
    data = window.top10["world_trend"]
    var myChart = echarts.init(document.getElementById('world-trend', 'white'));
    var option = {
        title: {
            text: "WORLD TREND",
            left: 'center',
            textStyle: {
                color:"white",
                fontSize:15
            },
        },
        backgroundColor: 'black',
        tooltip: {
            position:"top",
            extraCssText:'width:160px;height:60px;background:red'
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        legend: {
            data:data["country"],
            top:"10%",
            textStyle: {
                color:"white",
                fontSize:15
            },
        },
        xAxis: {
            data: data["period"],
            axisLabel : {
                margin:'0',
                textStyle:{
                  align:'right',
                  color:'white'
                }
            },
        },
        grid: {
            x: 100, //默认是80px
            y: 60, //默认是60px
            x2: 40, //默认80px
            y2: 45 //默认60px
        },
        yAxis:  [
            {
                type : 'value',
                axisLabel : {
                    margin:'0',
                    textStyle:{
                      align:'right',
                      color:'white'
                    }
                },
            }
        ],
        series: [{
                name: "new cases",
                type: 'line',
                data: data["cases"],
                label: {
                    normal: {
                        show: true,
                        position: 'right'
                    }
                },
            },{
                name: "new recovered",
                type: 'line',
                data: data["recovered"],
                label: {
                    normal: {
                        show: true,
                        position: 'right'
                    }
                },
            },{
                name: "new deaths",
                type: 'line',
                data: data["deaths"],
                label: {
                    normal: {
                        show: true,
                        position: 'right'
                    }
                },
            }
        ]
        
    };
    myChart.setOption(option);
</script>

<script type="text/javascript">
	function geoWorldData(data) {
		var myChart = echarts.init(document.getElementById("map"));
    	echarts.registerMap('world', data);
    	option = {
            title: {
                text: 'Total Cases Distributed',
                left: 'right',
                textStyle: {
                    color:"white",
                    fontSize:15
                },
                itemGap:2,
            },
            grid: {
                top: '10%',
                left: '3%',
                right: '11%',
                bottom: '2.5%',
                containLabel: true
            },
            tooltip: {
                trigger: 'item',
                showDelay: 0,
                transitionDuration: 0.2,
                extraCssText:'width:160px;height:80px;background:red',
                formatter: function (params) {
                    var confirmed = (params.data.value[2]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
                    var recovered = (params.data.value[0]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
                    var death = (params.data.value[1]+'').replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
                    return "confirmed:"+confirmed+"<br/>"+"recovered:"+recovered+"<br/>"+"death:"+death+"<br/>"+"(click to see details)";
                }
            },
            visualMap: {
                left: 'right',
                top: 'center',
                min: 100000,
                max: 1000000,
                inRange: {
                    // color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                    color: ['#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                },
                text:['High','Low'],           // 文本，默认为数值文本
                calculable: true
            },
            toolbox: {
                show: true,
                orient: 'vertical',
                left: 'left',
                top: 'top',
                feature: {
                    dataView: {show:true, readOnly: false},
                    restore: {},
                    saveAsImage: {}
                }
            },
            series: [
                {
                    name: 'Confirmed of Countries',
                    type: 'map',
                    map: 'world',
                    roam: true,
                    zoom: 1.2,
                    itemStyle:{
                        normal:{label:{show:true}},
                        emphasis:{label:{show:true}}
                    },
                    //进行设置，显示国家名称时同时显示其新闻数量
                    data:window.map_data,
                    // 自定义名称映射
                    nameMap: {
                    	"United States":"US",
                        "Greenland":"Denmark",
                        "Palestine":"West Bank and Gaza"
                    }
                }
            ]
        };
    	myChart.setOption(option);
        myChart.on("click", function(params) {
            document.getElementById(params.name).scrollIntoView();
        });
	}
</script>

</script>
<!-- 这句代码非常重要，需要放在最后，相当于定义函数后，在此进行调用-->
<script type="text/javascript" src="data/world.json?callback=geoWorldData"></script>

</html>