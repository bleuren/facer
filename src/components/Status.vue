<template>
<div class="panel panel-default">
    <div class="panel-heading">
        <i class="fa fa-bar-chart-o fa-fw"></i> 學生學習情況
        <div class="pull-right">
            <div class="btn-group">
                <button type="button" @click="socketConnect" class="btn btn-default btn-xs" data-toggle="button" aria-pressed="false" autocomplete="off">
                    開始記錄
                </button>
                <button type="button" @click="fillData()" class="btn btn-default btn-xs" data-toggle="button" aria-pressed="false" autocomplete="off">
                    Fill Data
                </button>                
            </div>
        </div>
    </div>
    <!-- /.panel-heading -->
    <div class="panel-body">
        <div class="row">
            <div class="col-lg-6">
                <div class="table-responsive">
                    <table class="table table-bordered table-hover table-striped">
                        <thead>
                            <tr>
                                <th>名稱</th>
                                <th>分鐘數</th>
                                <th>目前情緒</th>
                                <th>累計情緒</th>
                                <th>百分比</th>
                                <th>判斷結果</th>
                            </tr>
                        </thead> 
                        <tbody>
                            <tr v-for="label in labels" v-bind:key="label">
                                <td>{{ label }}</td>
                                <td>0 / 0</td>
                                <td>None</td>
                                <td>None</td>
                                <td>0%</td>
                                <td>曠課</td>
                            </tr>
                        </tbody>
                    </table>                                                     
                </div>
                <p id="searchResult"></p>
                <!-- /.table-responsive -->
            </div>
            <!-- /.col-lg-4 (nested) chart-->
            <div class="col-lg-6">
                <bar-chart :chart-data="datacollection"></bar-chart>
                <p><img :src="jsonObj.view" class="img-responsive"/></p>
            </div>
            <!-- /.col-lg-8 (nested) -->
        </div>
        <!-- /.row -->
    </div>
    <!-- /.panel-body -->
    
</div>
</template>

<script>
import BarChart from './BarChart'
export default {
  data () {
    return {
      jsonObj: '',
      labels: '',
      datacollection: null
    }
  },
  components: {
    BarChart
  },
  mounted () {
    this.$socket.emit('labels')
  },
  sockets: {
    connect () {
      console.log('socket connected(status)')
    },
    message (value) {
      this.jsonObj = value
      console.log(value)
    },
    labels (value) {
      this.labels = value
      this.fillData()
    }
  },
  methods: {
    socketConnect: function (val) {
      this.$socket.emit('predict', {'tresh': 0.7, 'course': 'hello'})
    },
    fillData () {
      this.datacollection = {
        labels: this.labels,
        datasets: [
          {
            label: 'GitHub Commits',
            backgroundColor: '#f87979',
            data: Array.from({length: 44}, () => Math.floor(Math.random() * 44))
          }
        ]
      }
    },
    getRandomInt () {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
    }
  }
}

</script>
<style>
tbody {
    display:block;
    height:500px;
    overflow:auto;
}
thead, tbody tr {
    display:table;
    width:100%;
    table-layout:fixed;
}
thead {
    width: calc( 100% - 6px )
}

/* Let's get this party started */
::-webkit-scrollbar {
    width: 6px;
}
 
/* Track */
::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.2);
}
 
/* Handle */
::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.2); 
}
::-webkit-scrollbar-thumb:window-inactive {
    background: rgba(0,0,0,0.4); 
}
</style>