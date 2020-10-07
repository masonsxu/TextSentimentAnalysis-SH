 $(window).load(function(){$(".loading").fadeOut()})  
$(function () {
    echarts_1();
	echarts_2();
	echarts_3();
	echarts_4();
	echarts_5();
    zb1();
    zb2();
    zb3();
    zb4()

function echarts_1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart1'));
        option = {
                    tooltip : {
                        trigger: 'item',
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        right:10,
                        top:30,
                        height:140,
                        itemWidth:10,
                        itemHeight:10,
                        itemGap:10,
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize:12
                        },
                        orient:'vertical',
                        data:['上海市','北京市','重庆市']
                    },
                   calculable : true,
                    series : [
                        {
                            name:' ',
							color: ['#62c98d', '#2f89cf', '#4cb9cf', '#53b666', '#62c98d', '#205acf', '#c9c862', '#c98b62', '#c962b9', '#7562c9','#c96262'],
                            type:'pie',
                            radius : [30, 70],
                            center : ['35%', '50%'],
                            roseType : 'radius',
                            label: {
                                normal: {
                                    show: true
                                },
                                emphasis: {
                                    show: true
                                }
                            },

                            lableLine: {
                                normal: {
                                    show: false
                                },
                                emphasis: {
                                    show: true
                                }
                            },

                            data:[
                                {value:4.6, name:'上海市'},
                                {value:3.9, name:'北京市'},
                                {value:3.5, name:'重庆市'}

                            ]
                        },
                    ]
                };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
function echarts_2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart2'));

        option = {
                    tooltip : {
                        trigger: 'item',
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        right:10,
                        top:30,
                        height:140,
                        itemWidth:10,
                        itemHeight:10,
                        itemGap:10,
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize:12
                        },
                        orient:'vertical',
                        data:['重庆市','上海市','北京市']
                    },
                   calculable : true,
                    series : [
                        {
                            name:' ',
							color: [ '#c98b62', '#c962b9', '#7562c9','#c96262'],
                            type:'pie',
                            radius : [30, 70],
                            center : ['35%', '50%'],
                            roseType : 'radius',
                            label: {
                                normal: {
                                    show: true
                                },
                                emphasis: {
                                    show: true
                                }
                            },

                            lableLine: {
                                normal: {
                                    show: true
                                },
                                emphasis: {
                                    show: true
                                }
                            },

                            data:[
                                {value:75.37, name:'重庆市'},
                                {value:60.51, name:'上海市'},
                                {value:53.18, name:'北京市'}

                            ]
                        },
                    ]
                };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
