<template>
  <div v-if="count>0">
    <highcharts :options="chartOption" :constructor-type="'stockChart'" ref="chart"
    ></highcharts>
  </div>
  <div v-else>
    <el-empty :description="'暂无'+title+'数据'"></el-empty>
  </div>

</template>
<script>
import {Chart} from 'highcharts-vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import boostInt from 'highcharts/modules/boost'

Highcharts.setOptions({
  global: {
    useUTC: false
  }
});
stockInit(Highcharts)
boostInt(Highcharts)
export default {
  name: 'dataChart',
  props: {
    title: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    'highcharts': Chart,
  },
  data() {
    return {
      avg_result: "-1",
      sum: 0,
      count: 0,
      chartOption: {
        rangeSelector: {
          buttons: [],
          inputEnabled: false,
        },
        chart: {
          //alignTicks: false,
          //zoomType: 'x'
          width: null
        },
        tooltip: {
          shared: true // 开启交叉显示多条曲线的数据
        },
        credits: {
          enabled: false
        },
        title: {
          text: this.title
        },
        // yAxis: {
        //   title: {
        //     text: this.label
        //   },
        //   opposite: false,
        // },
        exporting: {
          enabled: false
        },
        legend: false,
        plotOptions: {
          series: {
            dataGrouping: {
              approximation: 'average',
              units: [[
                'minute',
                [1]
              ]]
            },
          }
        },
        series: [
          {
            name: this.title,
            type: "spline",
            data: [],
            tooltip: {
              pointFormat: '{point.series.name}:{point.y}'
            },
          }
        ]
      }
    }
  },
  methods: {
    clearData() {
      this.sum = 0;
      this.avg_result = "-1"
      this.count = 0
      for (let i in this.chartOption.series) {
        this.chartOption.series[i].data = []
      }

    },
    resize() {
      this.$refs.chart.chart.setSize(null, null)
    },
    addData(data) {
      let key = this.label.split(",")
      let title = this.title.split(",")
      if (key.length === 2) {
        this.chartOption.series.push(
            {
              name: this.title,
              type: "spline",
              data: [],
              tooltip: {
                pointFormat: '{point.series.name}:{point.y}'
              },
            }
        )
      }
      for (let i in key) {
        let value = parseFloat(data[key[i]])
        let time = (new Date()).getTime()
        this.chartOption.series[i].data.push([time, value])
        this.chartOption.series[i].name = title[i]
        this.sum += value
        this.count += 1
        this.avg_result = (this.sum / this.count).toFixed(2)
      }

    }
  },
  mounted() {
  }

}

</script>
<style scoped>

</style>