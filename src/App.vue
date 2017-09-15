<template>
<div id="wrapper">
    <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="index.html">深度學習教學管理系統</a>
        </div>
        <div class="navbar-default sidebar" role="navigation">
            <div class="sidebar-nav navbar-collapse">
                <ul class="nav" id="side-menu">
                    <li class="sidebar-search">
                        <div class="input-group custom-search-form">
                            <input type="text" class="form-control" placeholder="Search...">
                            <span class="input-group-btn">
                            <button class="btn btn-default" type="button">
                                <i class="fa fa-search"></i>
                            </button>
                        </span>
                        </div>
                    </li>                     
                    <li>
                        <router-link :to="{ path: '/' }"><i class="fa fa-dashboard fa-fw"></i> 系統儀錶板</router-link>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> 圖表<span class="fa arrow"></span></a>
                        <ul class="nav nav-second-level">
                            <li>
                                <router-link href="#" :to="{ path: '/' }" >全班出席率</router-link>
                            </li>
                            <li>
                                <router-link href="#" :to="{ path: '/' }" >個人出席率</router-link>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <router-link :to="{ path: '/' }"><i class="fa fa-table fa-fw"></i> 表</router-link>
                    </li>
                    <li>
                        <router-link :to="{ path: '/' }"><i class="fa fa-edit fa-fw"></i> 教師評價系統</router-link>
                    </li>
                    <li>
                        <router-link :to="{ path: '/' }"><i class="fa fa-sitemap fa-fw"></i> 班級成員編輯</router-link>
                    </li>
                    <li>
                        <router-link :to="{ path: '/' }"><i class="fa fa-sitemap fa-fw"></i> Register</router-link>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-files-o fa-fw"></i> 頁面管理<span class="fa arrow"></span></a>
                        <ul class="nav nav-second-level">
                            <li>
                                <router-link href="#" :to="{ path: '/' }">管理頁面</router-link>
                            </li>
                            <li>
                                <router-link href="#" :to="{ path: '/' }">新增頁面</router-link>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-wrench fa-fw"></i> 設定<span class="fa arrow"></span></a>
                        <ul class="nav nav-second-level">
                            <li>
                                <router-link href="#" :to="{ path: '/' }">修改帳戶資訊</router-link>
                            </li>
                            <li>
                                <router-link href="#" :to="{ path: '/' }">缺曠計畫調整</router-link>
                            </li>
                            <li>
                                <router-link href="#" :to="{ path: '/' }">學生影像資料庫</router-link>
                            </li>
                            <li>
                                <router-link href="#" :to="{ path: '/' }">日誌</router-link>
                            </li>                  
                        </ul>
                    </li>                        
                </ul>
            </div>
        </div>
    </nav>

    <div id="page-wrapper">
        <router-view></router-view>
        <footer class="text-center">系統設計 © 2017 任家輝</footer>
    </div>
</div>
</template>
<script>
export default {
  name: 'app'
}
</script>