function echarts_3() {
        // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById("echart3"));

        $.get('json/beijing.json', function (data) {
            myChart.setOption(option = {

                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        lineStyle: {
                            color: '#dddc6b'
                        }
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLabel:  {
                        textStyle: {
                            color: "rgba(255,255,255,.6)",
                            fontSize:16,
                        },
                    },
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }

                    },
                    data: data.map(function (item) {
                        return item[0];
                    })
                },
                yAxis: {
                    type: 'value',
                    axisTick: {show: false},
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    },
                    axisLabel:  {
                        textStyle: {
                            color: "rgba(255,255,255,.6)",
                            fontSize:14,
                        },
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    }
                },
                toolbox: {
                    left: 'center',
                    feature: {
                        dataZoom: {
                            yAxisIndex: 'none'
                        },
                        restore: {},
                        saveAsImage: {}
                    }
                },
                dataZoom: [{
                    startValue: '2014-06-01'
                }, {
                    type: 'inside'
                }],
                visualMap: {
                    top: 10,
                    right: 10,
                    pieces: [{
                        gt: 0,
                        lte: 100,
                        color: 'rgba(98,201,141)'
                    }, {
                        gt: 100,
                        lte: 1000,
                        color: 'rgba(201,200,98)'
                    }, {
                        gt: 1000,
                        lte: 5000,
                        color: 'rgba(201,139,98)'
                    }, {
                        gt: 5000,
                        lte: 10000,
                        color: 'rgba(32,90,207)'
                    }, {
                        gt: 10000,
                        lte: 30000,
                        color: '#F73466'
                    }, {
                        gt: 300000,
                        color: '#D84339'
                    }],
                    outOfRange: {
                        color: '#999'
                    }
                },
                series: {
                    name: '北京(朝阳区)2017全年的最小水平能见度(米)图示',
                    type: 'line',
                    data: data.map(function (item) {
                        return item[1];
                    }),
                    markLine: {
                        silent: true,
                        data: [{
                            yAxis: 100
                        }, {
                            yAxis: 1000
                        }, {
                            yAxis: 5000
                        }, {
                            yAxis: 10000
                        }, {
                            yAxis: 30000
                        }]
                    }
                }
            });
        });
        myChart.setOption(option)
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
function echarts_4() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart4'));

    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: ['温度/ ℃', '湿度/百分比'],
            align: 'right',
            right: '40%',
            top:'0%',
            textStyle: {
                color: "#fff",
                fontSize: '16',

            },
            itemWidth: 16,
            itemHeight: 16,
            itemGap: 35
        },
        grid: {
            left: '0%',
            top:'40px',
            right: '0%',
            bottom: '2%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
            axisLine: {
                show: true,
                lineStyle: {
                    color: "rgba(255,255,255,.1)",
                    width: 0.5,
                    type: "solid"
                },
            },

            axisTick: {
                show: false,
            },
            axisLabel:  {
                interval: 0,
                rotate:50,
                show: true,
                splitNumber: 15,
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: '16',
                },
            },
        }],
        yAxis: [{
            type: 'value',
            axisLabel: {
                //formatter: '{value} %'
                show:true,
                textStyle: {
                    color: "rgba(255,255,255,.6)",
                    fontSize: '16',
                },
            },
            axisTick: {
                show: false,
            },
            axisLine: {
                show: true,
                lineStyle: {
                    color: "rgba(255,255,255,.1	)",
                    width: 1,
                    type: "solid"
                },
            },
            splitLine: {
                lineStyle: {
                    color: "rgba(255,255,255,.1)",
                }
            }
        }],
        series: [{
            name: '温度/ ℃',
            type: 'bar',
            data:[6.67,6.7,10,17,21.72,23.78,31.4,29.43,24.4,19.02,13.47,6.75],
            barWidth:'15', //柱子宽度
            // barGap: 1, //柱子之间间距
            itemStyle: {
                normal: {
                    color:'#2f89cf',
                    opacity: 1,
                    barBorderRadius: 5,
                }
            }
        }, {
            name: '湿度/百分比',
            type: 'bar',
            data:[74.98,68,70,67,69.73,80.38,70.34,77.80,80.85,77.50,75,67.9],
            barWidth:'15',
            // barGap: 1,
            itemStyle: {
                normal: {
                    color:'#62c98d',
                    opacity: 1,
                    barBorderRadius: 5,
                }
            }
        },
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
function echarts_5() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart5'));
option = {
  //  backgroundColor: '#00265f',
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['积极情感分数', '消极情感分数'],
        align: 'right',
        right: '40%',
		top:'0%',
        textStyle: {
            color: "#fff",
		    fontSize: '16',

        },

        itemGap: 35
    },
    grid: {
        left: '0%',
		top:'40px',
        right: '0%',
        bottom: '2%',
       containLabel: true
    },
    xAxis: [{
        type: 'category',
      		data: ['2019/1/11','2019/2/13','2019/2/20', '2019/2/21', '2019/2/22', '2019/2/24', '2019/2/27', '2019/3/5',  '2019/3/8', '2019/3/8','2019/3/19','2019/3/30'],

        axisLine: {
            show: true,
         lineStyle: {
                color: "rgba(255,255,255,.1)",
                width: 1,
                type: "solid"
            },
        },
        axisTick: {
            show: false,
        },
		axisLabel:  {
                interval: 0,
                rotate:50,
                show: true,
                splitNumber: 15,
                textStyle: {
 					color: "rgba(255,255,255,.6)",
                    fontSize: '16',
                },
            },
    }],
    yAxis: [{
        type: 'value',
        axisLabel: {
           //formatter: '{value} %'
			show:true,
			 textStyle: {
 					color: "rgba(255,255,255,.6)",
                    fontSize: '16',
                },
        },
        axisTick: {
            show: false,
        },
        axisLine: {
            show: true,
            lineStyle: {
                color: "rgba(255,255,255,.1	)",
                width: 1,
                type: "solid"
            },
        },
        splitLine: {
            lineStyle: {
               color: "rgba(255,255,255,.1)",
            }
        },

    }],
    series: [{
        name: '积极情感分数',
        type: 'line',

        data: [39,4,27,11,6,10,21,12,7,118,9,67],

        itemStyle: {
            normal: {
                color:'#2f89cf',
                opacity: 1,

				barBorderRadius: 5,
            }
        }
    }, {
        name: '消极情感分数',
        type: 'line',
        data: [37,9,19,39,5,8,0.5,42,27,10,6,2],
		barWidth:'15',
       // barGap: 1,
        itemStyle: {
            normal: {
                color:'#62c98d',
                opacity: 1,
				barBorderRadius: 5,
            }
        }
    },
	]
};


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

    function zb1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('zb1'));
        var v1=11726
        var v2=45226//未结算数
        var v3=v1+v2//总订单数
        option = {
            series: [{
                type: 'pie',
                radius: ['60%', '70%'],
                color:'#49bcf7',
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: v1,
                    name: '重庆雾霾天比例',
                    label: {
                        normal: {
                            formatter:Math.round( v1/v3*100)+ '%',
                            textStyle: {
                                fontSize: 30,
                                color:'#fff',
                            }
                        }
                    }
                },
                    {
                        value: v2,
                        label: {
                            normal: {
                                formatter : function (params){
                                    return '重庆雾霾天比例'
                                },
                                textStyle: {
                                    color: '#aaa',
                                    fontSize: 16
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: 'rgba(255,255,255,.2)'
                            },
                            emphasis: {
                                color: '#fff'
                            }
                        },
                    }]
            }]
        };
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function zb3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('zb2'));
        var v1=2543//作品语种
        var v2=21348//未结算数
        var v3=v1+v2//总订单数
        option = {

//animation: false,
            series: [{
                type: 'pie',
                radius: ['60%', '70%'],
                color:'#49bcf7',
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: v1,
                    name: '北京雾霾比例',
                    label: {
                        normal: {
                            formatter:Math.round( v1/v3*100)+ '%',
                            textStyle: {
                                fontSize: 24,
                                color:'#fff',
                            }
                        }
                    }
                }, {
                    value: v2,
                    label: {
                        normal: {
                            formatter : function (params){
                                return '北京雾霾比例'
                            },
                            textStyle: {
                                color: '#aaa',
                                fontSize: 16
                            }
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgba(255,255,255,.2)'
                        },
                        emphasis: {
                            color: '#fff'
                        }
                    },
                }]
            }]
        };
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function zb2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('zb3'));
        var v1=1839//结算金额
        var v2=7458//未结算
        var v3=v1+v2
        option = {
            series: [{

                type: 'pie',
                radius: ['60%', '70%'],
                color:'#62c98d',
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: v1,
                    name: '北京雨天比例',
                    label: {
                        normal: {
                            formatter:Math.round( v1/v3*100)+ '%',
                            textStyle: {
                                fontSize: 24,
                                color:'#fff',
                            }
                        }
                    }
                }, {
                    value: v2,
                    label: {
                        normal: {
                            formatter : function (params){
                                return '北京雨天比例'
                            },
                            textStyle: {
                                color: '#aaa',
                                fontSize: 16
                            }
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgba(255,255,255,.2)'
                        },
                        emphasis: {
                            color: '#fff'
                        }
                    },
                }]
            }]
        };
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function zb4() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('zb4'));
        var v1=10096//结算金额
        var v2=14864//未结算
        var v3=v1+v2
        option = {
            series: [{

                type: 'pie',
                radius: ['60%', '70%'],
                color:'#29d08a',
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: v1,
                    name: '重庆雨天比例',
                    label: {
                        normal: {
                            formatter:Math.round( v1/v3*100)+ '%',
                            textStyle: {
                                fontSize: 24,
                                color:'#fff',
                            }
                        }
                    }
                }, {
                    value: v2,
                    label: {
                        normal: {
                            formatter : function (params){
                                return '重庆雨天比例'
                            },
                            textStyle: {
                                color: '#aaa',
                                fontSize: 16
                            }
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgba(255,255,255,.2)'
                        },
                        emphasis: {
                            color: '#fff'
                        }
                    },
                }]
            }]
        };
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
})


