<template>
  <div>
    <div class="row">
        <div class="col-lg-12">
            <h1 class="page-header">Dashboard</h1>
        </div>
        <!-- /.col-lg-12 -->
    </div>            
    <div class="row" ng-app="myApp" ng-controller="myCtrl">
        <div class="col-lg-8">
            <status></status>
            <!-- /.panel -->
        </div>
        <div class="col-lg-4">
            <system-info></system-info>
            <chat></chat>
        </div>
        <!-- /.col-lg-4 -->
    </div>
    <!-- /.row -->
    <!--
    Value: {{ count }}
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
    <button @click="incrementIfOdd">Increment if odd</button>
    <button @click="incrementAsync">Increment async</button>
    <button @click="socketConnect">Reverse Message</button>
    <div>Recent History (last 5 entries): {{ recentHistory }}</div>
    -->
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import BarChart from './BarChart'
import Chat from './Chat'
import SystemInfo from './SystemInfo'
import Status from './Status'
export default {
  computed: mapGetters([
    'count',
    'recentHistory'
  ]),
  components: {
    Status,
    BarChart,
    SystemInfo,
    Chat
  },
  methods: {
    ...mapActions([
      'increment',
      'decrement',
      'incrementIfOdd',
      'incrementAsync'
    ])
  }
}

</script>